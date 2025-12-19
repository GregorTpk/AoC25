import os
import sys
from itertools import product
import time

import numpy as np
import galois
import scipy.optimize

DICT = {
    "#": "1",
    ".": "0"
}

def solve(filename): 
    results_a = 0
    results_b = 0
    inp = list()

    indicator = list()
    indicator_num = list()

    joltage = list()
    button = list()
    button_matrix = list()

    with open(filename) as f: 
        for i, line in enumerate(f): 
            machine = line.strip().split(" ")
            inp.append(machine) # line in inp is one machine
            indicator.append(machine[0])
            joltage.append(machine[-1][1:-1].split(","))
            button.append(machine[1:-1])

            n_cols = len(indicator[i])-2
            n_rows = len(button[i])
            matrix = np.zeros((n_rows, n_cols))

            for row, buttons in enumerate(button[i]):
                indices = buttons[1:-1].split(",") # () werden durch [1:-1] entfernt

                for col in indices:
                    matrix[row][int(col)] = 1
    
            matrix = np.matrix_transpose(matrix)

            button_matrix.append(matrix)

            # Translation of indicator 
            trans = str.maketrans(DICT)
            c = list(map(int, list(indicator[i][1:-1].translate(trans))))
            indicator_num.append(c)

            A = np.array(button_matrix[i], dtype=int)
            b = np.array(indicator_num[i], dtype=int).reshape(-1)
            c = np.array(joltage[i], dtype = int).reshape(-1)

            results_a += solve_over_F2(A,b)
            results_b += solve_easy(A,c)

    return results_a, results_b

def solve_easy(A,b):
    n_cols = len(A[0])

    res = scipy.optimize.linprog(c= [1] * n_cols,
                                 A_eq=A,
                                 b_eq=b,
                                 bounds=(0, None),
                                 method="highs",
                                 integrality=True)
    return round(res.fun)   

def solve_over_F2(A, b):
    n_cols = len(A[0])

    solutions = list()
    norms = list()

    GF = galois.GF(2)  # Binary field GF(2)

    A = GF(A)
    b = GF(b)

    A_aug = GF(np.column_stack((A, b)))

    rref = A_aug.row_reduce() # Gaussian Eliminatio to receive reduced row elchon form
    
    N = A.null_space()  # contains all vectors x sadisfying the Ax=0
    print(N)

    # compute particular solution
    x_part = GF([0]*n_cols)
    for i, row in enumerate(rref):
        pivot_cols = np.where(row[:-1] == 1)[0] # gives col of first entry which has 0 
        if len(pivot_cols) > 0:
            pivot = pivot_cols[0]
            x_part[pivot] = row[-1] # allowed as matrix is in reduced elchon form

    # all solutions
    for mask in product([0,1], repeat=len(N)):
        x = x_part.copy()
        for coeff, basis_vec in zip(mask, N):
            x += coeff * basis_vec
        solutions.append(x)

    # calculate norm for all possible solutions, return the minimum
    for i, sol in enumerate(solutions):
        new_norm = (int(sum(np.array(sol))))
        norms.append(new_norm)

    return (min(norms))

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "example.txt"

    if os.path.isfile(filepath):
        t_start = time.time()
        result_a, result_b = solve(filepath)
        t_end = time.time()
        print("Result Part a: ", result_a)
        print("Result Part b: ", result_b)
        print("Time: ", t_end-t_start)
    else:
        print("There is no such file")