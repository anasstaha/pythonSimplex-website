#!/usr/bin/env python3
"""Detailed tableau and solution analysis"""

import numpy as np
from app import SimplexSolver
from copy import deepcopy

# Test
c = [-2, -3]
A = [[1, 1], [1, 0], [0, 1]]
b = [5, 1, 1]
signs = ['<=', '>=', '>=']

solver = SimplexSolver(c, A, b, signs, method='big_m', is_maximization=True)

# Manually solve to see the tableau
A_std, b_std = solver.convert_to_standard_form()
print(f"Standard form:")
print(f"  n_vars (original): {solver.n_vars}")
print(f"  n_constraints: {solver.n_constraints}")
print(f"  Total variables in A_std: {A_std.shape[1]}")
print(f"  Artificial vars indices: {solver.artificial_vars}")
print(f"  Slack vars indices: {solver.slack_vars}")

n_cols = A_std.shape[1]
c_phase1 = [0] * n_cols
for idx in solver.artificial_vars:
    c_phase1[idx] = 1
c_phase1 = np.array(c_phase1, dtype=float)

tableau = solver._create_tableau(A_std, b_std, c_phase1)

# Apply canonical form
for artificial_idx in solver.artificial_vars:
    for row_idx in range(tableau.shape[0] - 1):
        if abs(tableau[row_idx, artificial_idx] - 1.0) < 1e-10:
            tableau[-1, :-1] -= tableau[row_idx, :-1]
            tableau[-1, -1] -= tableau[row_idx, -1]
            break

print(f"\nInitial tableau (after canonical form):")
print(tableau)

result1, final_tableau_phase1 = solver._solve_tableau(deepcopy(tableau), "Phase 1")

print(f"\nFinal tableau Phase 1:")
print(final_tableau_phase1)
print(f"Result: {result1}")

# Phase 2
c_phase2 = np.concatenate([solver.c, np.zeros(n_cols - solver.n_vars)])
tableau_phase2 = deepcopy(final_tableau_phase1)
tableau_phase2[-1, :-1] = -c_phase2
tableau_phase2[-1, -1] = 0

print(f"\nInitial tableau Phase 2:")
print(tableau_phase2)

result2, final_tableau = solver._solve_tableau(tableau_phase2, "Phase 2")

print(f"\nFinal tableau Phase 2:")
print(final_tableau)
print(f"Result: {result2}")

# Analyze solution
print("\n" + "="*70)
print("ANALYZING SOLUTION EXTRACTION:")

m = final_tableau.shape[0] - 1
n = solver.n_vars

print(f"\nBasic variable analysis (constraint rows only):")
for j in range(n_cols):
    col = final_tableau[:m, j]
    nonzero_count = np.count_nonzero(col)
    
    label = f"x{j+1}" if j < n else f"slack/artificial{j-n+1}"
    if j in solver.artificial_vars:
        label += " (artificial)"
    elif j in solver.slack_vars:
        label += " (slack)"
    
    print(f"  Col {j:2d} ({label:20s}): {col} -> nonzero={nonzero_count}", end="")
    
    if nonzero_count == 1:
        i = np.where(col != 0)[0][0]
        val = col[i]
        if abs(val - 1.0) < 1e-10:
            rhs = final_tableau[i, -1]
            print(f" BASIC, value={rhs:.2f}")
        else:
            print(f" (but coefficient is {val:.2f}, not 1)")
    else:
        print()

solution = solver._extract_solution(final_tableau)
print(f"\nExtracted solution (x1, x2): {solution}")
print(f"Optimal value: {result2.get('optimal_value')}")
