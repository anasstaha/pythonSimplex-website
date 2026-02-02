#!/usr/bin/env python3
"""Debug script - test what the web form is doing"""

import numpy as np
from app import SimplexSolver

# Let's test with a MAXIMIZATION problem (like what might come from the web form)
# Maximize: Z = 2x1 + 3x2
# Subject to:
#   x1 + x2 <= 5
#   x1 >= 1
#   x2 >= 1

print("=" * 70)
print("TEST: Maximize Z = 2x1 + 3x2")
print("Subject to: x1 + x2 <= 5, x1 >= 1, x2 >= 1")
print("=" * 70)

c = [2, 3]  # Original objective
A = [[1, 1], [1, 0], [0, 1]]
b = [5, 1, 1]
signs = ['<=', '>=', '>=']

# The web form converts maximization to minimization by negating c
is_maximization = True
if is_maximization:
    c = [-c[0], -c[1]]  # Negate for minimization

print(f"\nAfter conversion for minimization:")
print(f"c (negated) = {c}")

solver = SimplexSolver(c, A, b, signs, method='big_m', is_maximization=is_maximization)

# Convert to standard form
A_std, b_std = solver.convert_to_standard_form()
print(f"\nStandard form:")
print(f"A_std shape: {A_std.shape}")
print(f"A_std = \n{A_std}")
print(f"b_std = {b_std}")
print(f"Artificial vars indices: {solver.artificial_vars}")
print(f"Slack vars indices: {solver.slack_vars}")

# Solve
result = solver.solve_two_phase()

print(f"\nResult from solver:")
print(f"success: {result.get('success')}")
print(f"solution: {result.get('solution')}")
print(f"optimal_value (before adjustment): {result.get('optimal_value')}")
print(f"iterations: {result.get('iterations')}")

# In the web form, if it's maximization, we negate the optimal value back
if result.get('success') and is_maximization:
    print(f"optimal_value (after negation for max): {-result.get('optimal_value')}")
    
print(f"\nExpected: Z = 8 (at x1=1, x2=4 or x1=2, x2=3 etc)")
