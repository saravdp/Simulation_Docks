# import the module simpy
import matplotlib
import simpy
# import the random component of numpy
from matplotlib import pyplot as plt
from matplotlib.table import table

from numpy import random
from tabulate import tabulate
import pandas as pd
import dataframe_image as dfi

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


# define the triangular distribution
def triangular_distribution(minimum, maximum, median):
    x = random.triangular(minimum, median, maximum)
    return x


# define the source
def source(env):
    i = 1
    while True:
        # start the process
        t = get_value(interarrival_frequency)
        yield env.timeout(t)
        if i <= 25:
            env.process(get_a_coffee(env, coffee_machine, i, t))
            i += 1


# describe the process
def get_a_coffee(env, coffee_machine, name, inter_arrival):
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

    # relese coffee machine for next person
    print('%ds - Ship %d releasing coffee machine' % (env.now, name))
    coffee_machine.release(request)
    time_departure = env.now
    time_spent_in_port = time_departure- arrival
    ships.append([name, inter_arrival, arrival, queueTime, t, time_departure, time_spent_in_port])


prep_data(interarrival_frequency)
prep_data(unload_time)

# create the simpy environment
env = simpy.Environment()

# define the resources
coffee_machine = simpy.Resource(env, capacity=1)

# start the source process
env.process(source(env))

# run the process
env.run(until=10000)

print(tabulate(ships, headers=["ID", "Tempo entre chegadas", "Hora de chegada", "Tempo na fila", "Tempo descarga"
                                "Hora saída", "Tempo no Porto"]))


average_unloading = 0
size = 0
average_arrival = 0
average_queue1 = 0
average_total1 = 0
for i in ships:
    average_arrival += i[1]
    average_queue1 += i[3]
    average_total1 += i[6]
    # descarga
    average_unloading += i[4]
    size += 1
average_arrival = average_arrival  / size
average_queue1 = average_queue1 / size
average_total1 = average_total1 / size
average_unloading = average_unloading /size
ships.append(["", average_arrival, "", average_queue1, average_unloading, "", average_total1])

df = pd.DataFrame(ships)


fig=plt.figure(figsize=(15,10))
ax=plt.subplot(111,frame_on=False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

tb1=table(ax,df.values,colLabels = ("ID", "Tempo entre chegadas", "Hora de chegada", "Tempo na fila", "Tempo descarga",
                                "Hora saída", "Tempo no Porto"),loc='center',colWidths=[0.15, 0.24, 0.2, 0.2, 0.25, 0.22, 0.22])

tb1.auto_set_font_size(False)
tb1.set_fontsize(17)
tb1.scale(1,6)
#plt.show()
plt.savefig('imgs/1cais.png',  bbox_inches='tight', pad_inches=0.1)

fig=plt.figure(figsize=(15,10))
X = range(2, len(ships))
Y = [ships[n][3] for n in X]

plt.plot(X, Y, "-o")
plt.xlabel("Numero de barcos")
plt.ylabel("Tempo de espera")

plt.xticks(X)
plt.draw()
plt.savefig('imgs/tempovsbarcos1.png')