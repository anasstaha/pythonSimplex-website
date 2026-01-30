# BIG-M METHOD vs TWO-PHASE METHOD

## 1. TRANSFORMATION OF CONSTRAINTS

### Problem Format
```
Minimize/Maximize: Z = c₁x₁ + c₂x₂ + ... + cₙxₙ
Subject to:
  a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ  (≤, ≥, =)  b₁
  a₂₁x₁ + a₂₂x₂ + ... + a₂ₙxₙ  (≤, ≥, =)  b₂
  ...
  xᵢ ≥ 0
```

### Standard Form Transformation

#### Constraint Type ≤ (Less Than or Equal)
```
Example: x₁ + 2x₂ ≤ 5

Transformation: Add SLACK variable s₁ ≥ 0
Standard form: x₁ + 2x₂ + s₁ = 5

Code:
- Add 1 slack variable per ≤ constraint
- Slack variable coefficient = +1
- Slack variable is basic in initial basis
```

#### Constraint Type ≥ (Greater Than or Equal)
```
Example: x₁ + 2x₂ ≥ 5

Transformation: Add SURPLUS variable -s₁ ≤ 0 AND ARTIFICIAL variable a₁ ≥ 0
Standard form: x₁ + 2x₂ - s₁ + a₁ = 5

Code:
- Add 1 surplus variable per ≥ constraint (coefficient = -1)
- Add 1 artificial variable per ≥ constraint (coefficient = +1)
- Surplus is non-basic initially
- Artificial variable is basic in initial basis
```

#### Constraint Type = (Equality)
```
Example: x₁ + 2x₂ = 5

Transformation: Add ARTIFICIAL variable a₁ ≥ 0
Standard form: x₁ + 2x₂ + a₁ = 5

Code:
- No slack or surplus needed
- Add 1 artificial variable per = constraint (coefficient = +1)
- Artificial variable is basic in initial basis
```

---

## 2. SIMPLEX TABLEAU STRUCTURE

### Variables Count After Transformation
```
Total columns = Original variables + Slack variables + Artificial variables + 1 (RHS)

Example:
- Original: 2 variables (x₁, x₂)
- Constraints: 1 ≤, 1 ≥, 1 =
- Slack: 1 (from ≤)
- Surplus: 1 (from ≥)
- Artificial: 2 (from ≥ and =)
- Total: 2 + 1 + 1 + 2 = 6 variables + 1 RHS = 7 columns
- Rows: 3 constraints + 1 objective = 4 rows
```

### Initial Tableau Structure
```
     | x₁  x₂  s₁  -s₂  a₁  a₂ | RHS
-----|------------------------------|-----
  1  | a₁₁ a₁₂  1   0   0   0  | b₁
  2  | a₂₁ a₂₂  0  -1   1   0  | b₂
  3  | a₃₁ a₃₂  0   0   0   1  | b₃
Z   | -c₁ -c₂  0   0   ?   ?  | 0
```

### Objective Row in Different Methods

#### TWO-PHASE METHOD - PHASE 1
```
Minimize: Sum of artificial variables = 0·x₁ + 0·x₂ + ... + 1·a₁ + 1·a₂

Objective coefficients: [0, 0, ..., 0, 1, 1, ...]
                         ↑ original vars    ↑ artificial vars

In tableau (negated): [0, 0, ..., 0, -1, -1, ...| initial RHS]

CRITICAL: Before solving, adjust objective row so basic variables have coefficient 0
For each artificial var that is basic:
  objective_row -= constraint_row_where_artificial_is_basic
```

#### BIG-M METHOD
```
Minimize: Z = c₁x₁ + c₂x₂ + ... + M·a₁ + M·a₂

Where M = very large number (e.g., 10^6 or larger than sum of all coefficients)

Objective coefficients: [c₁, c₂, ..., M, M, ...]
                         ↑ original          ↑ artificial with penalty M

In tableau (negated): [-c₁, -c₂, ..., -M, -M, ...| 0]

CRITICAL: Before solving, adjust objective row so basic variables have coefficient 0
For each artificial var that is basic:
  objective_row -= M * constraint_row_where_artificial_is_basic
```

---

## 3. PHASE 1 AND PHASE 2 (TWO-PHASE METHOD)

### PHASE 1: Find Feasible Basic Solution

**Objective:** Minimize sum of artificial variables

**Why:** If we can make all artificial variables = 0, we have a feasible solution
         If sum > 0, problem is infeasible

**Steps:**
1. Set up tableau with artificial variable minimization objective
2. Adjust objective row to canonical form (basic vars = 0)
3. Run simplex algorithm
4. If optimal value > 0: INFEASIBLE
5. If optimal value = 0: Remove artificial columns, go to Phase 2

