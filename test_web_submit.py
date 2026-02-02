#!/usr/bin/env python3
"""Test to diagnose the web form submission issue"""

import json
from app import app

# Create a test client
client = app.test_client()

# Test case: Maximize Z = 3x1 + 2x2
# Subject to: x1 + x2 <= 4, 2x1 + x2 >= 3

test_data = {
    'c': [3, 2],                    # Objective coefficients
    'A': [[1, 1], [2, 1]],          # Constraint matrix
    'b': [4, 3],                    # RHS
    'signs': ['<=', '>='],          # Constraint types
    'method': 'two_phase',          # Method
    'objective_type': 'max'         # Maximize
}

print("="*70)
print("TEST: Web Form Submission Simulation")
print("="*70)
print(f"Input: {json.dumps(test_data, indent=2)}")

# Send POST request
response = client.post('/solve', 
                       data=json.dumps(test_data),
                       content_type='application/json')

result = response.get_json()

print("\n" + "="*70)
print("RESPONSE FROM SOLVER:")
print("="*70)
print(f"HTTP Status: {response.status_code}")
print(f"Success: {result.get('success')}")
print(f"Solution: {result.get('solution')}")
print(f"Optimal Value: {result.get('optimal_value')}")
print(f"Method: {result.get('method')}")
print(f"Iterations: {result.get('iterations')}")
print(f"Message: {result.get('message')}")

print("\n" + "="*70)
print("EXPECTED:")
print("="*70)
print("Solution: x1=4, x2=0 (or close to it)")
print("Optimal Value: 12")
print("Iterations: Multiple (not 1)")

if result.get('solution') and result['solution'][0] > 0.1:
    print("\n✅ SUCCESS: Non-zero solution found!")
else:
    print("\n❌ FAILURE: Still returning zero solution")
