# com simpy
import simpy
import random

from matplotlib import pyplot as plt

random.seed(123)


# recursos.: porto

ships = []


class Ship:
    T0 = 10  # waitng time
    T1 = 10  # mean eating time
    DT = 1  # time to enter in the port

    def __init__(self, env, cais, id_ship):
        self.env, self.cais, self.id_ship = env, sorted(cais, key=id), id_ship
        self.waiting = 0

        env.process(self.run_life_cicle())

    def get_cais(self):
        start_waiting = self.env.now

        self.log("request first ")
        cais1_rq = self.cais[0].request()
        yield cais1_rq

        self.log("Obtained")
        self.waiting += self.env.now - start_waiting
        self.log("Waited time" + str(self.waiting))
        return cais1_rq

    def release_cais(self, cais1_rq):
        self.cais[0].release(cais1_rq)
        self.log("were released")

    def run_life_cicle(self):
        while True:
            # Waiting time
            waiting_time = random.expovariate(1 / self.T0)
            yield self.env.timeout(waiting_time)

            # entrar no cais
            get_cais_process = self.env.process(self.get_cais())
            cais1_rq = yield get_cais_process

            # descarga
            unload_time = random.expovariate(1 / self.T1)
            yield self.env.timeout(unload_time)

            self.release_cais(cais1_rq)

    def log(self, message):
        print(f"@{self.env.now} Ship {self.id_ship} - {message}")
        pass


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


def simulate(n_ships, time):
    env = simpy.Environment()

    # A fork is a reusable resource that should not be shared.
    cais = [simpy.Resource(env, capacity=1) for i in range(n_ships)]

    # Instantiate ship and assign them
    ships = [Ship(env, (cais[i], cais[(i + 1) % n_ships]), i) for i in range(n_ships)]

    env.run(until=time)
    return sum(ship.waiting for ship in ships) / n_ships


filename = "imgs/ships_2.jpg"


def main(max_ships, time, filename):
    X = range(2, max_ships)
    Y = [simulate(n, time) for n in X]
    print("average")
    print(sum(Y) / len(Y))
    plt.plot(X, Y, "-o")
    plt.xlabel("Number of boats")
    plt.ylabel("Waiting time")

    plt.xticks(X)

    plt.savefig(filename)


if __name__ == "__main__":
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
    prep_data(interarrival_frequency)
    prep_data(unload_time)
    print("interarrival_frequency")
    print(interarrival_frequency)
    max_boats = 20
    time = 1000

    main(max_boats, time, filename)
