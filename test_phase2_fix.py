#!/usr/bin/env python3
"""Direct test of the solver after Phase 2 fix"""

from app import SimplexSolver

# Test 1: Simple problem
print("="*70)
print("Test 1: Minimize Z = x1 + x2, x1 + x2 = 5, x1 >= 2")
print("="*70)

s = SimplexSolver([1,1], [[1,1],[1,0]], [5,2], ['=','>='], False)
r = s.solve_two_phase()

print(f"Success: {r.get('success')}")
print(f"Solution: x1={r['solution'][0]:.4f}, x2={r['solution'][1]:.4f}")
print(f"Optimal Z: {r.get('optimal_value'):.4f}")
print(f"Iterations: {r.get('iterations')}")
print(f"Expected: x1=2, x2=3, Z=5")

# Test 2: Mixed constraints
print("\n" + "="*70)
print("Test 2: Minimize Z = 2x1 + 3x2")
print("Subject to: x1 + x2 >= 5, 2x1 + x2 <= 10")
print("="*70)

s2 = SimplexSolver([2,3], [[1,1],[2,1]], [5,10], ['>=','<='], False)
r2 = s2.solve_two_phase()

print(f"Success: {r2.get('success')}")
print(f"Solution: x1={r2['solution'][0]:.4f}, x2={r2['solution'][1]:.4f}")
print(f"Optimal Z: {r2.get('optimal_value'):.4f}")
print(f"Iterations: {r2.get('iterations')}")
print(f"Expected: x1=0, x2=10 or nearby, Z=30")

# Test 3: Maximize
print("\n" + "="*70)
print("Test 3: Maximize Z = 3x1 + 2x2")
print("Subject to: x1 + x2 <= 4, 2x1 + x2 >= 3")
print("="*70)

s3 = SimplexSolver([-3,-2], [[1,1],[2,1]], [4,3], ['<=','>='], True)  # Negated for minimization
r3 = s3.solve_two_phase()

print(f"Success: {r3.get('success')}")
print(f"Solution: x1={r3['solution'][0]:.4f}, x2={r3['solution'][1]:.4f}")
print(f"Optimal Z (minimized -Z): {r3.get('optimal_value'):.4f}")
print(f"Actual Z (maximized): {-r3.get('optimal_value'):.4f}")
print(f"Iterations: {r3.get('iterations')}")
print(f"Expected: x1=4, x2=0, Z=12")
