import os, sys, argparse

type Interval = list[int, int]
type IntervalList = list[Interval]

def binary_search(sorted_intervals: IntervalList, id: int) -> Interval:
    """Takes sorted list of intervals and an id.
    Returns interval with the largest lowerbound <= id, if it exists.
    Otherwise return None."""
    a = 0
    b = len(sorted_intervals) - 1

    if sorted_intervals[0][0] > id:
        return None

    while a < b:
        #Bisect search interval
        c = (a + b + 1)//2
        if sorted_intervals[c][0] <= id:
            a = c
        else:
            b = c - 1
    if a == b:
        return sorted_intervals[a]
    return None

def load_intervals(filename: str) -> tuple[IntervalList, list[int]]:
    """Loads file, processes intervals into list of sorted, disjoint intervals."""

    unsorted_intervals = None
    available_ids = None
    with open(filename, "r") as f:
        unsorted_intervals, available_ids = f.read().split("\n\n")
        unsorted_intervals = [[int(interv_bound) for interv_bound in interv.split("-")] for interv in unsorted_intervals.split("\n")]
        available_ids = [int(avail_id) for avail_id in available_ids.strip().split("\n")]

    #Sort the loaded intervals after their lower boundary
    key_func = lambda interv: interv[0]
    sorted_intervals = sorted(unsorted_intervals, key=key_func)

    #Merge overlapping intervals
    disjoint_intervals = []
    current_merge = None
    for interv in sorted_intervals:
        if current_merge == None:
            current_merge = list(interv)
        elif interv[0] <= current_merge[1] + 1:
            #Merge interv with current interval
            current_merge[1] = max(interv[1], current_merge[1])
        else:
            #Begin next, disjoint interval
            disjoint_intervals.append(current_merge)
            current_merge = interv
    disjoint_intervals.append(current_merge)

    return disjoint_intervals, available_ids

def count_fresh_available_ids(disjoint_intervals: IntervalList, available_ids: list[int]) -> int:
    #Subproblem a: Find all fresh available ids
    fresh_available_count = 0
    for avail_id in available_ids:
        interv = binary_search(disjoint_intervals, avail_id)
        if interv != None and avail_id <= interv[1]:
            fresh_available_count += 1

    return fresh_available_count

def count_all_fresh_ids(disjoint_intervals: IntervalList) -> int:
    #Subproblem b: Count all ids considered fresh
    #Sum of all interval lengths
    return sum((interv[1] - interv[0] + 1 for interv in disjoint_intervals))

def solve(filename: str) -> tuple[int, int]:
    """Solves both a and b: Returns (fresh_available_count, total_fresh_count)"""
    disjoint_intervals, available_ids = load_intervals(filename)

    fresh_available_count = count_fresh_available_ids(disjoint_intervals, available_ids)

    total_fresh_count = count_all_fresh_ids(disjoint_intervals)

    return (fresh_available_count, total_fresh_count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    args = parser.parse_args()

    filepath = args.filepath
    QUIET = args.quiet

    if os.path.isfile(filepath):
        fresh_available_count, total_fresh_count = solve(filepath)
        if not QUIET:
            print("a: %s fresh, available ids"%fresh_available_count)
            print("b: %s ids considered fresh in total"%total_fresh_count)
        else:
            print(fresh_available_count)
            print(total_fresh_count)
    else:
        print("There is no such file")
