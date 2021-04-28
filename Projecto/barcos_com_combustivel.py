# import the module simpy
import simpy
# import the random component of numpy
from numpy import random
from tabulate import tabulate
import pandas as pd

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
fueling_time = [
    [6, 4],
    [7, 7],
    [8, 16],
    [9, 37],
    [10, 22],
    [11, 9],
    [12, 5]
]
ships = []
def get_value(data):
    value = random.random()
    for a in data:
        if a[3] > value:
            return a[0]
    return data[-1][0]



# Preparação dos dados
def prep_data(data):
    sum = 0

    for a in interarrival_frequency:
        sum += a[1]

    for i in range(len(data)):
        data[i].append(data[i][1] / sum)
        data[i].append(data[i][2] + data[i - 1][3] if i > 0 else data[i][2])


# define the exponential distribution
def exponential_distribution(mean):
    x = random.exponential(mean)
    return x


# define the source
def source(env):
    i = 1
    while True:
        # start the process
        t = get_value(interarrival_frequency)
        yield env.timeout(t)
        if i <= 25:
            env.process(get_a_coffee(env, coffee_machine, fueling_station, i, t))
            i += 1


# describe the process
def get_a_coffee(env, coffee_machine, fueling_station, name, inter_arrival):
    # walk to kitchen
    arrival = env.now
    # print('%ds - Person %d walking to kitchen' % (env.now, name))
    # t = get_value(unload_time)
    # yield env.timeout(t)
    print('%ds - Ship %d arrived at kitchen' % (env.now, name))

    # request coffee machine
    print('%ds - Ship %d requesting use of coffee machine' % (env.now, name))
    request = coffee_machine.request()
    req_time = env.now
    yield request
    obtained_time = env.now
    queueTime = obtained_time - req_time

    # print('%ds - Person %d seized coffee machine' % (env.now, name))

    # make coffee
    print('%ds - Ship %d making coffee' % (env.now, name))
    t = get_value(unload_time)
    yield env.timeout(t)
    print('%ds - Ship %d finished making coffee' % (env.now, name))

    # release coffee machine for next person
    print('%ds - Ship %d releasing coffee machine' % (env.now, name))
    coffee_machine.release(request)

    arrival_station = env.now
    request_station = fueling_station.request()
    req_arrival_station = env.now
    yield request_station
    obtained_time_station = env.now
    queue_time_station = obtained_time_station - req_arrival_station
    # tempo abastecer
    t_fueling = get_value(fueling_time)
    yield env.timeout(t_fueling)


    fueling_station.release(request_station)
    time_departure = env.now
    time_spent_in_port = time_departure- arrival
    ships.append([name, inter_arrival, arrival, queueTime, t, arrival_station, queue_time_station, t_fueling, time_departure, time_spent_in_port])


prep_data(interarrival_frequency)
prep_data(unload_time)
prep_data(fueling_time)
# create the simpy environment
env = simpy.Environment()

# define the resources
coffee_machine = simpy.Resource(env, capacity=1)
fueling_station = simpy.Resource(env, capacity=1)

# start the source process
env.process(source(env))

# run the process
env.run(until=10000)

print(tabulate(ships, headers=["ID", "Tempo entre chegadas", "Hora de chegada", "Tempo na fila", "Tempo descarga",
                               "arrival_station", "queue_time_station", "t_fueling"
                                "Hora saída", "Tempo no Porto"]))




df = pd.DataFrame(ships)

pdf_filepath = "novotestepdf.pdf"
demo_df = pd.DataFrame(df, columns = ("ID", "Tempo entre chegadas", "Hora de chegada", "Tempo na fila", "Tempo descarga"
                                "Hora saída", "Tempo no Porto"))


