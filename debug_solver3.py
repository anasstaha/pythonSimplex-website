#!/usr/bin/env python3
"""Debug script - detailed tableau analysis"""

import numpy as np
from app import SimplexSolver
from copy import deepcopy

# Test with a simple problem
c = [-2, -3]  # Minimize -2x1 -3x2 (which is maximize 2x1 + 3x2)
A = [[1, 1], [1, 0], [0, 1]]
b = [5, 1, 1]
signs = ['<=', '>=', '>=']

solver = SimplexSolver(c, A, b, signs, method='big_m', is_maximization=True)
A_std, b_std = solver.convert_to_standard_form()

# Phase 1
n_cols = A_std.shape[1]
c_phase1 = [0] * n_cols
for idx in solver.artificial_vars:
    c_phase1[idx] = 1
c_phase1 = np.array(c_phase1, dtype=float)

tableau = solver._create_tableau(A_std, b_std, c_phase1)
print("Initial Tableau (Phase 1):")
print(tableau)

result1, tableau_phase1 = solver._solve_tableau(deepcopy(tableau), "Phase 1")

print("\n" + "="*70)
print("FINAL TABLEAU AFTER PHASE 1:")
print(tableau_phase1)
print(f"\nOptimal value Phase 1: {result1.get('optimal_value')}")
print(f"Iterations Phase 1: {result1.get('iterations')}")

# Phase 2
c_phase2 = np.concatenate([solver.c, np.zeros(n_cols - solver.n_vars)])
print(f"\nPhase 2 objective: {c_phase2}")

tableau_phase2 = deepcopy(tableau_phase1)
tableau_phase2[-1, :-1] = -c_phase2
tableau_phase2[-1, -1] = 0

print("\nInitial Tableau (Phase 2):")
print(tableau_phase2)

result2, final_tableau = solver._solve_tableau(tableau_phase2, "Phase 2")

print("\n" + "="*70)
print("FINAL TABLEAU AFTER PHASE 2:")
print(final_tableau)
print(f"\nOptimal value Phase 2: {result2.get('optimal_value')}")
print(f"Iterations Phase 2: {result2.get('iterations')}")

# Manual solution extraction
print("\n" + "="*70)
print("ANALYZING SOLUTION EXTRACTION:")
m = final_tableau.shape[0] - 1
n = solver.n_vars

print(f"\nConstraint matrix (m={m} constraints, n={n} original variables):")
print(final_tableau[:m, :n+3])  # Show first few columns

print(f"\nLooking for basic variables (columns with exactly one non-zero = 1):")
for j in range(n):
    col = final_tableau[:m, j]
    nonzero_count = np.count_nonzero(col)
    print(f"  x{j+1}: col = {col}, nonzero count = {nonzero_count}, all_are_0or1 = {all(v in [0.0, 1.0] for v in col)}")
    if nonzero_count == 1:
        i = np.where(col != 0)[0][0]
        if abs(col[i] - 1.0) < 1e-10:
            value = final_tableau[i, -1]
            print(f"       -> BASIC: x{j+1} = {value}")

solution = solver._extract_solution(final_tableau)
print(f"\nExtracted solution: {solution}")
print(f"Optimal value: {result2.get('optimal_value')}")
