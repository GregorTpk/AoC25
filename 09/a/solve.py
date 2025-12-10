import os, sys

def solve(filepath):
    with open(filepath, "r") as f:
        tiles = [[int(comp) for comp in pos.split(",")] for pos in f.readlines()]

    max_area = 0

    for i, p1 in enumerate(tiles):
        for p2 in tiles[i+1:]:
            area = ((abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1))
            if area > max_area:
                max_area = area

    return max_area

if __name__ == "__main__":
    (filepath := sys.argv[1]) if len(sys.argv) >= 2 else (filepath := "input.txt")
    print(solve(filepath)) if os.path.isfile(filepath) else print("There is no such file")
