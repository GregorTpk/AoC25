import os, argparse

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

def solve(filename: str) -> tuple[int, int]:
    grid = None
    line_length = None
    with open(filename, "r") as f:
        grid = [list(line.strip()) for line in f.readlines()]
        line_length = len(grid[0])

    first_iteration_removed_count = None
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

        #Update grid
        grid = new_grid
        if first_iteration_removed_count == None:
            first_iteration_removed_count = iteration_removed_count
        total_removed_count += iteration_removed_count

        #End condition
        if iteration_removed_count == 0:
            has_removed_paper = False

        if PRINT_GRID:
            print()

    return first_iteration_removed_count, total_removed_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    parser.add_argument('-l', '--log', action='store_true', default=False, help="Show log. Tuned by --loglevel")
    args = parser.parse_args()

    filepath = args.filepath

    QUIET = args.quiet
    PRINT_GRID = not QUIET and args.log

    if os.path.isfile(filepath):
        first_iteration_removed_count, total_removed_count = solve(filepath)
        if not QUIET:
            print("Removed %s paper rolls after first iteration."%first_iteration_removed_count)
            print("Removed %s paper rolls in total."%total_removed_count)
        else:
            print(first_iteration_removed_count)
            print(total_removed_count)
    else:
        print("There is no such file")
