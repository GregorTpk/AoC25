import os, sys, re

def solve(filepath):
    """Solve problem 06b.
    Takes filepath, returns total_sum."""

    #Read and parse input file

    with open(filepath, "r") as f:
        lines = list(f.readlines())

    #Fill shorter lines with spaces for uniform line length
    longest_line = max((len(line) for line in lines))
    for i, line in enumerate(lines):
        lines[i] = line.strip("\n")
        lines[i] += " "*(longest_line - len(line))

    #Extract all operators and operand-lists from the lines
    operand_lines = lines[:-1]
    operand_lists = []
    operators = []

    column_operands = None
    #Iterate through operator-line in order to discern the columns
    for i, char in enumerate(lines[-1]):

        #An operator != " " implies start of new column
        if char != " ":
            if column_operands!= None:
                operand_lists.append(column_operands)
            operators.append(char)
            column_operands = []

        #Read operand top to bottom at current index
        new_operand = ""
        for op_line in operand_lines:
            if op_line[i] != " ":
                new_operand += op_line[i]
        if new_operand != "":
            column_operands.append(int(new_operand))
    #Add last operand-list
    operand_lists.append(column_operands)


    #Do all calculations

    total_sum = 0

    for operands, operator in zip(operand_lists, operators):
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
