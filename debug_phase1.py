#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug détaillé du tableau pour >= contraintes
"""

from app import SimplexSolver
import numpy as np

c = [2, 3]
A = [[1, 2], [2, 1]]
b = [6, 5]
signs = ['>=', '>=']

print("Test: Minimiser Z = 2x1 + 3x2 avec x1 + 2x2 >= 6, 2x1 + x2 >= 5")
print()

solver = SimplexSolver(c, A, b, signs, 'two_phase', is_maximization=False)
A_std = solver.convert_to_standard_form()

print(f"Forme standard:")
print(f"  A_std =\n{A_std}")
print(f"  slack_vars = {solver.slack_vars}")
print(f"  artificial_vars = {solver.artificial_vars}")
print()

# Construire l'objectif pour phase 1
c_phase1 = [0] * A_std.shape[1]
for idx in solver.artificial_vars:
    c_phase1[idx] = 1

print(f"Phase 1: Minimiser somme des artificielles")
print(f"  c_phase1 = {c_phase1}")
print()

tableau = solver._create_tableau(A_std, b, np.array(c_phase1, dtype=float))
print(f"Tableau Phase 1 initial:")
print(f"  Shape: {tableau.shape}")
print(tableau)
print()

# Vérifier l'optimalité
last_row = tableau[-1, :-1]
print(f"Dernière ligne: {last_row}")
print(f"Coefficient le plus négatif (pour entrer): {np.min(last_row)} à index {np.argmin(last_row)}")
print()

# Tenter un pivot
pivot_col = np.argmin(last_row)
col = tableau[:-1, pivot_col]
print(f"Colonne pivot {pivot_col}: {col}")

print(f"Test du rapport minimum:")
for i in range(len(col)):
    if col[i] > 1e-10:
        ratio = tableau[i, -1] / col[i]
        print(f"  Ligne {i}: RHS={tableau[i, -1]}, coeff={col[i]}, ratio={ratio}")
