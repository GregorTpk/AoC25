import os, sys

TILE_EMPTY = "."
TILE_STARTER = "S"
TILE_SPLITTER = "^"
TILE_BEAM = "|"

def solve(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    #Directly process first line: Spawn beams
    prev_line = [1 if tile == TILE_STARTER else 0 for tile in lines.pop(0)]
    #Assume exactly one starter
    timeline_count = 1

    for line in lines:
        new_line = [0] * len(line)
        for pos, (prev_beams, tile) in enumerate(zip(prev_line, line)):
            if tile == TILE_EMPTY:
                new_line[pos] += prev_beams
            elif tile == TILE_SPLITTER:
                timeline_count += prev_beams
                new_line[pos-1] += prev_beams
                new_line[pos+1] += prev_beams
        prev_line = new_line
    return timeline_count

if __name__ == "__main__":
    (filepath := sys.argv[1]) if len(sys.argv) >= 2 else (filepath := "input.txt")
    print(solve(filepath)) if os.path.isfile(filepath) else print("There is no such file")
