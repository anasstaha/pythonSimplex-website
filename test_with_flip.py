#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test avec flip de b >= négatif
"""

from app import SimplexSolver
import numpy as np

print("==== TEST 1: x >= b où toutes les variables ont des bornes inférieures ====")
print("Minimiser Z = 5x1 + 9x2 + 14x3")
print("Sous: x1 >= 3, x2 >= 104, x3 >= 37")
print()

c = [5, 9, 14]
A = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
b = [3, 104, 37]
signs = ['>=', '>=', '>=']

# Flip b négatif et inverser les signes (comme le fait /solve)
A_flipped = []
b_flipped = []
signs_flipped = []
for i in range(len(b)):
    if b[i] < 0:
        A_flipped.append([-x for x in A[i]])
        b_flipped.append(-b[i])
        # Inverser le signe
        if signs[i] == '<=':
            signs_flipped.append('>=')
        elif signs[i] == '>=':
            signs_flipped.append('<=')
        else:
            signs_flipped.append('=')
    else:
        A_flipped.append(A[i])
        b_flipped.append(b[i])
        signs_flipped.append(signs[i])

solver = SimplexSolver(c, A_flipped, b_flipped, signs_flipped, 'two_phase', is_maximization=False)
result = solver.solve_two_phase()

if result['success']:
    print(f"OK: x={result['solution']}, Z={result['optimal_value']}")
    print(f"Attendu: x=[3, 104, 37], Z=1019")
else:
    print(f"Erreur: {result['message']}")

print()
print("==== TEST 2: Minimiser Z = 2x1 + 3x2 ====")
print("Sous: x1 + 2x2 >= 6, 2x1 + x2 >= 5")
print()

c = [2, 3]
A = [[1, 2], [2, 1]]
b = [6, 5]
signs = ['>=', '>=']

A_flipped = []
b_flipped = []
signs_flipped = []
for i in range(len(b)):
    if b[i] < 0:
        A_flipped.append([-x for x in A[i]])
        b_flipped.append(-b[i])
        if signs[i] == '<=':
            signs_flipped.append('>=')
        elif signs[i] == '>=':
            signs_flipped.append('<=')
        else:
            signs_flipped.append('=')
    else:
        A_flipped.append(A[i])
        b_flipped.append(b[i])
        signs_flipped.append(signs[i])

solver = SimplexSolver(c, A_flipped, b_flipped, signs_flipped, 'two_phase', is_maximization=False)
result = solver.solve_two_phase()

if result['success']:
    print(f"OK: x={result['solution']}, Z={result['optimal_value']}")
else:
    print(f"Erreur: {result['message']}")
