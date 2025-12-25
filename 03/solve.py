import os, argparse

BATTERY_COUNTS = (2, 12)

def solve_subproblem(banks, battery_count):
    joltage = list()
    for num in banks:
        new_num = list()
        index_num = list()

        digits = [int(d) for d in str(num)]
        largest_digt_idx = -1

        # to solve
        # 1. find highest digit, so dass noch min. 11 ziffern übrigbleiben , append to list
        # 2. finde zweithöchste ziffer nach der höchsten ziffer, so dass noch min. 10 ziffern übrigbleiben
        # 3. repeat until 12 digits are found
        for i in range(battery_count):
            largest_digit = max(digits[largest_digt_idx + 1 : len(digits) - battery_count + i + 1])
            largest_digt_idx = digits.index(largest_digit, largest_digt_idx+1)
            new_num.append(largest_digit)

        whole_num = "".join(str(d) for d in new_num)
        joltage.append(int(whole_num))
    result = sum(joltage)
    return result

def solve(filename):
    with open(filename) as f:
        banks = f.read().strip().split("\n")

    return [solve_subproblem(banks, battery_count) for battery_count in BATTERY_COUNTS]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    args = parser.parse_args()

    filepath = args.filepath

    QUIET = args.quiet

    if os.path.isfile(filepath):
        results = solve(filepath)
        if not QUIET:
            msg = lambda total_jolt, battery_count: "Max total output joltage of %s when using %s batteries per bank."%(total_jolt, battery_count)
        else:
            msg = lambda total_jolt, _: total_jolt
        for total_jolt, battery_count in zip(results, BATTERY_COUNTS):
            print(msg(total_jolt, battery_count))
    else:
        print("There is no such file")
