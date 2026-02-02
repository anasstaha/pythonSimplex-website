from app import SimplexSolver
import numpy as np

s = SimplexSolver([-3,-2], [[1,1],[2,1]], [4,3], ['<=','>='], 'two_phase', False)

# Check what Phase 1 does
A_std, b_std = s.convert_to_standard_form()

print("Standard form:")
print(f"A_std:\n{A_std}")
print(f"b_std: {b_std}")
print(f"Artificial vars indices: {s.artificial_vars}")
print(f"Slack vars indices: {s.slack_vars}")

# Manual Phase 1
c_phase1 = [0] * A_std.shape[1]
for idx in s.artificial_vars:
    c_phase1[idx] = 1
c_phase1 = np.array(c_phase1, dtype=float)

print(f"\nPhase 1 objective: {c_phase1}")

tableau = s._create_tableau(A_std, b_std, c_phase1)
print(f"\nInitial Phase 1 tableau before canonical form:")
print(tableau)

# Apply canonical form fix
for artificial_idx in s.artificial_vars:
    for row_idx in range(tableau.shape[0] - 1):
        if abs(tableau[row_idx, artificial_idx] - 1.0) < 1e-10:
            print(f"\nSubtracting row {row_idx} from objective row for artificial var {artificial_idx}")
            print(f"Before: {tableau[-1, :]}")
            tableau[-1, :-1] -= tableau[row_idx, :-1]
            tableau[-1, -1] -= tableau[row_idx, -1]
            print(f"After: {tableau[-1, :]}")
            break

print(f"\nFinal Phase 1 tableau:")
print(tableau)

# Check what solution Phase 1 would find
solution_basic = s._extract_solution(tableau)
print(f"\nInitial basic solution: {solution_basic}")
