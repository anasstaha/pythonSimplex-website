import json
from app import SimplexSolver
import numpy as np

# Simulate endpoint logic
data = {
    'c': [3, 2],
    'A': [[1, 1], [2, 1]],
    'b': [4, 3],
    'signs': ['<=', '>='],
    'method': 'two_phase',
    'objective_type': 'max'
}

c = np.array(data['c'], dtype=float)
A = np.array(data['A'], dtype=float)
b = np.array(data['b'], dtype=float)
signs = data['signs']
method = data['method']
objective_type = data['objective_type']

print(f"Original c (before endpoint logic): {c}")
print(f"objective_type: {objective_type}")

# Endpoint logic
is_maximization = (objective_type == 'max')
print(f"\nis_maximization initial: {is_maximization}")

if is_maximization:
    c = -c
    is_maximization = False

print(f"c after negation: {c}")
print(f"is_maximization after negation: {is_maximization}")

# Create solver
solver = SimplexSolver(c.tolist(), A.tolist(), b.tolist(), signs, method, is_maximization)

print(f"\nSolver created with:")
print(f"  solver.c: {solver.c}")
print(f"  solver.is_maximization: {solver.is_maximization}")

# Solve
result = solver.solve_two_phase()

print(f"\nResult from solver:")
print(f"  solution: {result['solution']}")
print(f"  optimal_value: {result['optimal_value']}")

# Apply endpoint post-processing
if objective_type == 'max':
    result['optimal_value'] = -result['optimal_value']
    
print(f"\nAfter endpoint post-processing:")
print(f"  optimal_value: {result['optimal_value']}")
