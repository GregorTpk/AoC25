import os, argparse
from itertools import product

import numpy as np
import galois
import scipy.optimize

QUIET = False
TRANSLATION_DICT = {
    "#": "1",
    ".": "0"
}
TRANSLATION_TABLE = str.maketrans(TRANSLATION_DICT)

def solve(filename): 
    results_a = 0
    results_b = 0

    with open(filename) as f:
        for i, line in enumerate(f):
            #Read data from current line
            machine = line.strip().split(" ")
            indicators_str = machine[0]
            indicators = [int(val) for val in indicators_str[1:-1].translate(TRANSLATION_TABLE)] # List of indicator values as integers
            joltage = machine[-1][1:-1].split(",") # List of joltage values as strings
            buttons = machine[1:-1] # List of buttons as strings

            #Build button matrix
            n_cols = len(buttons)
            n_rows = len(indicators)
            button_matrix = np.zeros((n_rows, n_cols))

            for col, button in enumerate(buttons):
                indices = button[1:-1].split(",") # [1:-1] removes '(', ')'
                for row in indices:
                    button_matrix[int(row)][col] = 1
    
            A = np.array(button_matrix, dtype=int)
            b = np.array(indicators, dtype=int)
            c = np.array(joltage, dtype = int)

            #Solve subproblems
            results_a += solve_over_F2(A,b)
            results_b += solve_over_N(A,c)

    return results_a, results_b

def solve_over_N(A, b):
    """Solves Ax=b with values in N_0."""

    n_cols = len(A[0])

    res = scipy.optimize.linprog(c=[1] * n_cols,    # Minimize 1-norm, i.e. c^T*x
                                 A_eq=A,            # Button matrix
                                 b_eq=b,            # Specified joltage levels
                                 bounds=(0, None),  # Bound to non-negative components x_i
                                 method="highs",
                                 integrality=True)  # Constrain to integral x_i
    return round(res.fun)   

def solve_over_F2(A, b):
    """Solves Ax=b with values in the field F_2."""

    n_cols = len(A[0])

    solutions = list()

    GF = galois.GF(2)  # Binary field GF(2)

    A = GF(A)
    b = GF(b)

    A_aug = GF(np.column_stack((A, b)))

    rref = A_aug.row_reduce() # Gaussian Elimination to receive reduced row echelon form

    N = A.null_space()  # Contains all vectors x satisfying the Ax=0

    if not QUIET:
        print(N)

    # Compute a particular solution
    x_part = GF([0]*n_cols)
    for row in rref:
        pivot_cols = np.where(row[:-1] == 1)[0] # gives col of first entry which has 1
        if len(pivot_cols) > 0:
            pivot = pivot_cols[0]
            x_part[pivot] = row[-1] # allowed as matrix is in reduced echelon form

    # All solutions
    for mask in product([0,1], repeat=len(N)):
        x = x_part.copy()
        for coeff, basis_vec in zip(mask, N):
            x += coeff * basis_vec
        solutions.append(x)

    # Calculate norm for all possible solutions, return the minimum
    norms = list()
    for sol in solutions:
        norms.append(sum(map(int, sol)))

    return min(norms)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    args = parser.parse_args()

    filepath = args.filepath

    QUIET = args.quiet

    if os.path.isfile(filepath):
        result_a, result_b = solve(filepath)
        if not QUIET:
            print("Result Part a: ", result_a)
            print("Result Part b: ", result_b)
        else:
            print(result_a)
            print(result_b)
    else:
        print("There is no such file")
