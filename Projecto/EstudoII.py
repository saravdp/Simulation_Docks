import statistics

import numpy as np
import simpy
import random
import matplotlib.pyplot as plt
from tabulate import tabulate

random.seed(123)
interarrival_frequency = [
        [5, 1],
        [6, 3],
        [7, 6],
        [8, 7],
        [9, 9],
        [10, 10],
        [11, 11],
        [12, 11],
        [13, 11],
        [14, 9],
        [15, 7],
        [16, 6],
        [17, 5],
        [18, 4]
    ]
unload_time = [
        [9, 20],
        [10, 22],
        [11, 19],
        [12, 16],
        [13, 10],
        [14, 8],
        [15, 3],
        [16, 2]
    ]
# Preparação dos dados
def prep_data(data):
    sum = 0

    for a in interarrival_frequency:
        sum += a[1]

    for i in range(len(data)):
        data[i].append(data[i][1] / sum)
        data[i].append(data[i][2] + data[i - 1][3] if i > 0 else data[i][2])


def get_value(data):
    value = random.random()
    for a in data:
        if a[3] > value:
            return a[0]
    return data[-1][0]

shipsTable=[]

class Ship:
    prep_data(interarrival_frequency)
    prep_data(unload_time)

    def __init__(self, env, docks, id_ship):
        # A well-known solutions to a deadlock is to allocate resources in some globally defined order
        self.env, self.docks, self.id = env, sorted(docks, key=id), id_ship
        self.waitedTime = 0
        self.interval = 0
        self.unloading = 0
        self.waiting_times = []
        env.process(self.run_life_cicle())


    def get_docks(self):

        self.log("request first fork")
        dock1_rq = self.docks[0].request()
        yield dock1_rq

        self.log("Obtained the two docks")

        return dock1_rq

    def release_docks(self, fork1_rq):
        self.docks[0].release(fork1_rq)
        self.log("The docks were released")

    def run_life_cicle(self):
        while True:
            start_waiting = self.env.now
            arrival_time = self.env.now
            T0 = get_value(interarrival_frequency)  # Mean arrival time
            T1 = get_value(unload_time)  # Mean unloading time
            # arrivals time
            arrivals_time = random.expovariate(1 / T0)

            yield self.env.timeout(arrivals_time)
            # Getting hungry
            get_docks_process = self.env.process(self.get_docks())
            docks1_rq = yield get_docks_process

            # unloading time
            unloading_time = random.expovariate(1 / T1)
            yield self.env.timeout(unloading_time)
            self.interval = arrivals_time
            self.unloading = unloading_time
            self.release_docks(docks1_rq)

            self.waitedTime = self.env.now - start_waiting

            self.waiting_times = self.env.now - arrival_time


    def log(self, message):
        # print(f"@{self.env.now} Philosopher {self.id} - {message}")
        pass

    # def print_stats(self):
    #     if self.waiting_times:
    #         average_wait = statistics.mean(self.waiting_times)
    #         minutes, frac_minutes = divmod(average_wait, 1)
    #         return round(minutes)
    #     else:
    #         print("No data to present.")

def simulate(n_ships, time):
    env = simpy.Environment()

    # A fork is a reusable resource that should not be shared.
    docks = [simpy.Resource(env, capacity=1)]

    # Instantiate ships and assign them two docks (left and right)
    ships = Ship(env, docks, n_ships)
    env.run(until=time)

    shipsTable.append([n_ships, ships.interval, ships.waitedTime, ships.unloading, ships.waiting_times])
    # print(shipsTable)

    return # sum(ship.waitedTime for ship in ships) / n_ships







def main(max_ships, time, filename):


    X = range(1, max_ships +1)
    for n in X:
        simulate(n, time)

    unloading = 0
    size = 0
    arrival=0
    queue1 = 0
    total1 = 0
    for i in shipsTable:
        queue1 += i[2]
        arrival += i[1]
        total1 += i[4]
        #descarga
        unloading += i[3]
        size += 1

    print("Media de tempos de fila")
    print(unloading / size)
    print("media descarga")
    print(unloading/size)
    print("Media de tempos de chegada")
    print(arrival/size)
    print("Media de tempos no porto")
    print(total1 / size)
    print(tabulate(shipsTable))
if __name__ == "__main__":

    max_ships = 20
    time = 20000
    filename = "imgs/ships_3.jpg"

    main(max_ships, time,  filename)

