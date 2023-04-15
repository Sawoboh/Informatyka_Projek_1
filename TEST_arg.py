# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 11:23:35 2023

@author: Sawob
"""

import argparse

"""
def process_args():
    parser = argparse.ArgumentParser(prog='my-awesome-program')
    parser.add_argument('--value1', dest='value1', type=int)
    parser.add_argument('--value2', dest='value2', type=int)

    args = parser.parse_args()
    return args


def main():
    args = process_args()
    args = vars(args)

    my_value_1 = args['value1']
    my_value_2 = args['value2']
    print('%s, %s' % (my_value_1, my_value_2))


if __name__ == '__main__':
    main()
"""

parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print(f"the square of {args.square} equals {answer}")
elif args.verbosity == 1:
    print(f"{args.square}^2 == {answer}")
else:
    print(answer)