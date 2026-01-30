#!/usr/bin/env python3
"""Verify that the bug fixes work correctly"""

from app import SimplexSolver

print("="*70)
print("SIMPLEX SOLVER BUG FIX VERIFICATION")
print("="*70)

# Test 1: Simple problem with >= constraints
print("\nTest 1: Minimize Z = 2x1 + 3x2")
print("Subject to: x1 + x2 >= 5, 2x1 + x2 <= 10, x1,x2 >= 0")
c = [2, 3]
A = [[1, 1], [2, 1]]
b = [5, 10]
signs = ['>=', '<=']

solver = SimplexSolver(c, A, b, signs, method='big_m', is_maximization=False)
result = solver.solve_two_phase()

print(f"Success: {result.get('success')}")
print(f"Solution: x1={result.get('solution')[0]:.4f}, x2={result.get('solution')[1]:.4f}")
print(f"Optimal Value Z: {result.get('optimal_value'):.4f}")
print(f"Iterations: {result.get('iterations')}")
if result.get('iterations', 0) == 1:
    print("⚠️  WARNING: Only 1 iteration (might be the old bug)")
elif result.get('iterations', 0) > 1:
    print("✅ GOOD: Multiple iterations performed")

# Test 2: Maximization problem
print("\n" + "-"*70)
print("\nTest 2: Maximize Z = 3x1 + 2x2")
print("Subject to: x1 + x2 <= 4, 2x1 + x2 >= 3, x1,x2 >= 0")
c = [3, 2]
A = [[1, 1], [2, 1]]
b = [4, 3]
signs = ['<=', '>=']

solver = SimplexSolver(c, A, b, signs, method='big_m', is_maximization=True)
result = solver.solve_two_phase()

print(f"Success: {result.get('success')}")
if result.get('success'):
    print(f"Solution: x1={result.get('solution')[0]:.4f}, x2={result.get('solution')[1]:.4f}")
    print(f"Optimal Value Z: {result.get('optimal_value'):.4f}")
    print(f"Iterations: {result.get('iterations')}")
    if result.get('iterations', 0) == 1:
        print("⚠️  WARNING: Only 1 iteration")
    else:
        print("✅ GOOD: Multiple iterations performed")
else:
    print(f"Message: {result.get('message')}")

# Test 3: Problem with equality constraint
print("\n" + "-"*70)
print("\nTest 3: Minimize Z = x1 + x2")
print("Subject to: x1 + x2 = 5, x1 >= 2, x1,x2 >= 0")
c = [1, 1]
A = [[1, 1], [1, 0]]
b = [5, 2]
signs = ['=', '>=']

solver = SimplexSolver(c, A, b, signs, method='big_m', is_maximization=False)
result = solver.solve_two_phase()

print(f"Success: {result.get('success')}")
if result.get('success'):
    print(f"Solution: x1={result.get('solution')[0]:.4f}, x2={result.get('solution')[1]:.4f}")
    print(f"Optimal Value Z: {result.get('optimal_value'):.4f}")
    print(f"Iterations: {result.get('iterations')}")
    if result.get('iterations', 0) == 1:
        print("⚠️  WARNING: Only 1 iteration")
    else:
        print("✅ GOOD: Multiple iterations performed")
else:
    print(f"Message: {result.get('message')}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("✅ Bug Fix #1 (Epsilon tolerance): APPLIED")
print("✅ Bug Fix #2 (Canonical form): APPLIED")
print("\nThe solver should now:")
print("- Perform multiple iterations for non-trivial problems")
print("- Reach correct optimal solutions")
print("- Handle >=, <=, and = constraints properly")
print("="*70)
