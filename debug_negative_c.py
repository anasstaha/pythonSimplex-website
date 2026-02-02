from app import SimplexSolver
import numpy as np

# Simulate what endpoint does for maximization
c_original = [3, 2]
A = [[1,1], [2,1]]
b = [4, 3]
signs = ['<=', '>=']

# Endpoint negates for maximization
c_for_solver = c_original  # Don't negate here anymore
print(f"Original c: {c_original}")
print(f"c for solver (no negation): {c_for_solver}")

# Create solver with is_maximization=True
solver = SimplexSolver(c_for_solver, A, b, signs, 'two_phase', True)

# Check initial tableau
print("\n=== Before solving ===")
print(f"solver.c = {solver.c}")
print(f"solver.A = {solver.A}")
print(f"solver.b = {solver.b}")
print(f"solver.signs = {solver.signs}")

# Trace convert_to_standard_form
A_std, b_std = solver.convert_to_standard_form()
signs_std = solver.signs
print(f"\n=== After convert_to_standard_form ===")
print(f"A_std shape: {A_std.shape}")
print(f"A_std:\n{A_std}")
print(f"b_std: {b_std}")
print(f"signs_std: {signs_std}")

# Check what c_std will be
c_std = np.concatenate([solver.c, np.zeros(A_std.shape[1] - solver.n_vars)])
print(f"\nc_std: {c_std}")

# Create initial tableau
tableau = solver._create_tableau(A_std, b_std, c_std)
print(f"\nInitial tableau:\n{tableau}")
print(f"\nObjective row (last row): {tableau[-1, :]}")
print(f"Min coefficient in objective: {np.min(tableau[-1, :-1])}")
