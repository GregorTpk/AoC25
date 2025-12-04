import os, sys
import time

PRINT_GRID = True

#NEIGHBOR_LIMIT = 4
#ACCESSIBLE_PAPER_NEIGHBOR_COUNT = [0, 1, 2, 3]
#Game of Life rules
ACCESSIBLE_PAPER_NEIGHBOR_COUNT = [0, 1, 4, 5, 6, 7, 8]
SPAWN_PAPER_NEIGHBOR_COUNT = [3]

PAPER = "O"
SPACE = "."
ACCESSIBLE_PAPER = "O" # "x"

def update_neighbors(neighbor_counts, i, only_neighbors):
    if i > 0:
        neighbor_counts[i-1] += 1
    if not only_neighbors:
        neighbor_counts[i] += 1
    if i < len(neighbor_counts)-1:
        neighbor_counts[i+1] += 1

count_valid_tiles = lambda line_counts: sum(map(lambda n_count: n_count < NEIGHBOR_LIMIT, line_counts))

def count_valid_tiles(line, line_neighbor_counts):
    if PRINT_GRID:
        answer_line = ""

    s = 0
    for tile, n_count in zip(line, line_neighbor_counts):
        if tile == PAPER and n_count in ACCESSIBLE_PAPER_NEIGHBOR_COUNT: #n_count < NEIGHBOR_LIMIT:
            s += 1
            if PRINT_GRID:
                answer_line += ACCESSIBLE_PAPER
        elif PRINT_GRID:
            answer_line += tile
    if PRINT_GRID:
        print(answer_line)
    return s

def remove_paper(line, line_neighbor_counts):
    newline = []
    for tile, n_count in zip(line, line_neighbor_counts):
        if tile == PAPER and n_count in ACCESSIBLE_PAPER_NEIGHBOR_COUNT: #n_count < NEIGHBOR_LIMIT:
            newline.append(SPACE)
        elif tile == SPACE and n_count in SPAWN_PAPER_NEIGHBOR_COUNT:
            newline.append(PAPER)
        else:
            newline.append(tile)
    return newline

def solve(filename):
    grid = None
    line_length = None
    with open(filename, "r") as f:
        grid = [list(line.strip()) for line in f.readlines()]
        line_length = len(grid[0])

    total_removed_count = 0
    has_removed_paper = True

    while has_removed_paper:
        new_grid = []
        iteration_removed_count = 0

        prev_line = None
        prev_line_neigbor_counts = None
        line_neighbor_counts = [0] * line_length
        next_line_neighbor_counts = [0] * line_length
        for line in grid:
            for i, tile in enumerate(line):
                if tile == PAPER:
                    if prev_line_neigbor_counts != None:
                        update_neighbors(prev_line_neigbor_counts, i, only_neighbors=False)

                    update_neighbors(line_neighbor_counts, i, only_neighbors=True)

                    update_neighbors(next_line_neighbor_counts, i, only_neighbors=False)

            if prev_line_neigbor_counts != None:
                iteration_removed_count += count_valid_tiles(prev_line, prev_line_neigbor_counts)
                new_grid.append(remove_paper(prev_line, prev_line_neigbor_counts))

            prev_line = line
            prev_line_neigbor_counts = line_neighbor_counts
            line_neighbor_counts = next_line_neighbor_counts
            next_line_neighbor_counts = [0] * line_length

        iteration_removed_count += count_valid_tiles(prev_line, prev_line_neigbor_counts)
        new_grid.append(remove_paper(prev_line, prev_line_neigbor_counts))

        grid = new_grid
        total_removed_count += iteration_removed_count

        if iteration_removed_count == 0:
            has_removed_paper = False

        if PRINT_GRID:
            print()

        time.sleep(0.075)

    return total_removed_count


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "gol_glider_gun.txt" #"input.txt"

    if os.path.isfile(filepath):
        starttime = time.time()
        print(solve(filepath))
        print(time.time()-starttime)
    else:
        print("There is no such file")
