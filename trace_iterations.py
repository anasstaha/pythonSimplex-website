from app import SimplexSolver
import numpy as np

# Solve max 3x1 + 2x2 s.t. x1+x2<=4, 2x1+x2>=3

s = SimplexSolver([3,2], [[1,1],[2,1]], [4,3], ['<=','>='], 'two_phase', True)

print(f"Initial c (before __init__): [3, 2]")
print(f"After __init__, solver.c: {s.c}")
print(f"solver.is_maximization: {s.is_maximization}")

# Now manually trace the first iterations
A_std, b_std = s.convert_to_standard_form()
print(f"\nA_std shape: {A_std.shape}")
print(f"A_std:\n{A_std}")
print(f"b_std: {b_std}")

c_std = np.concatenate([s.c, np.zeros(A_std.shape[1] - s.n_vars)])
print(f"\nc_std: {c_std}")

tableau = s._create_tableau(A_std, b_std, c_std)
print(f"\nInitial tableau:\n{tableau}")

# Now solve and see what happens
result = s.solve_two_phase()
print(f"\n=== RESULT ===")
print(f"Solution: {result['solution']}")
print(f"Z: {result['optimal_value']}")
print(f"Iterations: {result['iterations']}")
print(f"\n=== ITERATIONS HISTORY ===")
for i, iteration in enumerate(s.iterations[:min(5, len(s.iterations))]):
    print(f"\nIteration {i}: {iteration}")
