from app import SimplexSolver

# Maximize 3x1 + 2x2 subject to x1+x2<=4, 2x1+x2>=3
# Endpoint negates c and passes is_maximization=True
# Solver.__init__ then negates again, so self.c = -(-c) = c = [3, 2]

print("Test: Passing c=[3,2] with is_maximization=True")
s = SimplexSolver([3,2], [[1,1],[2,1]], [4,3], ['<=','>='], 'two_phase', True)

print(f"After __init__:")
print(f"  s.c = {s.c}")
print(f"  s.is_maximization = {s.is_maximization}")
print(f"  s.c_original = {s.c_original}")

r = s.solve_two_phase()
print(f"\nResult:")
print(f"  Success: {r['success']}")
print(f"  Solution: {r['solution']}")
print(f"  Optimal value: {r['optimal_value']}")
