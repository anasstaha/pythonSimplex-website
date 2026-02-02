from app import SimplexSolver
from copy import deepcopy
import numpy as np

s = SimplexSolver([-3,-2], [[1,1],[2,1]], [4,3], ['<=','>='], 'two_phase', False)

# Manually trace through solve_two_phase
A_std, b_std = s.convert_to_standard_form()
n_cols = A_std.shape[1]

print("Standard form:")
print(f"A_std:\n{A_std}")
print(f"b_std: {b_std}")
print(f"Artificial vars: {s.artificial_vars}")

# Phase 1
c_phase1 = [0] * n_cols
for idx in s.artificial_vars:
    c_phase1[idx] = 1
c_phase1 = np.array(c_phase1, dtype=float)

tableau = s._create_tableau(A_std, b_std, c_phase1)

# Canonical form adjustment for Phase 1
for artificial_idx in s.artificial_vars:
    for row_idx in range(tableau.shape[0] - 1):
        if abs(tableau[row_idx, artificial_idx] - 1.0) < 1e-10:
            tableau[-1, :-1] -= tableau[row_idx, :-1]
            tableau[-1, -1] -= tableau[row_idx, -1]
            break

print("\nPhase 1 initial tableau (after canonical form):")
print(tableau)

# Solve Phase 1
result1, tableau_phase1 = s._solve_tableau(deepcopy(tableau), "Phase 1")

print("\nPhase 1 result:")
print(f"  Success: {result1.get('success')}")
print(f"  Optimal value: {result1.get('optimal_value')}")
print(f"  Iterations: {result1.get('iterations')}")
print(f"  Message: {result1.get('message')}")

print(f"\nNumber of iterations tracked: {len(s.iterations)}")
print("Iteration history:")
for i, iteration in enumerate(s.iterations[:5]):  # First 5 iterations
    print(f"  Iteration {i}: {iteration}")

print("\nPhase 1 final tableau:")
print(tableau_phase1)

# Check artificial variable values
print("\nArtificial variable values in Phase 1 final tableau:")
for idx in s.artificial_vars:
    col = tableau_phase1[:-1, idx]
    print(f"  Column {idx} (a.v. {idx}): {col}")
    if np.count_nonzero(col) == 1:
        row_idx = np.where(col != 0)[0][0]
        if abs(col[row_idx] - 1.0) < 1e-10:
            value = tableau_phase1[row_idx, -1]
            print(f"    Basic variable, value = {value}")
