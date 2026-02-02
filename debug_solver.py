#!/usr/bin/env python3
"""Script to debug the simplex solver"""

import numpy as np
from app import SimplexSolver

# Test case: Simple problem
# Minimize: Z = 2x1 + 3x2
# Subject to:
#   x1 + x2 >= 5
#   2x1 + x2 <= 10
#   x1, x2 >= 0
# Expected: Z = 10, x1=5, x2=0 or Z=10, x1=0, x2=5 or somewhere on the line

print("=" * 60)
print("TEST 1: Minimize Z = 2x1 + 3x2")
print("Subject to: x1 + x2 >= 5, 2x1 + x2 <= 10")
print("=" * 60)

c = [2, 3]
A = [[1, 1], [2, 1]]
b = [5, 10]
signs = ['>=', '<=']

solver = SimplexSolver(c, A, b, signs, method='big_m', is_maximization=False)

# Convert to standard form and print
A_std, b_std = solver.convert_to_standard_form()
print(f"\nOriginal problem:")
print(f"Minimize: Z = 2x1 + 3x2")
print(f"Constraints: {A} {signs} {b}")
print(f"\nStandard form:")
print(f"A_std = \n{A_std}")
print(f"b_std = {b_std}")
print(f"Artificial vars: {solver.artificial_vars}")
print(f"Slack vars: {solver.slack_vars}")

# Create initial tableau
n_cols = A_std.shape[1]
c_phase1 = [0] * n_cols
for idx in solver.artificial_vars:
    c_phase1[idx] = 1
c_phase1 = np.array(c_phase1, dtype=float)

print(f"\nPhase 1 objective (minimize sum of artificial vars):")
print(f"c_phase1 = {c_phase1}")

tableau = solver._create_tableau(A_std, b_std, c_phase1)
print(f"\nInitial tableau (Phase 1):")
print(tableau)
print(f"\nLast row (objective): {tableau[-1, :-1]}")
print(f"RHS: {tableau[-1, -1]}")

# Check optimality condition
last_row = tableau[-1, :-1]
epsilon = 1e-10
print(f"\nOptimality check (all elements >= -epsilon = {-epsilon}):")
print(f"Elements: {last_row}")
print(f"All >= {-epsilon}? {np.all(last_row >= -epsilon)}")
print(f"Min element: {np.min(last_row)}")

# Solve
print("\n" + "="*60)
print("SOLVING...")
print("="*60)

result = solver.solve_two_phase()

print(f"\nResult: {result}")
