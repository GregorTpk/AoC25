import os, sys

PRINT_GRID = False

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
    if PRINT_GRID:
        answer_line = ""

    s = 0
    for tile, n_count in zip(line, line_neighbor_counts):
        if tile == PAPER and n_count < NEIGHBOR_LIMIT:
            s += 1
            if PRINT_GRID:
                answer_line += "x"
        elif PRINT_GRID:
            answer_line += tile
    if PRINT_GRID:
        print(answer_line)
    return s

def remove_paper(line, line_neighbor_counts):
    newline = []
    for tile, n_count in zip(line, line_neighbor_counts):
        if tile == PAPER and n_count < NEIGHBOR_LIMIT:
            newline.append(SPACE)
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

    return total_removed_count


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"

    if os.path.isfile(filepath):
        print(solve(filepath))
    else:
        print("There is no such file")
