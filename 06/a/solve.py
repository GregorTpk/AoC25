import os, sys, re

def solve(filepath):
    """Solve problem 06a.
    Takes filepath, returns total_sum."""

    #Read input file

    with open(filepath, "r") as f:
        lines = list(f.readlines())
        #Split lines at sequences of ' '
        operand_lists = [[int(operand) for operand in re.split(r' {1,}', line.strip())] for line in lines[:-1]]
        operators = re.split(r' {1,}', lines[-1].strip())

    #Do all calculations
    total_sum = 0

    for operands, operator in zip(zip(*operand_lists), operators):
        if operator == "+":
            total_sum += sum(operands)
        elif operator == "*":
            prod = 1
            for op in operands:
                prod *= op
            total_sum += prod

    return total_sum

if __name__ == "__main__":
    (filepath := sys.argv[1]) if len(sys.argv) >= 2 else (filepath := "input.txt")
    print(solve(filepath)) if os.path.isfile(filepath) else print("There is no such file")
