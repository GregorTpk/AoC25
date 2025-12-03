import os, sys

def solve(filename):
    joltage = list()
    with open(filename) as f:
        inp = f.read().strip().split("\n")
    for i, num in enumerate(inp):
        new_num = list()
        index_num = list()

        digits = [int(d) for d in str(num)]
        new_num.append(max(digits[: len(digits) - 11]))
        index_num.append(digits.index(new_num[0]))

        for j in range(1,12):
            new_num.append(max(digits[index_num[-1] + 1: len(digits) - (11 - j)]))
            index_num.append(digits.index(new_num[-1], index_num[-1] + 1))

        print("number: ", num)
        print("new_number: ", new_num)
        whole_num = "".join(str(d) for d in new_num)
        joltage.append(int(whole_num))
    print("joltage list: ", joltage)
    result = sum(joltage)
    return result

# to solve
# 1. find highest digit, so dass noch min. 11 ziffern übrigbleiben , append to list
# 2. finde zweithöchste ziffer nach der höchsten ziffer, so dass noch min. 10 ziffern übrigbleiben
# 3. repeat until 12 digits are found

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