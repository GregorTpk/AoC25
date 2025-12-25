import os, argparse

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

    for tree in trees:

        a, b = tree[0]
        area = a*b

        presents = tree[1]

        sum_presents = sum(presents)
        if sum_presents <= area/9:
            counter += 1
    return counter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    args = parser.parse_args()

    filepath = args.filepath
    QUIET = args.quiet

    if os.path.isfile(filepath):
        result = solve(filepath)
        msg = ("%s solvable regions (probably)"%result if not QUIET else result)
        print(msg)
    else:
        print("There is no such file")
