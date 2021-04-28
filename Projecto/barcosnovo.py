# import the module simpy
import simpy
# import the random component of numpy
from numpy import random

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
        t = exponential_distribution(get_value(interarrival_frequency))
        yield env.timeout(t)
        env.process(get_a_coffee(env, coffee_machine, i))
        i += 1


# describe the process
def get_a_coffee(env, coffee_machine, name):
    # walk to kitchen
    print('%ds - Person %d walking to kitchen' % (env.now, name))
    t = get_value(unload_time)
    yield env.timeout(t)
    print('%ds - Person %d arrived at kitchen' % (env.now, name))

    # request coffee machine
    print('%ds - Person %d requesting use of coffee machine' % (env.now, name))
    request = coffee_machine.request()
    yield request
    print('%ds - Person %d seized coffee machine' % (env.now, name))

    # make coffee
    print('%ds - Person %d making coffee' % (env.now, name))
    t = triangular_distribution(30, 120, 45)
    yield env.timeout(t)
    print('%ds - Person %d finished making coffee' % (env.now, name))

    # relese coffee machine for next person
    print('%ds - Person %d releasing coffee machine' % (env.now, name))
    coffee_machine.release(request)

prep_data(interarrival_frequency)
prep_data(unload_time)

# create the simpy environment
env = simpy.Environment()

# define the resources
coffee_machine = simpy.Resource(env, capacity=1)

# start the source process
env.process(source(env))

# run the process
env.run(until=300)