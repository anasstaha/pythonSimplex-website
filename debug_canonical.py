#!/usr/bin/env python3
"""Debug with more output"""

import numpy as np
from app import SimplexSolver
from copy import deepcopy

# Test with a simple problem
c = [-2, -3]
A = [[1, 1], [1, 0], [0, 1]]
b = [5, 1, 1]
signs = ['<=', '>=', '>=']

solver = SimplexSolver(c, A, b, signs, method='big_m', is_maximization=True)
A_std, b_std = solver.convert_to_standard_form()

n_cols = A_std.shape[1]
c_phase1 = [0] * n_cols
for idx in solver.artificial_vars:
    c_phase1[idx] = 1
c_phase1 = np.array(c_phase1, dtype=float)

tableau = solver._create_tableau(A_std, b_std, c_phase1)

print("Initial tableau BEFORE canonical form adjustment:")
print(tableau)
print(f"Artificial vars: {solver.artificial_vars}")

# Normalize the objective row
for artificial_idx in solver.artificial_vars:
    for row_idx in range(tableau.shape[0] - 1):
        if abs(tableau[row_idx, artificial_idx] - 1.0) < 1e-10:
            print(f"\nFound artificial var {artificial_idx} is basic in row {row_idx}")
            print(f"Row before: {tableau[-1, :]}")
            tableau[-1, :-1] -= tableau[row_idx, :-1]
            tableau[-1, -1] -= tableau[row_idx, -1]
            print(f"Row after:  {tableau[-1, :]}")
            break

print("\nInitial tableau AFTER canonical form adjustment:")
print(tableau)

print("\n" + "="*70)
print("Solving Phase 1...")

result1, tableau_phase1 = solver._solve_tableau(deepcopy(tableau), "Phase 1")
print(f"\nPhase 1 result: {result1}")
print(f"\nFinal tableau Phase 1:")
print(tableau_phase1)
