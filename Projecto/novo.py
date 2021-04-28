from simpy import *
import random

maxNumber = 20      # Max number of customers
maxTime = 400.0     # Rumtime limit
timeInDock = 20.0   # Mean time in bank
arrivalMean = 10.0  # Mean of arrival process
seed = 123       # Seed for simulation


def Customer(env, name, counters):
    arrive = env.now
    Qlength = [NoInSystem(counters[i]) for i in range(len(counters))]
    print("%7.4f %s: Here I am. %s" % (env.now, name, Qlength))
    for i in range(len(Qlength)):
        if Qlength[i] == 0 or Qlength[i] == min(Qlength):
            choice = i  # the chosen queue number
            break
    with counters[choice].request() as req:
        # Wait for the counter
        yield req
        wait = env.now - arrive
        # We got to the counter
        print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        tib = random.expovariate(1.0 / timeInDock)
        yield env.timeout(tib)
        print('%7.4f %s: Finished' % (env.now, name))


def NoInSystem(R):
    """Total number of customers in the resource R"""
    return max([0, len(R.put_queue) + len(R.users)])


def Source(env, number, interval, counters):
    for i in range(number):
        c = Customer(env, 'Customer%02d' % i, counters)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


# Setup and start the simulation
print('Bank with multiple queues')
random.seed(seed)
env = Environment()

counters = [Resource(env), Resource(env)]
env.process(Source(env, maxNumber, arrivalMean, counters))
env.run(until=maxTime)