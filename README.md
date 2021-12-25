# Introduction
This is the source code for final project of CSE 6140. Our group members are Chengrui Li, Rui Feng, Haodan Tan.

# Run the code
`python tsp_main.py -inst <filename> -alg [BnB | Approx | LS1 | LS2] -time <cutoff_in_seconds> [-seed <random_seed>] [-bnb_bound reduce_matrix | smallest_edge]`
* -inst: the filepath of a single input instance
* -alg: the method to use:
    * BnB: branch and bound
    * Approx: MST approximation algorithm
    * LS1: the first local search algorithm, neighborhood 2-opt
    * LS2: the second local search algorithm, neighborhood 3-opt
* -time: the cut-off time in seconds
* -seed: the random seed only used for `LS1` or `LS2`
* -bnb_bound: the lower bound calculation for branch and bound. Default = reduce_matrix.

Two output files `.sol` and `.trace` will be generated in the folder `output`.


# Code Structure
**/**
tsp_main.py  // main file. reads input argument and dispatch arguments to specified algorithm. 
**/method**
*  __init__.py
*  Approx.py // approximation algorithm implementation. 
*  LS1.py    // 2-opt local search. 
*  LS2.py    // 3-opt local search.
*  utils.py  // helper functions.
* **/method/BnB**      
    *    __init__.py  // module file. defines solve function to dispatch arguments to one of the lower bound implementations.
    *   reduce_matrix.py // defines lower bound implementation with reduce_matrix.
    *   smallest_edge.py // defines lower bound implementation with smallest_edge.py.
    *   utils.py         // helper functions for BnB, including IO and bound calculations.  


Each algorithm file has a unified IO structure. The main file seeks to call the solve(args) function in the algorithm file, where args are input arguments. For BnB, the solve function is defined in __init__.py, which directs the arguments to either of the two lower bound implementations.

