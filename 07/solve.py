import os, argparse

TILE_EMPTY = "."
TILE_STARTER = "S"
TILE_SPLITTER = "^"
TILE_BEAM = "|"

def solve(filepath: str) -> tuple[int, int]:
    with open(filepath, "r") as f:
        lines = f.readlines()

    #Directly process first line: Spawn beams
    #Foreach x-pos in a line: Store number of timelines where the beam goes through x-pos
    prev_line = [1 if tile == TILE_STARTER else 0 for tile in lines.pop(0)]

    split_count = 0
    #Assume exactly one starter
    timeline_count = 1

    #Calculate beams from top to bottom
    for line in lines:
        current_beam_count = [0] * len(line)
        for x_pos, (prev_beam_count, current_tile) in enumerate(zip(prev_line, line)):
            if current_tile == TILE_EMPTY:
                #Beam travels downwards
                current_beam_count[x_pos] += prev_beam_count
            elif current_tile == TILE_SPLITTER:
                if prev_beam_count:
                    split_count += 1
                #Split all timelines where the beam goes through splitter at current x_pos
                timeline_count += prev_beam_count
                #Assume no splitters on left/right border
                current_beam_count[x_pos-1] += prev_beam_count
                current_beam_count[x_pos+1] += prev_beam_count
        prev_line = current_beam_count

    return split_count, timeline_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    args = parser.parse_args()

    filepath = args.filepath
    QUIET = args.quiet

    if os.path.isfile(filepath):
        split_count, timeline_count = solve(filepath)
        if not QUIET:
            print("a: %s splits"%split_count)
            print("b: %s different timelines"%timeline_count)
        else:
            print(split_count)
            print(timeline_count)
    else:
        print("There is no such file")
