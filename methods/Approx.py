# Approximation: Minimum Spaning Tree approximation
# Author: Chengrui Li

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
import time
from .utils import cycleValue

def prim(g):
    '''
    use prim algorithm to generate minimum spanning tree
    '''
    n = g.shape[0]
    tree = g.copy()
    mst = np.inf * np.ones((n, n))
    np.fill_diagonal(tree, np.inf)
    selected = np.zeros(n, dtype=bool)
    selected[0] = True
    for i in range(1, n):
        from_idx, idx = np.divmod(np.argmin(tree[selected]), n)
        from_idx = np.where(selected)[0][from_idx]
        selected[idx] = True
        tree[selected, idx], tree[idx, selected] = np.inf, np.inf
        mst[from_idx, idx], mst[idx, from_idx] = g[from_idx, idx], g[idx, from_idx]
    return mst

def depthFirstSearch(g, root):
    '''
    use depth first search to traverse an MST to obtain a TSP tour
    '''
    visited = []
    stack = [root] # use stack to do DFS
    while len(stack) != 0:
        curr = stack.pop()
        if curr not in visited:
            visited.append(curr)
            stack.extend(np.where(g[curr] != np.inf)[0])
    return visited

def approx(filename, output_path):
    df = pd.read_csv(filename, skiprows=5, header=None, sep=' ', usecols=[0, 1, 2]) # read file
    g = squareform(pdist(df.iloc[:-1, 1:].values)) # form adjacency matrix
    np.fill_diagonal(g, np.inf)

    best_value = np.inf
    start = time.time() # start time
    mst = prim(g) # build MST
    for i in range(g.shape[0]):
        # start from every node and use DFS to traverse the MST
        tour_list = depthFirstSearch(mst, i)
        value = cycleValue(tour_list, g)
        if value < best_value:
            best_value = value
            best_tour_list = tour_list
    end = time.time()

    # save file
    f = open(output_path + '.sol', 'w')
    f.write(f'{round(best_value)}\n{str(best_tour_list)[1:-1].replace(" ", "")}')
    f.close()
    
    f = open(output_path + '.trace', 'w')
    f.write(f'{end - start:.2f}, {round(best_value)}')
    f.close()

def solve(args):
    approx(args.inst, args.output_path)
