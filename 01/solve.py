import os, sys

DIRECTIONS = {"L":-1, "R":1}

def solve(filepath):
    result1 = 0
    result2 = 0
    dial = 50
    with open(filepath, "r") as f:
        for l in f.readlines():
            l = l.strip()
            direction = l[0]
            step = int(l[1:])

            # Count full revolutions of the dial
            result2 += abs(step // 100)

            # Only consider remaining step
            step %= 100

            newdial = dial + step*DIRECTIONS[direction]

            # Pointing at zero during remaining steps
            if dial != 0 and (newdial <= 0 or newdial >= 100):
                result2 += 1

            dial = newdial % 100

            result1 += dial == 0
    return result1, result2

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"

    if os.path.isfile(filepath):
        results = solve(filepath)

        print("Result 1: ", results[0])
        print("Result 2: ", results[1])
    else:
        print("There is no such file")