**Example:**
```
Minimize: a₁ + a₂
Subject to:
  x₁ + x₂ - s₁ + a₁ = 5  (from x₁ + x₂ ≥ 5)
  x₁ + 2x₂ + a₂ = 3      (from x₁ + 2x₂ = 3)
  x₁, x₂, s₁, a₁, a₂ ≥ 0

Initial basis: a₁, a₂
Initial tableau before adjustment:
  | x₁  x₂  -s₁  a₁  a₂ | RHS
--|----------------------------|----
1 |  1   1  -1   1   0  |  5
2 |  1   2   0   0   1  |  3
Z | -1  -1   0  -1  -1  |  0

After canonical form (subtract row 1 and row 2 from Z):
  | x₁  x₂  -s₁  a₁  a₂ | RHS
--|----------------------------|----
1 |  1   1  -1   1   0  |  5
2 |  1   2   0   0   1  |  3
Z | -2  -3   1   0   0  | -8

Run simplex until:
- All coefficients in objective row are ≥ 0
- AND optimal value = 0
```

### PHASE 2: Optimize Original Objective

**Objective:** Minimize/Maximize original objective function

**Prerequisites:**
1. Phase 1 must have found optimal value = 0
2. Artificial variables now have value 0
3. Use basis from Phase 1

**Steps:**
1. Take final tableau from Phase 1
2. Remove artificial variable columns
3. Replace objective row with original objective
4. Adjust objective row to canonical form
5. Run simplex algorithm until optimal

**Example (continuing above):**
```
After Phase 1, suppose:
- x₁ = 2, x₂ = 1, s₁ = 0, a₁ = 0, a₂ = 0

Phase 2: Minimize: Z = 3x₁ + 2x₂

New objective: [3, 2, 0]
In tableau: [-3, -2, 0 | 0]

Adjust to canonical form:
(basis variables are x₁=2, x₂=1)
objective_row -= (-3)*row_for_x₁ - 2*row_for_x₂

Run simplex until optimal
```

---

## 4. BIG-M METHOD

### Key Difference from Two-Phase
Instead of two separate phases, use ONE phase with penalty:

**Objective:**
```
Minimize: c₁x₁ + c₂x₂ + ... + M·a₁ + M·a₂

M = sufficiently large constant (e.g., 1000000)

This penalizes artificial variables heavily:
- If artificial vars > 0, objective becomes huge
- Algorithm naturally pushes them to 0
- If optimal solution has a₁ > 0, it's infeasible
```

### Advantages & Disadvantages

**Advantages:**
- One phase instead of two
- Simpler logic
- Fewer iterations typically

**Disadvantages:**
- M value is hard to choose
- Numerical instability with very large M
- Can cause rounding errors

### When Artificial Vars Reach 0

If during simplex:
1. An artificial variable becomes non-basic (value = 0)
2. It can enter basis again? NO - once removed from basis, M penalty keeps it out
3. Continue until optimal

---

## 5. CODE IMPLEMENTATION LOGIC

### Data Structure
```python
# Problem definition
c = [c₁, c₂, ..., cₙ]          # Objective coefficients
A = [[a₁₁, a₁₂, ...],          # Constraint matrix
     [a₂₁, a₂₂, ...],
     ...]
b = [b₁, b₂, ...]              # RHS values
signs = ['<=', '>=', '=', ...]  # Constraint types
```

### Transformation Algorithm
```python
def convert_to_standard_form(c, A, b, signs):
    n_slack = count(constraint_type == '<=') + count(constraint_type == '>=')
    n_artificial = count(constraint_type == '>=') + count(constraint_type == '=')
    
    A_std = []
    slack_vars = []
    artificial_vars = []
    
    for i, sign in enumerate(signs):
        row = list(A[i])
        
        if sign == '<=':
            # Add slack variable
            row += [1 for _ in range(n_slack) if slack_count is current]
            row += [0 for _ in remaining slack vars]
            row += [0 for _ in artificial vars]
            slack_vars.append(index)
            
        elif sign == '>=':
            # Add surplus (-slack) and artificial
            row += [-1 for _ in range(n_slack) if slack_count is current]
            row += [0 for _ in remaining slack vars]
            row += [0 for _ in artificial vars]
            row += [1 for _ in range(n_artificial) if artificial_count is current]
            row += [0 for _ in remaining artificial vars]
            slack_vars.append(index)
            artificial_vars.append(index)
            
        elif sign == '=':
            # Add only artificial
            row += [0 for _ in slack vars]
            row += [1 for _ in range(n_artificial) if artificial_count is current]
            row += [0 for _ in remaining artificial vars]
            artificial_vars.append(index)
        
        A_std.append(row)
    
    return A_std, slack_vars, artificial_vars
```

### Two-Phase Algorithm
```python
def solve_two_phase(c, A_std, b, artificial_vars):
    # PHASE 1
    c_phase1 = [0]*len(c) + [0]*slack_count + [1]*artificial_count
    tableau = create_tableau(A_std, b, c_phase1)
    
    # Canonical form: make basic variables = 0 in objective
    for art_idx in artificial_vars:
        for row in range(num_constraints):
            if tableau[row, art_idx] == 1:
                tableau[-1, :] -= tableau[row, :]  # Subtract row from objective
    
    tableau = run_simplex(tableau)
    
    if tableau[-1, -1] > epsilon:  # Optimal value > 0
        return INFEASIBLE
    
    # PHASE 2
    c_phase2 = original_c + [0]*slack_count + [0]*artificial_count
    tableau[-1, :] = [-c for c in c_phase2] + [0]
    
    # Canonical form adjustment for original objective
    for each_basic_var:
        tableau[-1, :] -= objective_coefficient[var] * tableau[row_of_var, :]
    
    tableau = run_simplex(tableau)
    
    return extract_solution(tableau)
```

