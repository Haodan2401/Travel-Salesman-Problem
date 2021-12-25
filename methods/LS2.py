# Local Search: Neighborhood - 3-opt exchange
# Author: Haodan Tan

import time
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from .utils import cycleValue

# the Three opt swap
def threeOptSwap(route, g, i, j, k):
    A, B, C, D, E, F = route[i - 1], route[i], route[j - 1], route[j], route[k - 1], route[k % len(route)]
    d0 = g[A, B] + g[C, D] + g[E, F]
    d1 = g[A, C] + g[B, D] + g[E, F]
    d2 = g[A, B] + g[C, E] + g[D, F]
    d3 = g[A, D] + g[E, B] + g[C, F]
    d4 = g[F, B] + g[C, D] + g[E, A]

    if d0 > d1:
        route[i:j] = np.flip(route[i:j])
        return -d0 + d1
    elif d0 > d2:
        route[j:k] = np.flip(route[j:k])
        return -d0 + d2
    elif d0 > d4:
        route[i:k] = np.flip(route[i:k])
        return -d0 + d4
    elif d0 > d3:
        route[i:k] = np.concatenate((route[j:k], route[i:j]))
        return -d0 + d3
    return 0

# threeOpt method
def threeOpt(g, cut_off_time, seed):
    # randomly generate the initial route
    routeLength = g.shape[0]
    route = np.arange(routeLength)
    rng = np.random.default_rng(seed)
    rng.shuffle(route)

    trace = [] # distance, time
    start_time = time.time() # start time
    best_distance = cycleValue(route, g)
    while True:
        delta = 0
        # Generate all segments combinations#
        all_segments = []
        for i in range(routeLength):
            for j in range(i + 2, routeLength):
                for k in range(j + 2, routeLength + (i > 0)):
                    all_segments.append((i, j, k))

        for (a, b, c) in all_segments:

            delta += threeOptSwap(route, g, a, b, c)
            new_distance = cycleValue(route, g)
            if new_distance < best_distance:
                t = time.time() - start_time # current running time
                if t > cut_off_time: # time-out
                    return trace, best_route
                best_route = route.copy()
                best_distance = new_distance
                trace.append((best_distance, t))
        if time.time() - start_time > cut_off_time:
            return trace, best_route
        if delta >= 0:
            rng.shuffle(route)


def solve(args):
    # extract the data
    df = pd.read_csv(args.inst, skiprows=5, header=None, sep=' ', usecols=[0, 1, 2])

    # build the graph
    g = squareform(pdist(df.iloc[:-1, 1:].values))

    trace, best_route = threeOpt(g, args.time, args.seed)

    f = open(args.output_path + '.sol', 'w')
    f.write(f'{round(trace[-1][0])}\n{str(list(best_route))[1:-1].replace(" ", "")}')
    f.close()
    
    f = open(args.output_path + '.trace', 'w')
    for each_record in trace:
        f.write(f'{each_record[1]:.2f}, {round(each_record[0])}\n')
    f.close()
