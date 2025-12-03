import os, sys

def solve(filename):
    joltage = list()
    with open(filename) as f:
        inp = f.read().strip().split("\n")
    for i, num in enumerate(inp):
        digits = [int(d) for d in str(num)]            
        highest_dig = max(digits)
        if digits.index(highest_dig) == len(digits) - 1:
            highest_dig = sorted(digits)[-2]
        second_highest_dig = max(digits[digits.index(highest_dig) + 1:])
        joltage.append(int(str(highest_dig) + str(second_highest_dig)))
    result = sum(joltage)
    return result


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"

    if os.path.isfile(filepath):
        results = solve(filepath)
        print(results)
    else:
        print("There is no such file")