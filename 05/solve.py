import os, sys

def binary_search(intervals, id):
    #Returns interval with largest lowerbound <= id,
    #None if no matching interval was found
    a = 0
    b = len(intervals) - 1

    if intervals[0][0] > id:
        return None

    while a < b:
        c = (a + b + 1)//2
        if intervals[c][0] <= id:
            a = c
        else:
            b = c - 1
    if a == b:
        return intervals[a]
    return None

def load_intervals(filename):
    #Load file, processes intrevals into list of sorted, disjoint intervals

    unsorted_intervals = None
    available_ids = None
    with open (filename, "r") as f:
        unsorted_intervals, available_ids = f.read().split("\n\n")
        unsorted_intervals = [[int(interv_bound) for interv_bound in interv.split("-")] for interv in unsorted_intervals.split("\n")]
        available_ids = [int(avail_id) for avail_id in available_ids.strip().split("\n")]

    #Sort the fresh intervals after their lower boundary
    key_func = lambda interv: interv[0]
    sorted_intervals = sorted(unsorted_intervals, key=key_func)

    #Merge overlapping intervals
    disjoint_intervals = []
    current_merge = None
    for interv in sorted_intervals:
        if current_merge == None:
            current_merge = list(interv)
        elif interv[0] <= current_merge[1] + 1:
            current_merge[1] = max(interv[1], current_merge[1])
        else:
            disjoint_intervals.append(current_merge)
            current_merge = interv
    disjoint_intervals.append(current_merge)

    return disjoint_intervals, available_ids

def count_fresh_available_ids(disjoint_intervals, available_ids):
    #Subproblem a: Find all fresh available ids
    fresh_available_count = 0
    for avail_id in available_ids:
        interv = binary_search(disjoint_intervals, avail_id)
        if interv != None and avail_id <= interv[1]:
            fresh_available_count += 1

    return fresh_available_count

def count_all_fresh_ids(disjoint_intervals):
    #Subproblem b: Count all ids considered fresh
    return sum((interv[1] - interv[0] + 1 for interv in disjoint_intervals))

def solve(filename):
    #Solves both a and b: Returns (fresh_available_count, total_fresh_count)
    disjoint_intervals, available_ids = load_intervals(filename)

    fresh_available_count = count_fresh_available_ids(disjoint_intervals, available_ids)

    total_fresh_count = count_all_fresh_ids(disjoint_intervals)

    return (fresh_available_count, total_fresh_count)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"

    if os.path.isfile(filepath):
        fresh_available_count, total_fresh_count = solve(filepath)
        print("a: %s fresh, available ids"%fresh_available_count)
        print("b: %s ids considered fresh in total"%total_fresh_count)
    else:
        print("There is no such file")
