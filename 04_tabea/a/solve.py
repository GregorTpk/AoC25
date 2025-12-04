import os, sys, time

PAPER = "@"
EMPTY = "."

def solve(filename):
    with open(filename, 'r') as f:
        inp = f.read().strip().split("\n")
        inp = [list(line) for line in inp]

    accessibility = inp

    count_accessible_paper = 0
    for y_index, y in enumerate(inp):
        for x_index, x in enumerate(inp[y_index]):
            if inp[y_index][x_index] == PAPER or inp[y_index][x_index] == "x":
                n_neigbours = count_neighbour(y_index, x_index, inp)
                if n_neigbours < 4:
                    count_accessible_paper += 1
                    accessibility[y_index][x_index] = "x"
    return count_accessible_paper

def count_neighbour(i,j,grid):
    n_neigbours = 0
    directions = [  (-1, -1),   (-1, 0),    (-1, 1),
                    (0, -1),                (0, 1),
                    (1, -1),    (1, 0),     (1, 1)]
    for d in directions:
        di, dj = d
        ni, nj = i + di, j + dj
        if 0 <= ni < len(grid) and 0 <= nj < len(grid[i]):
            if grid[ni][nj] == PAPER or grid[ni][nj] == "x":
                n_neigbours += 1
    return n_neigbours

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"

    if os.path.isfile(filepath):
        t1 = time.time()
        results = solve(filepath)
        t2 = time.time()
        print("Runtime: ", t2-t1)
        print(results)
    else:
        print("There is no such file")