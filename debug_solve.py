#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug de _solve_tableau
"""

from app import SimplexSolver
import numpy as np

c = [5, 9, 14]
A = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
b = [3, 104, 37]
signs = ['>=', '>=', '>=']

solver = SimplexSolver(c, A, b, signs, 'big_m', is_maximization=False)

result = solver.solve_big_m()
print(f"Resultat: {result}")
