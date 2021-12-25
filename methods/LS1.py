# Local Search: Neighborhood - 2-opt exchange
# Author: Haodan Tan

import time
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from .utils import cycleValue

# the two opt swap
def twoOptSwap(route, i, j):
    new_route = route.copy()
    new_route[i:j+1] = np.flip(route[i:j+1])
    return new_route


# implement the twoOpt method to find the optimal distance
def twoOpt(graph, cut_off_time, seed):
    # randomly generate the initial route
    routeLength = graph.shape[0]
    route = np.arange(routeLength)
    rng = np.random.default_rng(seed)
    rng.shuffle(route)

    # compute the total distance of exsiting route
    best_distance = cycleValue(route, graph)
    best_route = route

    # repeat until no improvement is made
    trace = [] # distance, time
    start_time = time.time() # start time
    while True:
        improved = False
        for i in range(routeLength-1):
            for j in range(i+1, routeLength):
                new_route = twoOptSwap(route, i, j)
                new_distance = cycleValue(new_route, graph)
                if (new_distance < best_distance):
                    t = time.time() - start_time # current running time
                    if t > cut_off_time: # time-out
                        return trace, best_route
                    best_route = new_route.copy()
                    best_distance = new_distance
                    trace.append((best_distance, t))
                    improved = True
        if time.time() - start_time > cut_off_time:
            return trace, best_route
        route = best_route.copy()
        if improved == False:
            rng.shuffle(route)

# define the main function
def solve(args):
    # extract the data
    df = pd.read_csv(args.inst, skiprows=5, header=None, sep=' ', usecols=[0, 1, 2])

    # build the graph
    g = squareform(pdist(df.iloc[:-1, 1:].values))

    # the total running time of the two opt mthod of local search
    trace, best_route = twoOpt(g, args.time, args.seed)

    f = open(args.output_path + '.sol', 'w')
    f.write(f'{round(trace[-1][0])}\n{str(list(best_route))[1:-1].replace(" ", "")}')
    f.close()
    
    f = open(args.output_path + '.trace', 'w')
    for each_record in trace:
        f.write(f'{each_record[1]:.2f}, {round(each_record[0])}\n')
    f.close()
