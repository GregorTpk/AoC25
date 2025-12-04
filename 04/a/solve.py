import os, sys

NEIGHBOR_LIMIT = 4

PAPER = "@"
SPACE = "."

def update_neighbors(neighbor_counts, i, only_neighbors):
    if i > 0:
        neighbor_counts[i-1] += 1
    if not only_neighbors:
        neighbor_counts[i] += 1
    if i < len(neighbor_counts)-1:
        neighbor_counts[i+1] += 1

count_valid_tiles = lambda line_counts: sum(map(lambda n_count: n_count < NEIGHBOR_LIMIT, line_counts))

def count_valid_tiles(line, line_neighbor_counts):
    answer_line = ""

    s = 0
    for tile, n_count in zip(line, line_neighbor_counts):
        if tile == PAPER and n_count < NEIGHBOR_LIMIT:
            answer_line += "x"
            s += 1
        else:
            answer_line += tile
    print(answer_line)
    return s

def solve(filename):
    grid = None
    line_length = None
    with open(filename, "r") as f:
        grid = [list(line.strip()) for line in f.readlines()]
        line_length = len(grid[0])

    valid_tile_sum = 0

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
            valid_tile_sum += count_valid_tiles(prev_line, prev_line_neigbor_counts)

        prev_line = line
        prev_line_neigbor_counts = line_neighbor_counts
        line_neighbor_counts = next_line_neighbor_counts
        next_line_neighbor_counts = [0] * line_length

    valid_tile_sum += count_valid_tiles(prev_line, prev_line_neigbor_counts)

    return valid_tile_sum


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"

    if os.path.isfile(filepath):
        print(solve(filepath))
    else:
        print("There is no such file")
