import os, sys

# 1. Compute all numbers in the range
# 2. For each number in the range, get number of possible substrings (= get divisors of length of string)
# 3. For each divisor, get all substrings of that length
# 4. Check if number is made up of repeated substrings
# 5. If TRUE, add to invalid_id list

def get_divisors(n):
    divisors = list()
    for i in range(1, n + 1):
        if n % i == 0 and i != n:
            divisors.append(i)
    return divisors

def solve(filename):
    with open(filename) as f:
        inp = f.read().strip().split(",")

    invalid_id = list()

    for i, check_id in enumerate(inp):
        start = int(check_id.split('-')[0])
        end = int(check_id.split('-')[1])
        for j, num in enumerate(range(start, end + 1)):
            length_of_num = len(str(num))
            for k, divisor in enumerate(get_divisors(length_of_num)):
                substring = str(num)[:divisor]
                if substring * (length_of_num // divisor) == str(num):
                    invalid_id.append(num)

    invalid_id = set(invalid_id)
    sum_invalid_id = sum(invalid_id)
    return sum_invalid_id

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