### Big-M Algorithm
```python
def solve_big_m(c, A_std, b, artificial_vars):
    M = 10^6  # Large penalty value
    
    # Objective with M penalty
    c_bigm = original_c + [0]*slack_count + [M]*artificial_count
    tableau = create_tableau(A_std, b, c_bigm)
    
    # Canonical form: make basic variables = 0 in objective
    for art_idx in artificial_vars:
        for row in range(num_constraints):
            if tableau[row, art_idx] == 1:
                tableau[-1, :] -= M * tableau[row, :]  # Multiply by M!
    
    tableau = run_simplex(tableau)
    
    # Check if any artificial variables are non-zero
    for art_idx in artificial_vars:
        if solution[art_idx] > epsilon:
            return INFEASIBLE
    
    return extract_solution(tableau)
```

---

## 6. NUMERICAL EXAMPLE

### Problem
```
Maximize: Z = 3x₁ + 2x₂
Subject to:
  x₁ + x₂ ≤ 4
  2x₁ + x₂ ≥ 3
  x₁, x₂ ≥ 0
```

### Transformation to Standard Form
```
Constraint 1 (≤): x₁ + x₂ + s₁ = 4
Constraint 2 (≥): 2x₁ + x₂ - s₂ + a₁ = 3

Variables: [x₁, x₂, s₁, s₂, a₁]
Indices:   [0,  1,  2,  3,  4]
```

### TWO-PHASE SOLUTION

**PHASE 1: Minimize a₁**

Initial tableau:
```
      | x₁  x₂  s₁ -s₂  a₁ | RHS
------|----------------------|----
constr1| 1   1   1   0   0  |  4
constr2| 2   1   0  -1   1  |  3
Z_ph1 | 0   0   0   0  -1  |  0

After canonical (subtract constr2 from Z):
      | x₁  x₂  s₁ -s₂  a₁ | RHS
------|----------------------|----
constr1| 1   1   1   0   0  |  4
constr2| 2   1   0  -1   1  |  3
Z_ph1 |-2  -1   0   1   0  | -3

Pivot on x₁ (most negative in row 2):
... (iterations) ...
Final: a₁ = 0, x₁ = 1, x₂ = 0, s₁ = 3, s₂ = -1
```

**PHASE 2: Maximize 3x₁ + 2x₂**

Remove a₁ column, use original objective:
```
New tableau:
      | x₁  x₂  s₁ -s₂ | RHS
------|-------------------|----
... (canonical form) ...
Z     |-3  -2   0   ?  |  0

... (pivot iterations) ...
Final: x₁ = 4, x₂ = 0, Z = 12
```

### BIG-M SOLUTION

```
Minimize: Z = -3x₁ - 2x₂ + 1000000·a₁

Initial tableau:
      | x₁    x₂    s₁  -s₂      a₁    | RHS
------|-------------------------------  |----
constr1| 1     1     1    0       0     |  4
constr2| 2     1     0   -1       1     |  3
Z     |-3    -2     0    0  -1000000   |  0

After canonical (subtract 10^6*constr2 from Z):
      | x₁    x₂    s₁    -s₂    a₁  | RHS
------|--------------------------------|----
constr1| 1     1     1      0     0   |  4
constr2| 2     1     0     -1     1   |  3
Z     |-2M-3 -M-2   0    M    0      | -3M

... (pivot iterations until optimal) ...
Final: a₁ = 0, x₁ = 4, x₂ = 0, Z = 12
```

---

## 7. KEY DIFFERENCES SUMMARY

| Aspect | Two-Phase | Big-M |
|--------|-----------|-------|
| **Phases** | 2 (separate optimization phases) | 1 (combined with penalty) |
| **Objective in phase 1** | Minimize Σ artificial | Minimize c + M·Σ artificial |
| **Iterations** | Usually more | Usually fewer |
| **Numerical stability** | Better (avoids large M) | Can have rounding issues |
| **When to use** | Recommended (standard) | Quick implementation |
| **Implementation** | More code | Simpler code |

---

## 8. CORRECT IMPLEMENTATION NOTES

### ✅ DO THIS:
- In Phase 1, minimize ONLY artificial variables
- Adjust objective row to canonical form BEFORE solving
- Check Phase 1 optimal value = 0 for feasibility
- Use original objective in Phase 2
- For Big-M, choose M > sum of all objective coefficients

### ❌ DON'T DO THIS:
- Mix the methods (Big-M should NOT call Two-Phase)
- Forget canonical form adjustment
- Use same objective row for Phase 1 and Phase 2
- Set M too small (will miss infeasibility)
- Set M too large (numerical errors)

