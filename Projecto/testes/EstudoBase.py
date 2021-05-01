import random
import matplotlib.pyplot as plt
from pprint import pprint

random.seed(123)


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


def main(num_boats, interarrival_frequency, unload_time):
    prep_data(interarrival_frequency)
    prep_data(unload_time)

    time_arrival, time_to_unload, time_in_queue, time_in_port = [], [], [], []
    time_arrival_sum, leaving_time = 0, 0

    print(f"Boat\t|A.t\t|Arr.\t|Queue\t|Unload\t|Leav.\t|Port")

    for i in range(num_boats):
        # obter valores para o tempo de chegada
        time_arrival.append(get_value(interarrival_frequency))
        time_arrival_sum += time_arrival[-1]

        # obter valores para o tempo na fila
        time_in_queue.append(leaving_time - time_arrival_sum if leaving_time - time_arrival_sum > 0 else 0)

        # obter valores para o tempo de descarregar
        time_to_unload.append(get_value(unload_time))

        leaving_time = time_arrival_sum + time_in_queue[-1] + time_to_unload[-1]

        time_in_port.append(leaving_time - time_arrival_sum)

        print(
            f"{i}\t|{time_arrival[-1]}\t|{time_arrival_sum}\t|{time_in_queue[-1]}\t|{time_to_unload[-1]}\t|{leaving_time}\t|{time_in_port[-1]}"
        )

    if num_boats:
        print("\nAvg. Arrivals:", sum(time_arrival) / num_boats)
        print("Avg. Unload:", sum(time_to_unload) / num_boats)
        print("Avg. Queue:", sum(time_in_queue) / num_boats)
        print("Avg. Port:", sum(time_in_port) / num_boats)


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
    number_of_boats = 25
    main(number_of_boats, interarrival_frequency, unload_time)
