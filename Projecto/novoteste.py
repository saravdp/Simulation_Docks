import numpy as np
import simpy
import random

# Preparação dos dados
from tabulate import tabulate


def get_value(data):
    count1 = 0
    freq = 0
    min1 = data[0][0]
    max1 = data[0][0]
    for el in data:
        count1 += el[0] * el[1]
        freq += el[1]
        if el[0] < min1:
            min1 = el[0]
        elif el[0] > max1:
            max1 = el[0]
    average = count1 / freq
    rand = random.randint(min1, max1)
    print("ran", rand)

    return rand


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
shipsTable = []


class Car:

    def __init__(self, env, dock, name):
        self.env, self.dock, self.name = env, dock, name
        self.takenTime = 0
        self.arrived = 0
        self.unloading = get_value(unload_time)
        self.env.process(self.run_life_cicle())
        self.taken = 0

    def set_takenTime(self, x):
        self.takenTime = x

    def set_arrived(self, x):
        self.__arrived = x

    def set_unloading(self, x):
        self.__unloading = x

    def get_takenTime(self):
        return self.takenTime

    def get_arrived(self):
        return self.__arrived

    def get_unloading(self):
        return self.__unloading

    def refuel(self):
        self.set_unloading(get_value(unload_time))
        yield self.env.timeout(self.unloading)

    def run_life_cicle(self):
        with self.dock.request() as req:
            self.set_arrived(self.env.now)

            yield req
            print(f"@{self.env.now} - {self.name}: Arrived")

            yield from self.refuel()
            print(f"@{self.env.now} - {self.name}: Refueled")
            self.taken = self.env.now - self.get_arrived()
            self.set_takenTime(self.taken)
            print(self.taken)
            print(" Took", self.get_takenTime())


def generate_cars(env, dock, car_inter_arrival_time):
    i = 0
    while True:
        interarrival_time = random.randint(1, car_inter_arrival_time)
        print("interarrival_time")
        print(interarrival_time)
        yield env.timeout(interarrival_time)

        i += 1
        car = Car(env, dock, name=f"Car {i}")
        print(car.get_takenTime())
        shipsTable.append([i, interarrival_time, car.unloading, car.get_takenTime()])


def main(dock_capacity, time, car_inter_arrival_time):
    env = simpy.Environment()

    dock = simpy.Resource(env, dock_capacity)

    env.process(generate_cars(env, dock, car_inter_arrival_time))

    env.run(until=time)
    # Calculating mean across Columns
    column_mean = np.mean(shipsTable, axis=0)

    print(tabulate(shipsTable, headers=["id", "interarrival_time", "Descarga", "Time in port"]))
    column1_mean = column_mean[1]
    print("media interarrival")
    print(column1_mean)
    column1_mean = column_mean[2]
    print("media descarga")
    print(column1_mean)


if __name__ == "__main__":
    dock_capacity = 1
    time = 200
    car_inter_arrival_time = get_value(unload_time)

    main(dock_capacity, time, car_inter_arrival_time)
