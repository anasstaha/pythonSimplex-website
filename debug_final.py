#!/usr/bin/env python3
"""Debug Phase 1 step by step"""

import numpy as np
from app import SimplexSolver
from copy import deepcopy

class DebugSimplex (SimplexSolver):
    def _solve_tableau(self, tableau, phase_name):
        """Override to add debugging"""
        iteration = 0
        max_iterations = 1000
        epsilon = 1e-8
        
        while iteration < max_iterations:
            print(f"\n{'='*70}")
            print(f"ITERATION {iteration}")
            print(f"{'='*70}")
            print("Tableau:")
            print(tableau)
            
            last_row = tableau[-1, :-1]
            min_coeff = np.min(last_row)
            print(f"\nObjective row: {last_row}")
            print(f"Min coefficient: {min_coeff}")
            
            if min_coeff >= -epsilon:
                print("OPTIMAL!")
                return {
                    'success': True,
                    'optimal_value': -tableau[-1, -1],
                    'iterations': iteration,
                }, tableau
            
            pivot_col = np.argmin(last_row)
            print(f"Pivot column: {pivot_col}")
            
            col = tableau[:-1, pivot_col]
            print(f"Column {pivot_col}: {col}")
            
            min_ratio = float('inf')
            pivot_row = -1
            
            for i in range(len(col)):
                if col[i] > epsilon:
                    ratio = tableau[i, -1] / col[i]
                    print(f"  Row {i}: col[{i}]={col[i]:.6f}, RHS={tableau[i, -1]:.6f}, ratio={ratio:.6f}", end="")
                    if ratio >= -epsilon and ratio < min_ratio:
                        min_ratio = ratio
                        pivot_row = i
                        print(" <- SELECTED")
                    else:
                        print()
            
            if pivot_row == -1:
                print("NO VALID PIVOT FOUND - UNBOUNDED!")
                return {
                    'success': False,
                    'message': 'Unbounded',
                }, tableau
            
            print(f"\nPivot: ({pivot_row}, {pivot_col})")
            print(f"Min ratio: {min_ratio}")
            
            # Perform pivot
            pivot_value = tableau[pivot_row, pivot_col]
            print(f"Pivot value: {pivot_value}")
            
            tableau[pivot_row, :] /= pivot_value
            
            for i in range(tableau.shape[0]):
                if i != pivot_row:
                    factor = tableau[i, pivot_col]
                    tableau[i, :] -= factor * tableau[pivot_row, :]
            
            iteration += 1
            if iteration > 10:
                break
        
        return {'success': False, 'message': 'Max iterations'}, tableau

# Test
c = [-2, -3]
A = [[1, 1], [1, 0], [0, 1]]
b = [5, 1, 1]
signs = ['<=', '>=', '>=']

solver = DebugSimplex(c, A, b, signs, is_maximization=True)
A_std, b_std = solver.convert_to_standard_form()

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

result1, final = solver._solve_tableau(deepcopy(tableau), "Phase 1")
print(f"\n\nPhase 1 Result: {result1}")
