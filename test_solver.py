#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test de la classe SimplexSolver"""

import sys
sys.path.insert(0, '.')
from app import SimplexSolver
import json

print("=" * 70)
print("TEST 1: Problème simple avec contraintes <= (Grand M)")
print("=" * 70)
# Maximiser Z = 3x1 + 2x2
# Sous: x1 + x2 <= 4
#       2x1 + x2 <= 5
#       x1, x2 >= 0

c1 = [3, 2]
A1 = [[1, 1], [2, 1]]
b1 = [4, 5]
signs1 = ['<=', '<=']

solver1 = SimplexSolver(c1, A1, b1, signs1, 'big_m')
result1 = solver1.solve_big_m()
print(json.dumps(result1, indent=2))

print("\n" + "=" * 70)
print("TEST 2: Même problème avec Deux Phases")
print("=" * 70)

solver2 = SimplexSolver(c1, A1, b1, signs1, 'two_phase')
result2 = solver2.solve_two_phase()
print(json.dumps(result2, indent=2))

print("\n" + "=" * 70)
print("TEST 3: Problème avec contrainte >= (Grand M)")
print("=" * 70)
# Minimiser Z = 2x1 + 3x2
# Sous: x1 + 2x2 >= 6
#       2x1 + x2 >= 5
#       x1, x2 >= 0

c3 = [2, 3]
A3 = [[1, 2], [2, 1]]
b3 = [6, 5]
signs3 = ['>=', '>=']

solver3 = SimplexSolver(c3, A3, b3, signs3, 'big_m')
result3 = solver3.solve_big_m()
print(json.dumps(result3, indent=2))

print("\n" + "=" * 70)
print("TEST 4: Même problème avec Deux Phases")
print("=" * 70)

solver4 = SimplexSolver(c3, A3, b3, signs3, 'two_phase')
result4 = solver4.solve_two_phase()
print(json.dumps(result4, indent=2))

print("\n" + "=" * 70)
print("TEST 5: Problème avec contrainte = (Grand M)")
print("=" * 70)
# Maximiser Z = x1 + 2x2
# Sous: x1 + x2 = 3
#       2x1 + x2 <= 4
#       x1, x2 >= 0

c5 = [1, 2]
A5 = [[1, 1], [2, 1]]
b5 = [3, 4]
signs5 = ['=', '<=']

solver5 = SimplexSolver(c5, A5, b5, signs5, 'big_m')
result5 = solver5.solve_big_m()
print(json.dumps(result5, indent=2))

print("\n" + "=" * 70)
print("TEST 6: Même problème avec Deux Phases")
print("=" * 70)

solver6 = SimplexSolver(c5, A5, b5, signs5, 'two_phase')
result6 = solver6.solve_two_phase()
print(json.dumps(result6, indent=2))
