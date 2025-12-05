import os, sys
def binary_search(intervals, id, a, b):
    return None if intervals[0][0] > id else (intervals[a] if a == b else (binary_search(intervals, id, *((c, b) if intervals[(c := (a+b+1)//2)][0] <= id else (a, c-1))) if a < b else None))
def load_intervals(filename):
    with open (filename, "r") as f:
        filecontents = f.read().split("\n\n")
    disjoint_intervals, current_merge = [], (sorted_intervals := sorted([[int(interv_bound) for interv_bound in interv.split("-")] for interv in filecontents[0].split("\n")], key=lambda interv: interv[0]))[0]
    for interv in sorted_intervals:
        current_merge = [current_merge[0], max(interv[1], current_merge[1])] if interv[0] <= current_merge[1] + 1 else (interv if disjoint_intervals.append(current_merge) or True else None)
    return disjoint_intervals + [current_merge], [int(avail_id) for avail_id in filecontents[1].strip().split("\n")]
print("a: %s fresh, available ids\nb: %s ids considered fresh in total"%((lambda d: sum(((interv := binary_search(d[0], avail_id, 0, len(d[0])-1)) != None and avail_id <= interv[1] for avail_id in d[1])))((data := load_intervals(filepath))), sum((interv[1] - interv[0] + 1 for interv in data[0]))) if os.path.isfile(filepath := sys.argv[1] if len(sys.argv) >= 2 else "input.txt") else "There is no such file") if __name__ == "__main__" else None
