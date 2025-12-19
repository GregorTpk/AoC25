import os, sys
import numpy as np
import sympy
import galois
import scipy.optimize
import pulp

import galois
import numpy as np
from itertools import product
from fractions import Fraction
from math import gcd



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
 
        matrix = np.matrix_transpose(matrix)

        button_matrix.append(matrix)

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
 
    for i, matrix in enumerate(button_matrix): 
        _, pivots = sympy.Matrix(matrix).rref() # Pivot elemente bestimmen
        button_matrix_independent.append(matrix[:, pivots]) # Columns der Pivot elemente nehmen

    for i, matrix in enumerate(button_matrix):
        A = np.array(matrix, dtype=int)
        b = np.array(indicator_num2[i], dtype=int).reshape(-1)
        c = np.array(v_joltage[i], dtype = int).reshape(-1)

       # results_a += solve_over_F2(A,b)
        print("Matrix Numer: ", i)
        results_b += solve_easy(A,c)
        print("---")
        

    return results_a, results_b

def lcm(a,b): # calculat least common multiple of two numbers
    return abs(a*b)//gcd(a,b)

def minimal_scalar(vector): 
    denominators = [Fraction(x).denominator for x in vector]
    scalar = denominators[0]
    for denom in denominators[1:]:
        scalar = lcm(scalar, denom)
    return [scalar*x for x in vector]

def solve_easy(A,b): 
    n_rows = len(A)
    n_cols = len(A[0])

    res = scipy.optimize.linprog(
    [1] * n_cols,
    A_eq=A,
    b_eq=b,
    bounds=(0, None),
    method="highs",
    integrality=True,
    )
    return round(res.fun)   

def solve_over_r(A,b):
 #   x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    n_rows = len(A)
    n_cols = len(A[0])
    
    A_aug = np.column_stack((A,b))

    rref,pivot_cols = sympy.Matrix(A_aug).rref()

    rref = rref.tolist()

    pivot_cols = list(pivot_cols) # -> Indices abhängigen Variablen (xi bei Ax=b)

    # Indices der Nicht-Pivot-Spalten
    nonpivot_index = list(range(n_cols)) # -> Indices freie Variablen (xi bei Ax=b)

    for i in pivot_cols: 
        nonpivot_index.remove(i)

    # Homogenese Gleichungssystem lösen (A|0) -> abhängigen Variablen bestimen in dem Pivot indices rückwärtz durchlaufen

    # Partikuläre Lösung bestimmen: unabhängige Variablen (aka, indices der nicht pivot spalten = 0)
    # Nullvektor erzeugen und dann ersetzen
    x_part = [0] * (n_cols)
    for i, pivot in enumerate(pivot_cols):
        x_part[pivot] = rref[i][-1]
    print(x_part)
    #x_part = minimal_scalar(x_part)
    # Calculate the direction vectors that span the solutions space   
    direction_vec = []

    for i in nonpivot_index:
        vector = [0]*(n_cols)
        vector[i] = 1 # Set each Nonpivot element to 1 and then 
        for j, element in enumerate(pivot_cols):
            vector[element] = -rref[j][i]
        direction_vec.append(vector)
    
    max_n_button_pushes = sum(b)
    min_n_button_pushes = max(b)
    
    c = list()
    A = list()
    b = list()
    bnd = list()
    
    n_buttons_to_push = sum(x_part)
    
    if len(direction_vec) > 0:
        direction_vec_scaled = list()
        for i, vec in enumerate(direction_vec):
            new_vec = minimal_scalar(vec)
            direction_vec_scaled.append(new_vec)
            c.append(sum(new_vec))

        bnd = scipy.optimize.Bounds(lb = np.zeros(len(direction_vec_scaled)), ub = np.full(len(direction_vec_scaled), np.inf))
        integ = [2] * len(direction_vec_scaled)
        
        A = (-1) * np.transpose(direction_vec_scaled)
        bu = x_part
        bl = np.full(len(x_part), -np.inf)

        constraints = scipy.optimize.LinearConstraint(A, lb = bl, ub=bu)

        opt = scipy.optimize.milp(c = c,
                    constraints=constraints,
                    bounds = bnd,
                    integrality = integ )
        
        res = np.round(opt.fun).astype(int)
        print("opt.fun", opt.fun, "res", res)
        n_buttons_to_push += res #opt.fun 
        if not (opt.fun).is_integer() or opt.status != 0:
            print(opt)
            
    return n_buttons_to_push

def solve_pulp(A,b):  #   x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    n_rows = len(A)
    n_cols = len(A[0])
    
    A_aug = np.column_stack((A,b))

    rref,pivot_cols = sympy.Matrix(A_aug).rref()

    rref = rref.tolist()

    pivot_cols = list(pivot_cols) # -> Indices abhängigen Variablen (xi bei Ax=b)

    # Indices der Nicht-Pivot-Spalten
    nonpivot_index = list(range(n_cols)) # -> Indices freie Variablen (xi bei Ax=b)

    for i in pivot_cols: 
        nonpivot_index.remove(i)
    
    x_part = [0] * (n_cols)
    for i, pivot in enumerate(pivot_cols):
        x_part[pivot] = rref[i][-1]

    # Calculate the direction vectors that span the solutions space   
    direction_vec = []

    for i in nonpivot_index:
        vector = [0]*(n_cols)
        vector[i] = 1 # Set each Nonpivot element to 1 and then 
        for j, element in enumerate(pivot_cols):
            vector[element] = -rref[j][i]
        direction_vec.append(vector)
    
    max_n_button_pushes = sum(b)
    min_n_button_pushes = max(b)

    n_buttons_to_push = 0 #sum(x_part)
    if len(direction_vec) > 0: 

        model = pulp.LpProblem(name = "AoC", sense = pulp.LpMinimize)

        x = [pulp.LpVariable(f"x_{i}", cat='Continuous') for i in range(len(direction_vec))]
        a = pulp.LpVariable("a", lowBound = 1, upBound = 1, cat = "Integer")
        y = [pulp.LpVariable(f"y_{i}", lowBound = 0, upBound = max_n_button_pushes, cat="Integer") for i in range(len(x_part))]

        model += a * sum(x_part) + pulp.lpSum([sum(direction_vec[i]) * x[i] for i in range(len(direction_vec))])

        # add contraint functions
        for i in range(len(x_part)):
            eq = [a*x_part[i]]
            for j, element in enumerate(direction_vec):
                eq.append( x[j] * element[i])
            model += pulp.lpSum(eq) == y[i]
        
        model.solve()
        
        print(model.variables())

        n_buttons_to_push += pulp.value(model.objective)
        #print(pulp.value(model.objective))
    #    for i, var in enumerate(model.variables()):
     #       if var.value() is not None:
      #          print(var.value())
       #         n_buttons_to_push += sum(direction_vec[i])*var.value()

    return n_buttons_to_push


    
   # nonpivot_index = list_col.remove(list(pivot_index))
#    print("Urpsrungs Matrix: ", A)
 #   print("rref ", rref)
  #  print("pivot", pivot_cols)
  #  print("nonpivot index", nonpivot_index)
  #  print("Partikuläre Lösung", x_part)
  #  print("Solutions space: basis:", direction_vec)
  #  print("Results linear progr. ", opt)
  #  print("")
  
    return n_buttons_to_push

# Freiheitsgrade = n_Spalten - n_pivot -> Dimension des Lösungsraum

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
        filepath = "input2.txt"

    if os.path.isfile(filepath):
        results_a, results_b = solve(filepath)
        print("Result Part a: ", results_a)
        print("Result Part b: ", results_b)
    else:
        print("There is no such file")