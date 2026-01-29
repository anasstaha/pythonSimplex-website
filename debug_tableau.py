#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug pour x >= b
"""

from app import SimplexSolver
import numpy as np

print("\n=== Test: Minimiser Z = 5x1 + 9x2 + 14x3 avec x1>=3, x2>=104, x3>=37 ===\n")

c = [5, 9, 14]
A = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
b = [3, 104, 37]
signs = ['>=', '>=', '>=']

solver = SimplexSolver(c, A, b, signs, 'big_m', is_maximization=False)

print("Avant conversion à la forme standard:")
print(f"  c = {solver.c}")
print(f"  A = {solver.A}")
print(f"  b = {solver.b}")
print(f"  signs = {solver.signs}")

A_std = solver.convert_to_standard_form()

print(f"\nAprès conversion à la forme standard:")
print(f"  A_std shape = {A_std.shape}")
print(f"  A_std = \n{A_std}")
print(f"  slack_vars = {solver.slack_vars}")
print(f"  artificial_vars = {solver.artificial_vars}")

# Créer c_modified pour Grand M
n_cols = A_std.shape[1]
c_modified = list(solver.c) + [0] * (n_cols - solver.n_vars)
M = 10**6
for idx in solver.artificial_vars:
    c_modified[idx] = M

print(f"\n  c_modified = {c_modified}")

# Créer le tableau
tableau = solver._create_tableau(A_std, solver.b, np.array(c_modified, dtype=float))

print(f"\nTableau initial:")
print(f"  Shape: {tableau.shape}")
print(tableau)

print(f"\nDernière ligne (fonction objectif avant normalisation):")
print(tableau[-1, :])

# Normaliser pour les variables artificielles
M = 10**6
for i, col_idx in enumerate(solver.artificial_vars):
    print(f"\nSoustrayant M * ligne {i} de la dernière ligne (M={M}, col={col_idx})")
    tableau[-1, :] -= M * tableau[i, :]

print(f"\nDernière ligne (après normalisation):")
print(tableau[-1, :])
