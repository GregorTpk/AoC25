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
        #a = int(tree[0].split("x")[0]) // 3
        #b = int(tree[0].split("x")[1]) // 3
        a, b = tree[0]
        print (a,b)
        area = a*b

        presents = tree[1]

       # presents = np.to_numeric(presents)

        sum_presents = sum(presents)
        print(sum_presents)
        if sum_presents < area/9:
            counter += 1
    print(counter)
    
    print(trees)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"

    if os.path.isfile(filepath):
        results = solve(filepath)
        print(results)
    else:
        print("There is no such file")