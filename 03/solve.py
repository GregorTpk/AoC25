import os, argparse

#Number of considered batteries in both subproblems respectively
BATTERY_COUNTS = (2, 12)

def solve_subproblem(banks, battery_count):
    """Maximize joltage by choosing battery_count many batteries per bank."""

    joltage = list()
    for num in banks:
        new_num = list()
        index_num = list()

        digits = [int(d) for d in str(num)]
        largest_digit_idx = -1

        #Iteratively choose batteries from highest to lowest significance
        #Always choose the battery with max joltage such that enough batteries remain
        for i in range(battery_count):
            largest_digit = max(digits[largest_digit_idx + 1 : len(digits) - battery_count + i + 1])
            largest_digit_idx = digits.index(largest_digit, largest_digit_idx+1)
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
