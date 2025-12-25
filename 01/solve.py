import os, argparse

DIRECTIONS = {"L":-1, "R":1}
DIAL_START_POSITION = 50

def solve(filepath: str) -> tuple[int, int]:
    pointing_at_zero_count = 0
    passing_zero_count = 0
    dial = DIAL_START_POSITION
    with open(filepath, "r") as f:
        for l in f.readlines():
            l = l.strip()
            direction = DIRECTIONS[l[0]]
            step = int(l[1:])

            # Count full revolutions of the dial
            passing_zero_count += abs(step // 100)

            # Only consider remaining step
            step %= 100

            newdial = dial + step*direction

            # Pointing at zero during remaining steps
            if dial != 0 and (newdial <= 0 or newdial >= 100):
                passing_zero_count += 1

            dial = newdial % 100

            pointing_at_zero_count += dial == 0
    return pointing_at_zero_count, passing_zero_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    args = parser.parse_args()

    filepath = args.filepath

    QUIET = args.quiet

    if os.path.isfile(filepath):
        pointing_at_zero_count, passing_zero_count = solve(filepath)

        if not QUIET:
            print("a: Pointed at zero after rotation %s times."%pointing_at_zero_count)
            print("b: Passed zero %s times."%passing_zero_count)
        else:
            print(pointing_at_zero_count)
            print(passing_zero_count)
    else:
        print("There is no such file")
