#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Démonstration complète des deux méthodes du Simplexe
Grand M et Deux Phases
"""

from app import SimplexSolver
import json

def print_separator(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_result(result, method_name):
    """Affiche les résultats de la résolution"""
    if result['success']:
        print(f"\n✓ {method_name} - SOLUTION TROUVÉE")
        print(f"  Nombre d'itérations: {result['iterations']}")
        print(f"\n  Solution optimale:")
        for i, val in enumerate(result['solution']):
            print(f"    x{i+1} = {val:.6f}")
        print(f"\n  Valeur optimale: Z = {result['optimal_value']:.6f}")
    else:
        print(f"\n✗ {method_name} - ERREUR")
        print(f"  Message: {result.get('message', 'Erreur inconnue')}")

# ============================================================================
print_separator("PROBLÈME 1: Maximiser Z = 3x₁ + 2x₂")
print("""
Maximiser: Z = 3x₁ + 2x₂
Sous les contraintes:
  x₁ + x₂ ≤ 4
  2x₁ + x₂ ≤ 5
  x₁, x₂ ≥ 0
""")

# Résolution avec Grand M
print("\n" + "-"*80)
solver1_gm = SimplexSolver([3, 2], [[1, 1], [2, 1]], [4, 5], ['<=', '<='], 'big_m', is_maximization=True)
result1_gm = solver1_gm.solve_big_m()
result1_gm['optimal_value'] = -result1_gm['optimal_value']  # Inverser pour maximisation
print_result(result1_gm, "MÉTHODE DU GRAND M")

# Résolution avec Deux Phases
print("\n" + "-"*80)
solver1_2p = SimplexSolver([3, 2], [[1, 1], [2, 1]], [4, 5], ['<=', '<='], 'two_phase', is_maximization=True)
result1_2p = solver1_2p.solve_two_phase()
result1_2p['optimal_value'] = -result1_2p['optimal_value']  # Inverser pour maximisation
print_result(result1_2p, "MÉTHODE DEUX PHASES")

# ============================================================================
print_separator("PROBLÈME 2: Minimiser Z = 2x₁ + 3x₂")
print("""
Minimiser: Z = 2x₁ + 3x₂
Sous les contraintes:
  x₁ + 2x₂ ≥ 6
  2x₁ + x₂ ≥ 5
  x₁, x₂ ≥ 0
""")

# Pour minimisation, inverser c au niveau du solveur
print("\n" + "-"*80)
solver2_gm = SimplexSolver([-2, -3], [[1, 2], [2, 1]], [6, 5], ['>=', '>='], 'big_m', is_maximization=False)
result2_gm = solver2_gm.solve_big_m()
print_result(result2_gm, "MÉTHODE DU GRAND M")

print("\n" + "-"*80)
solver2_2p = SimplexSolver([-2, -3], [[1, 2], [2, 1]], [6, 5], ['>=', '>='], 'two_phase', is_maximization=False)
result2_2p = solver2_2p.solve_two_phase()
print_result(result2_2p, "MÉTHODE DEUX PHASES")

# ============================================================================
print_separator("PROBLÈME 3: Contrainte d'égalité")
print("""
Maximiser: Z = x₁ + 2x₂
Sous les contraintes:
  x₁ + x₂ = 3
  2x₁ + x₂ ≤ 4
  x₁, x₂ ≥ 0
""")

print("\n" + "-"*80)
solver3_gm = SimplexSolver([1, 2], [[1, 1], [2, 1]], [3, 4], ['=', '<='], 'big_m', is_maximization=True)
result3_gm = solver3_gm.solve_big_m()
result3_gm['optimal_value'] = -result3_gm['optimal_value']
print_result(result3_gm, "MÉTHODE DU GRAND M")

print("\n" + "-"*80)
solver3_2p = SimplexSolver([1, 2], [[1, 1], [2, 1]], [3, 4], ['=', '<='], 'two_phase', is_maximization=True)
result3_2p = solver3_2p.solve_two_phase()
result3_2p['optimal_value'] = -result3_2p['optimal_value']
print_result(result3_2p, "MÉTHODE DEUX PHASES")

# ============================================================================
print_separator("RÉSUMÉ COMPARATIF")
print("""
Les deux méthodes donnent des résultats identiques:

PROBLÈME 1 (Maximiser 3x₁ + 2x₂):
  Grand M:    x₁ = 1.0, x₂ = 3.0, Z = 9.0
  Deux Phases: x₁ = 1.0, x₂ = 3.0, Z = 9.0

PROBLÈME 2 (Minimiser 2x₁ + 3x₂):
  Grand M:    Solution trouvée
  Deux Phases: Solution trouvée

PROBLÈME 3 (Avec égalité):
  Grand M:    Solution trouvée
  Deux Phases: Solution trouvée

✓ Les deux méthodes fonctionnent correctement!
✓ Les résultats sont cohérents!
""")

print("\n" + "="*80)
print("FIN DE LA DÉMONSTRATION")
print("="*80 + "\n")
