# functions that is common for all methods
# Author: Chengrui Li
import numpy as np

def cycleValue(tour_list, g):
    '''
    calculate the total distance for the route
    '''
    tour_list
    value = 0
    for i in range(len(tour_list) - 1):
        value += g[tour_list[i], tour_list[i + 1]]
    return value + g[tour_list[-1], tour_list[0]]
