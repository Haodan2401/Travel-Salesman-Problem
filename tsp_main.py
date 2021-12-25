import os
import argparse

def parse_arguments():
    '''
    parse the four arguments
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-inst', type=str, required=True
    )

    parser.add_argument(
        '-alg', choices=['BnB', 'Approx', 'LS1', 'LS2'], required=True
    )

    parser.add_argument(
        '-time', type=int, required=True
    )

    parser.add_argument(
        '-seed', type=int, default=None
    )

    parser.add_argument(
        '-bnb_bound', choices=['reduce_matrix', 'smallest_edge'], default='reduce_matrix'
    )

    args = parser.parse_args()
    return args


def dispatch_args(args):

    def generate_output_path(args):
        '''
        generate output path for writting the solution and trace file
        '''
        inst = args.inst
        city_file = os.path.split(inst)[1]
        city_name = os.path.splitext(city_file)[0]
        file_name = "{}_{}_{}".format(
            city_name, args.alg, args.time)
        if args.seed is not None:
            file_name += "_" + str(args.seed)
        if args.bnb_bound == 'smallest_edge':
            file_name += "_se"
        return "output/" + file_name
    
    output_path = generate_output_path(args)
    args.output_path = output_path
    if not os.path.isdir("output"):
        os.makedirs("output")

    import importlib
    try:
        method_module = importlib.import_module(f'methods.{args.alg}')
    except:
        print(f"Algorithm {args.alg} is not found in methods/. Check code.")

    method_module.solve(args)



if __name__ == '__main__':
    args = parse_arguments()
    dispatch_args(args)

