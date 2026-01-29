#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test des contraintes >= et =
"""

from app import SimplexSolver
import numpy as np

def test_case(name, c, A, b, signs, is_max):
    """Tester un cas"""
    print("\n" + "="*80)
    print(f"TEST: {name}")
    print("="*80)
    print(f"Objectif: {'Maximiser' if is_max else 'Minimiser'} Z = {' + '.join([f'{ci}x{i+1}' for i, ci in enumerate(c)])}")
    print(f"Contraintes:")
    for i, (row, sign, bi) in enumerate(zip(A, signs, b)):
        constraint = ' + '.join([f'{aij}x{j+1}' for j, aij in enumerate(row)])
        print(f"  {constraint} {sign} {bi}")
    
    # Convertir c selon l'objectif (toujours minimiser)
    c_to_use = [-ci for ci in c] if is_max else c
    
    print(f"\nRésolution avec Grand M:")
    solver_gm = SimplexSolver(c_to_use, A, b, signs, 'big_m', is_max)
    result_gm = solver_gm.solve_big_m()
    
    if result_gm['success']:
        print(f"OK - Succes ({result_gm['iterations']} iterations)")
        for i, val in enumerate(result_gm['solution']):
            print(f"  x{i+1} = {val:.6f}")
        print(f"  Z = {result_gm['optimal_value']:.6f}")
    else:
        print(f"XX - Erreur: {result_gm['message']}")
    
    print(f"\nResolution avec Deux Phases:")
    solver_2p = SimplexSolver(c_to_use, A, b, signs, 'two_phase', is_max)
    result_2p = solver_2p.solve_two_phase()
    
    if result_2p['success']:
        print(f"OK - Succes ({result_2p['iterations']} iterations)")
        for i, val in enumerate(result_2p['solution']):
            print(f"  x{i+1} = {val:.6f}")
        print(f"  Z = {result_2p['optimal_value']:.6f}")
    else:
        print(f"XX - Erreur: {result_2p['message']}")

# Test 1: Minimiser avec contraintes >=
test_case(
    "Minimiser Z = 5x1 + 9x2 + 14x3 avec x1>=3, x2>=104, x3>=37",
    [5, 9, 14],           # c
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]],  # A
    [3, 104, 37],         # b
    ['>=', '>=', '>='],   # signs
    False                 # minimize
)

# Test 2: Minimiser avec contraintes >=
test_case(
    "Minimiser Z = 2x1 + 3x2 avec x1 + 2x2 >= 6, 2x1 + x2 >= 5",
    [2, 3],               # c
    [[1, 2], [2, 1]],     # A
    [6, 5],               # b
    ['>=', '>='],         # signs
    False                 # minimize
)

# Test 3: Minimiser avec contrainte d'égalité
test_case(
    "Minimiser Z = x1 + 2x2 avec x1 + x2 = 3, 2x1 + x2 <= 4",
    [1, 2],               # c
    [[1, 1], [2, 1]],     # A
    [3, 4],               # b
    ['=', '<='],          # signs
    False                 # minimize
)

# Test 4: Maximiser avec contraintes >=
test_case(
    "Maximiser Z = 3x1 + 2x2 avec x1 + x2 >= 2, 2x1 + x2 >= 3",
    [3, 2],               # c
    [[1, 1], [2, 1]],     # A
    [2, 3],               # b
    ['>=', '>='],         # signs
    True                  # maximize
)

print("\n" + "="*80)
print("FIN DES TESTS")
print("="*80)
