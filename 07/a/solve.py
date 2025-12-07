import os, sys

OUTPUT = False

TILE_EMPTY = "."
TILE_START = "S"
TILE_SPLITTER = "^"
TILE_BEAM = "|"

def solve(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    split_count = 0

    prev_line = list(lines.pop(0))
    if OUTPUT: print("".join(prev_line).strip())

    for line in lines:
        new_line = list(line)
        for pos, (prev_tile, tile) in enumerate(zip(prev_line, line)):
            if prev_tile == TILE_START:
                new_line[pos] = TILE_BEAM
            elif prev_tile == TILE_BEAM:
                if tile == TILE_EMPTY:
                    new_line[pos] = TILE_BEAM
                elif tile == TILE_SPLITTER:
                    split_count += 1

                    if pos-1 >= 0 and new_line[pos-1] == TILE_EMPTY:
                        new_line[pos-1] = TILE_BEAM
                    if pos+1 <= len(line)-1 and new_line[pos+1] == TILE_EMPTY:
                        new_line[pos+1] = TILE_BEAM

        if OUTPUT: print("".join(new_line).strip())
        prev_line = new_line

    return split_count

if __name__ == "__main__":
    (filepath := sys.argv[1]) if len(sys.argv) >= 2 else (filepath := "input.txt")
    print(solve(filepath)) if os.path.isfile(filepath) else print("There is no such file")
