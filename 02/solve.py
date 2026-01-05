import os, argparse

# 1. Compute all numbers in the range
# 2. For each number in the range, get number of possible substrings (= get divisors of length of string)
# 3. For each divisor, get all substrings of that length
# 4. Check if number is made up of repeated substrings
# 5. If TRUE, add to invalid_id list

def get_all_divisors(n):
    divisors = list()
    for i in range(1, n + 1):
        if n % i == 0 and i != n:
            divisors.append(i)
    return divisors

def solve_subproblem(intervals, get_divisors):
    invalid_id = list()
    #Iterate over all ids in the given intervals
    for start, end in intervals:
        for num in range(start, end + 1):
            length_of_num = len(str(num))
            #Iterate relevant divisors of current id
            for divisor in get_divisors(length_of_num):
                #Check whether current id is the repetition of its prefix
                substring = str(num)[:divisor]
                if substring * (length_of_num // divisor) == str(num):
                    invalid_id.append(num)

    invalid_id = set(invalid_id)
    sum_invalid_id = sum(invalid_id)
    return sum_invalid_id

def solve(filename):
    with open(filename) as f:
        intervals = [[int(border) for border in interv.split("-")] for interv in f.read().strip().split(",")]

    #Subproblem a: Only consider the divisor n//2 of even n
    twofold_repeating_inv_ids = solve_subproblem(intervals, get_divisors=lambda n: (n//2,) if n%2 == 0 else ())
    #Subproblem b: Consider all divisors
    manifold_repeating_inv_ids = solve_subproblem(intervals, get_divisors=get_all_divisors)

    return twofold_repeating_inv_ids, manifold_repeating_inv_ids

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    parser.add_argument('-l', '--log', action='store_true', default=False, help="Show log. Tuned by --loglevel")
    parser.add_argument('-L', '--log-level', type=int, default=None, help="The higher the --log-level=0,1,2, the more details. --loglevel=-1 is log all.")
    args = parser.parse_args()

    filepath = args.filepath

    QUIET = args.quiet

    if os.path.isfile(filepath):
        twofold_repeating_inv_ids, manifold_repeating_inv_ids = solve(filepath)
        if not QUIET:
            print("%s invalid ids with twofold repetition."%twofold_repeating_inv_ids)
            print("%s invalid ids with manifold repetition."%manifold_repeating_inv_ids)
        else:
            print(twofold_repeating_inv_ids)
            print(manifold_repeating_inv_ids)
    else:
        print("There is no such file")
