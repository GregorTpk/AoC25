import os, sys

def solve(filename): 
    with open(filename) as f:
        inp = f.read().strip().split(",")

    invalid_id = list()

    for i, check_id in enumerate(inp):
        start = int(check_id.split('-')[0])
        end = int(check_id.split('-')[1])
        for j, num in enumerate(range(start, end + 1)):
            if len(str(num)) / 2 == len(str(num)) // 2:
                if str(num)[:(len(str(num)) // 2)] == str(num)[(len(str(num)) // 2):]:
                    invalid_id.append(num)
 
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
