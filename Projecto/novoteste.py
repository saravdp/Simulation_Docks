import simpy
import random

# Preparação dos dados
def get_value(data):
    count1 = 0
    freq = 0
    min = data[0][0]
    max = data[0][0]
    for el in data:
        count1 += el[0] * el[1]
        freq += el[1]
        if el[0] < min:
            min = el[0]
        elif el[0] > max:
            max = el[0]
    average = count1/freq

    return random.randint(min, max)


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

class Car:
    TIME_REFUEL = get_value(unload_time)

    def __init__(self, env, dock, name):
        self.env, self.dock, self.name = env, dock, name
        self.takenTime = 0
        self.arrived = 0
        self.env.process(self.run_life_cicle())
    def refuel(self):
        yield self.env.timeout(Car.TIME_REFUEL)

    def run_life_cicle(self):
        with self.dock.request() as req:
            self.arrived = self.env.now

            yield req
            print(f"@{self.env.now} - {self.name}: Arrived")

            yield from self.refuel()
            print(f"@{self.env.now} - {self.name}: Refueled")
            self.takenTime = self.env.now - self.arrived
            print(" Took" , self.takenTime)

def generate_cars(env, dock, car_inter_arrival_time):
    i = 0
    while True:
        yield env.timeout(random.randint(1, car_inter_arrival_time))

        i += 1
        Car(env, dock, name=f"Car {i}")



def main(dock_capacity, time, car_inter_arrival_time):

    env = simpy.Environment()

    dock = simpy.Resource(env, dock_capacity)

    env.process(generate_cars(env, dock, car_inter_arrival_time))

    env.run(until=time)


if __name__ == "__main__":

    dock_capacity = 1
    time = 200
    car_inter_arrival_time = 10

    main(dock_capacity, time, car_inter_arrival_time)
