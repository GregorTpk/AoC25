import os, sys 
import numpy as np
import pandas as pd

def solve(filename): 
    trees = list()
    counter = 0

    with open(filename) as f:
        read_trees = False 
        for i, line in enumerate(f): 
            if "x" in line:
                read_trees = True
            if read_trees:
                raw_tree = line.strip().split(": ")
                trees.append([[int(dim) for dim in raw_tree[0].split("x")], 
                              [int(present_count) for present_count in raw_tree[1].strip().split(" ")]])

    for i, tree in enumerate(trees):

        a, b = tree[0]
        area = a*b

        presents = tree[1]

        sum_presents = sum(presents)
        if sum_presents <= area/9:
            counter += 1
    return counter
    
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input2.txt"

    if os.path.isfile(filepath):
        results = solve(filepath)
        print(results)
    else:
        print("There is no such file")