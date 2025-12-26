import os, re, argparse

type OperandGroups = list[list[int]]
type Operators = list[str]

def load_rowwise(filepath: str) -> tuple[OperandGroups, Operators]:
    """Read and parse input file for subproblem a."""

    with open(filepath, "r") as f:
        lines = list(f.readlines())
        #Split lines at sequences of ' '
        linewise_operands = [[int(operand) for operand in re.split(r' {1,}', line.strip())] for line in lines[:-1]]
        operators = re.split(r' {1,}', lines[-1].strip())

    operand_groups = list(zip(*linewise_operands))

    return operand_groups, operators

def load_columnwise(filepath: str) -> tuple[OperandGroups, Operators]:
    """Read and parse input file for subproblem b."""

    with open(filepath, "r") as f:
        lines = list(f.readlines())

    #Fill shorter lines with spaces for uniform line length
    #Lines probably already have uniform lenght
    longest_line = max((len(line) for line in lines))
    for i, line in enumerate(lines):
        lines[i] = line.strip("\n")
        lines[i] += " "*(longest_line - len(lines[i]))

    #Extract all operators and operand-groups from the lines
    operand_lines = lines[:-1]
    operand_groups = []
    operators = []
    #Iterate through operator-line in order to discern the columns
    for i, char in enumerate(lines[-1]):

        #An operator != " " implies start of new column
        if char != " ":
            current_operands = []
            operand_groups.append(current_operands)
            operators.append(char)

        #Read operand top to bottom at current column
        new_operand = ""
        for op_line in operand_lines:
            if op_line[i] != " ":
                new_operand += op_line[i]
        if new_operand != "":
            current_operands.append(int(new_operand))

    return operand_groups, operators

def calculate_total_sum(operand_groups: OperandGroups, operators: Operators) -> int:
    total_sum = 0

    for operands, operator in zip(operand_groups, operators):
        if operator == "+":
            total_sum += sum(operands)
        elif operator == "*":
            prod = 1
            for op in operands:
                prod *= op
            total_sum += prod

    return total_sum

def solve(filepath: str) -> tuple[int, int]:
    """Solve problem 06 a+b.
    Takes filepath, returns (total sum for a, total sum for b)."""
    rowwise_total_sum = calculate_total_sum(*load_rowwise(filepath))
    columnwise_total_sum = calculate_total_sum(*load_columnwise(filepath))
    return rowwise_total_sum, columnwise_total_sum

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    args = parser.parse_args()

    filepath = args.filepath
    QUIET = args.quiet

    if os.path.isfile(filepath):
        rowwise_total_sum, columnwise_total_sum = solve(filepath)
        if not QUIET:
            print("a: total sum %s when reading numbers rowwise."%rowwise_total_sum)
            print("b: total sum %s when reading numbers columnwise."%columnwise_total_sum)
        else:
            print(rowwise_total_sum)
            print(columnwise_total_sum)
    else:
        print("There is no such file")
