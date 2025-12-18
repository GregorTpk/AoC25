import os, sys
import numpy as np
import sympy
import galois

import galois
import numpy as np
from itertools import product


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
    button_matrix_independent = list()

    with open(filename) as f: 
        for i, line in enumerate(f): 
            machine = line.strip().split(" ")
            inp.append(machine)

    for i, machine in enumerate(inp): 
        indicator.append(machine[0])
        joltage.append(machine[-1])
        button.append(machine[1:-1])

    # Create for each machine button matrix
    for i, machine in enumerate(inp):
        n_cols = len(indicator[i])-2
        n_rows = len(button[i])
        matrix = np.zeros((n_rows, n_cols))

        for j, buttons in enumerate(button[i]):
            indices = buttons[1:-1].split(",") # () werden durch [1:-1] entfernt

            for k, index in enumerate(indices):
                matrix[j][int(index)] = 1
     #   print("Matrix")
      #  print(matrix)
        matrix = np.matrix_transpose(matrix)
       # print("Transponierte Matrix") # Transpose Matrix
        #print(matrix)
        button_matrix.append(matrix)
    #print(button_matrix)
    # From indicator to list of 1 and 0
    for i, indicators in enumerate(indicator): 
        trans = str.maketrans(DICT)
        c = indicators[1:-1].translate(trans)
        indicator_num.append(c)
    indicator_num2 = list()

    # Make str into list
    for i, indicators in enumerate(indicator_num):
        list_indicators = list(map(int, list(indicators))) 
        indicator_num2.append(list(list_indicators))
    v_joltage = list()
    for i, connection in enumerate(joltage): 
        v_joltage.append(connection[1:-1].split(","))
        #v_connections
    #print(v_connections)
    #print(joltage)
    for i, matrix in enumerate(button_matrix): 
        _, pivots = sympy.Matrix(matrix).rref() # Pivot elemente bestimmen
        button_matrix_independent.append(matrix[:, pivots]) # Columns der Pivot elemente nehmen

    for i, matrix in enumerate(button_matrix):
        A = np.array(matrix, dtype=int)
        b = np.array(indicator_num2[i], dtype=int).reshape(-1)
        c = np.array(v_joltage[i], dtype = int).reshape(-1)

        results_a += solve_over_F2(A,b)
       # print(solve_over_r(A,c))
    # = 0
    return results_a, results_b

def solve_over_r(A,b):
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

    A_aug = np.column_stack((A,b))

    #rref = A_aug.rref
    rref,_ = sympy.Matrix(A_aug).rref()
    print(rref)
    return x


def solve_over_F2(A, b):
    # --- 1) Define the field and matrix ---
    GF = galois.GF(2)  # Binary field GF(2)

    A = GF(A)
    b = GF(b)

    A_aug = GF(np.column_stack((A, b)))

    rref = A_aug.row_reduce()
    
    N = A.null_space()  # List of basis vectors

    # 4) Partikuläre Lösung (= letzte Spalte der RREF an Pivot Stellen)
    x_part = GF.Zeros(A.shape[1]) # 
    # (man müsste hier die Pivotspalten identifizieren…
    for i, row in enumerate(rref):
        # Pivot spalten sind meist die ersten nonzero Werte
        pivot_cols = np.where(row[:-1] == 1)[0]
        if len(pivot_cols) > 0:
            pivot = pivot_cols[0]
            x_part[pivot] = row[-1]

    # 5) Alle Lösungen auspartikuläre + Nullraum
    solutions = []

    for mask in product([0,1], repeat=N.shape[0]):
        x = x_part.copy()
        for coeff, basis_vec in zip(mask, N):
            x += coeff * basis_vec
        solutions.append(x)
    n_buttons_to_press = list()

    sol = []
   # print(solutions[1])
    for i in range(len(solutions)):
        sol.append(np.array(solutions[i]))
        count_ones = sum(1 for v in solutions[i] if v == 1)
        n_buttons_to_press.append(count_ones)

    sum_switch = list()
    for i in range(len(sol)):
        new_sum = int(sum(sol[i]))
        sum_switch.append(new_sum)
    print(sum_switch)
    return (min(sum_switch))

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "example.txt"

    if os.path.isfile(filepath):
        results_a = solve(filepath)
        print("Result Part a: ", results_a)
        print("Result Part b: ", )
    else:
        print("There is no such file")