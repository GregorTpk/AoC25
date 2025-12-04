import os, sys

PAPER = "@"
EMPTY = "."

def solve(filename):
    with open(filename, 'r') as f:
        inp = f.read().strip().split("\n")
        inp = [list(line) for line in inp]

    total_accessible_paper = 0
    new_grid = inp
    has_removed_paper = True

    while has_removed_paper == True:
        accessible_paper_per_round, new_grid = accessible_paper(new_grid)
        total_accessible_paper += accessible_paper_per_round                
        if accessible_paper_per_round == 0:
            has_removed_paper = False
    
    return total_accessible_paper  

def accessible_paper(grid):
    # Output: new map, where the accesible papers, and therfore removed papers are marked as x
    
    new_grid = grid
    count_accessible_paper = 0

    for y_index, y in enumerate(grid):
        for x_index, x in enumerate(grid[y_index]):
            if grid[y_index][x_index] == PAPER or grid[y_index][x_index] == "x":
                n_neigbours = count_neighbour(y_index, x_index, grid)
                if n_neigbours < 4:
                    count_accessible_paper += 1
                    new_grid[y_index][x_index] = "x"
    new_grid = [[EMPTY if x == "x" else x for x in lists] for lists in new_grid]
    return count_accessible_paper, new_grid

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
        results = solve(filepath)
        print(results)
    else:
        print("There is no such file")