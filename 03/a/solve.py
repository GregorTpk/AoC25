import os, sys

def solve(filepath):

    banks = None
    with open(filepath, "r") as f:
        banks = [[int(digit) for digit in line.strip()] for line in f.readlines()]

    joltages = []

    if banks != None:
        for bank in banks:
            key_func = lambda idx_joltage_pair: idx_joltage_pair[1]

            idx1, jolt1 = max(enumerate(bank[:-1]), key=key_func)
            idx2, jolt2 = max(enumerate(bank[idx1+1:]), key=key_func)

            joltage = 10*jolt1 + jolt2

            joltages.append(joltage)

    return sum(joltages)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"

    if os.path.isfile(filepath):
        result = solve(filepath)

        print(result)
    else:
        print("There is no such file")
