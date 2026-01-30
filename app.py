from flask import Flask, render_template, request, jsonify
import numpy as np
from copy import deepcopy

app = Flask(__name__)

class SimplexSolver:
    """Classe pour résoudre les problèmes de programmation linéaire avec le simplexe"""
    
    def __init__(self, c, A, b, signs, method='big_m', is_maximization=True):
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.signs = signs
        self.method = method
        self.is_maximization = is_maximization
        self.n_vars = len(c)
        self.n_constraints = len(b)
        self.iterations = []
        self.artificial_vars = []
        self.slack_vars = []
        self.tableau_history = []
        
    def convert_to_standard_form(self):
        """
        Convertir le problème à la forme standard.
        
        Stratégie:
        - Pour <=: ajouter slack positive s >= 0
        - Pour >=: ajouter slack négative -s et variable artificielle a
        - Pour =: ajouter variable artificielle a
        """
        n_slack = sum(1 for sign in self.signs if sign in ['<=', '>='])
        n_artificial = sum(1 for sign in self.signs if sign in ['>=', '='])
        
        A_std = []
        self.slack_vars = []
        self.artificial_vars = []
        slack_count = 0
        artificial_count = 0
        
        for i, sign in enumerate(self.signs):
            row = list(self.A[i])
            
            if sign == '<=':
                # x1 + x2 <= 4 devient x1 + x2 + s1 = 4
                for j in range(n_slack):
                    if j == slack_count:
                        row.append(1)
                    else:
                        row.append(0)
                slack_count += 1
                for j in range(n_artificial):
                    row.append(0)
                self.slack_vars.append(self.n_vars + slack_count - 1)
                
            elif sign == '>=':
                # x1 + x2 >= 4 devient x1 + x2 - s1 + a1 = 4
                # Slack s1 est négative initalement (s1 = 0 => x1 + x2 = 4, mais on veut >= 4)
                # Donc on ajoute une variable artificielle a1 pour la base initiale
                for j in range(n_slack):
                    if j == slack_count:
                        row.append(-1)
                    else:
                        row.append(0)
                slack_count += 1
                self.slack_vars.append(self.n_vars + slack_count - 1)
                
                # Ajouter variable artificielle
                for j in range(n_artificial):
                    if j == artificial_count:
                        row.append(1)
                    else:
                        row.append(0)
                artificial_count += 1
                self.artificial_vars.append(self.n_vars + n_slack + artificial_count - 1)
                
            elif sign == '=':
                # x1 + x2 = 3 reste x1 + x2 = 3
                # Pas de slack, seulement variable artificielle
                for j in range(n_slack):
                    row.append(0)
                    
                for j in range(n_artificial):
                    if j == artificial_count:
                        row.append(1)
                    else:
                        row.append(0)
                artificial_count += 1
                self.artificial_vars.append(self.n_vars + n_slack + artificial_count - 1)
            
            A_std.append(row)
        
        return np.array(A_std, dtype=float), self.b.copy()
    
    def solve_big_m(self):
        """
        Big-M Method: Single phase approach with penalty on artificial variables.
        
        Minimize: c₁x₁ + ... + cₙxₙ + M·a₁ + M·a₂ + ...
        
        Where M is a very large penalty (avoids multiple phases)
        """
        A_std, b_std = self.convert_to_standard_form()
        n_cols = A_std.shape[1]
        
        # Calculate M: must be larger than any coefficient in the problem
        M = max(abs(self.c)) * 1000 + 1000  # Large penalty value
        
        # Create objective: original coefficients + M penalty for artificial variables
        c_bigm = [0] * n_cols
        for i in range(self.n_vars):
            c_bigm[i] = self.c[i]
        
        # Add M penalty for each artificial variable
        for idx in self.artificial_vars:
            c_bigm[idx] = M
        
        c_bigm = np.array(c_bigm, dtype=float)
        
        tableau = self._create_tableau(A_std, b_std, c_bigm)
        
        # IMPORTANT: Normalize the objective row (canonical form)
        # For each artificial variable that is basic, subtract its row from objective row
        for artificial_idx in self.artificial_vars:
            for row_idx in range(tableau.shape[0] - 1):
                if abs(tableau[row_idx, artificial_idx] - 1.0) < 1e-10:
                    # This artificial variable is basic
                    # Subtract this row from objective row (weighted by M)
                    tableau[-1, :-1] -= M * tableau[row_idx, :-1]
                    tableau[-1, -1] -= M * tableau[row_idx, -1]
                    break
        
        result, final_tableau = self._solve_tableau(deepcopy(tableau), "Big-M - Single Phase")
        
        if result.get('success'):
            solution = self._extract_solution(final_tableau)
            
            # Check if any artificial variables are non-zero (indicates infeasibility)
            for art_idx in self.artificial_vars:
                col = final_tableau[:-1, art_idx]
                # Check if this variable is basic and non-zero
                if np.count_nonzero(col) == 1:
                    i = np.where(col != 0)[0][0]
                    if abs(col[i] - 1.0) < 1e-10:
                        value = final_tableau[i, -1]
                        if value > 1e-6:
                            return {
                                'success': False,
                                'message': f'Aucune solution réalisable trouvée (artificial var > 0: {value:.6f})'
                            }
            
            return {
                'success': True,
                'solution': solution.tolist(),
                'optimal_value': float(result.get('optimal_value', 0)),
                'iterations': len(self.iterations),
                'method': 'Big-M',
                'message': 'Solution optimale trouvée'
            }
        
        return result
    
    def solve_two_phase(self):
        """Méthode à deux phases"""
        A_std, b_std = self.convert_to_standard_form()
        n_cols = A_std.shape[1]
        
        # Phase 1 : Minimiser la somme des variables artificielles
        if self.artificial_vars:
            # Créer la fonction objectif pour la phase 1
            c_phase1 = [0] * n_cols
            for idx in self.artificial_vars:
                c_phase1[idx] = 1
            c_phase1 = np.array(c_phase1, dtype=float)
            
            tableau = self._create_tableau(A_std, b_std, c_phase1)
            
            # IMPORTANT: Normalize the objective row so that basic variables have coefficient 0
            # This is done by subtracting the constraint rows from the objective row
            # BUT: Do NOT subtract the RHS (last column) to avoid changing the objective value
            for artificial_idx in self.artificial_vars:
                # Find the row where this artificial variable is basic (has coefficient 1)
                for row_idx in range(tableau.shape[0] - 1):  # Exclude objective row
                    if abs(tableau[row_idx, artificial_idx] - 1.0) < 1e-10:
                        # This artificial variable is basic in row_idx
                        # Subtract this row from the objective row, except for the RHS part
                        tableau[-1, :-1] -= tableau[row_idx, :-1]
                        tableau[-1, -1] -= tableau[row_idx, -1]  # Also subtract RHS to maintain canonical form
                        break
            
            result1, tableau_phase1 = self._solve_tableau(deepcopy(tableau), "Phase 1 - Minimiser variables artificielles")
            
            # Vérifier si une solution de base réalisable existe
            optimal_value_phase1 = float(result1.get('optimal_value', 0))
            if optimal_value_phase1 > 1e-6:
                return {
                    'success': False,
                    'message': f'Aucune solution réalisable trouvée. Somme des variables artificielles = {optimal_value_phase1:.6f}'
                }
            
            # Phase 2 : Résoudre le problème original
            c_phase2 = np.concatenate([self.c, np.zeros(n_cols - self.n_vars)])
            
            # Utiliser le tableau final de la phase 1 comme base pour la phase 2
            tableau_phase2 = deepcopy(tableau_phase1)
            # Remplacer la ligne de la fonction objectif par celle de la phase 2
            tableau_phase2[-1, :-1] = -c_phase2
            tableau_phase2[-1, -1] = 0
            
            # CRITICAL FIX: Adjust Phase 2 objective row to canonical form
            # For each variable that is basic in the Phase 1 solution, make its coefficient 0
            for col_idx in range(n_cols):
                # Check if this column is a basic variable
                col = tableau_phase2[:-1, col_idx]
                if np.count_nonzero(col) == 1:
                    # Check if the non-zero element is exactly 1
                    row_idx = np.where(col != 0)[0][0]
                    if abs(col[row_idx] - 1.0) < 1e-10:
                        # This is a basic variable
                        coeff = tableau_phase2[-1, col_idx]
                        if abs(coeff) > 1e-10:
                            # Make its coefficient 0 in the objective row
                            tableau_phase2[-1, :] -= coeff * tableau_phase2[row_idx, :]
            
            # Adapter le tableau pour la phase 2 (éliminer les variables artificielles)
            result2, final_tableau = self._solve_tableau(tableau_phase2, "Phase 2 - Résoudre le problème original")
            
            if result2.get('success'):
                solution = self._extract_solution(final_tableau)
                    
                return {
                    'success': True,
                    'solution': solution.tolist(),
                    'optimal_value': float(result2.get('optimal_value', 0)),
                    'iterations': len(self.iterations),
                    'method': 'Deux Phases',
                    'message': 'Solution optimale trouvée'
                }
            return result2
        else:
            # Pas de variables artificielles, résoudre directement
            c_std = np.concatenate([self.c, np.zeros(A_std.shape[1] - self.n_vars)])
            tableau = self._create_tableau(A_std, b_std, c_std)
            result, final_tableau = self._solve_tableau(tableau, "Phase 1 - Unique")
            
            if result.get('success'):
                solution = self._extract_solution(final_tableau)
                    
                return {
                    'success': True,
                    'solution': solution.tolist(),
                    'optimal_value': float(result.get('optimal_value', 0)),
                    'iterations': len(self.iterations),
                    'method': 'Deux Phases',
                    'message': 'Solution optimale trouvée'
                }
            return result
    
    def _create_tableau(self, A, b, c):
        """Créer le tableau du simplexe initial"""
        m, n = A.shape
        tableau = np.zeros((m + 1, n + 1), dtype=float)
        tableau[:m, :n] = A
        tableau[:m, n] = b
        tableau[m, :n] = -c
        tableau[m, n] = 0
        return tableau
    
    def _solve_tableau(self, tableau, phase_name):
        """Résoudre le tableau du simplexe"""
        iteration = 0
        max_iterations = 1000
        epsilon = 1e-8  # Increased from 1e-10 for numerical stability
        
        while iteration < max_iterations:
            # Sauvegarder l'itération
            self.tableau_history.append({
                'iteration': iteration,
                'phase': phase_name,
                'tableau': tableau.copy()
            })
            self.iterations.append(iteration)
            
            # Vérifier l'optimalité (tous les coefficients de la ligne de Z >= 0)
            # Pour la minimisation, la ligne est -c, et nous voulons que tous les coefficients soient >= 0
            last_row = tableau[-1, :-1]
            # IMPORTANT: Use a smaller threshold (like -epsilon instead of >= -epsilon)
            # Check if minimum coefficient is close to zero or positive
            min_coeff = np.min(last_row)
            if min_coeff >= -epsilon:
                # Solution optimale trouvée
                solution = self._extract_solution(tableau)
                optimal_value = -tableau[-1, -1]
                
                return {
                    'success': True,
                    'solution': solution,
                    'optimal_value': optimal_value,
                    'iterations': iteration,
                    'message': 'Solution optimale trouvée'
                }, tableau
            
            # Choisir la colonne du pivot (le coefficient le plus négatif)
            pivot_col = np.argmin(last_row)
            
            # Choisir la ligne du pivot avec le test du rapport minimum
            col = tableau[:-1, pivot_col]
            min_ratio = float('inf')
            pivot_row = -1
            
            # IMPORTANT: Pour une variable entrant dans la base:
            # - Si son coefficient dans une contrainte est POSITIF: ratio = RHS / coefficient >= 0
            # - Si son coefficient est NEGATIF: on ne peut pas utiliser cette ligne (augmenter rendrait RHS negatif)
            # Le test du rapport minimum DOIT utiliser seulement des coefficients avec le même signe que on veut
            for i in range(len(col)):
                if col[i] > epsilon:  # Coefficient positif
                    ratio = tableau[i, -1] / col[i]
                    if ratio >= -epsilon:  # Ratio >= 0 (or close to 0 for degeneracy)
                        if ratio < min_ratio:
                            min_ratio = ratio
                            pivot_row = i
            
            # Vérifier si le problème est non borné
            if pivot_row == -1:
                # Aucun coefficient positif -> la variable peut augmenter indéfiniment
                return {
                    'success': False,
                    'message': 'Le problème est non borné'
                }, tableau
            
            # Effectuer le pivot (Gauss-Jordan)
            pivot_value = tableau[pivot_row, pivot_col]
            tableau[pivot_row, :] /= pivot_value
            
            for i in range(tableau.shape[0]):
                if i != pivot_row:
                    factor = tableau[i, pivot_col]
                    tableau[i, :] -= factor * tableau[pivot_row, :]
            
            iteration += 1
        
        return {
            'success': False,
            'message': f'Nombre maximum d\'itérations ({max_iterations}) atteint'
        }, tableau
    
    def _extract_solution(self, tableau):
        """Extraire la solution du tableau final"""
        m, n = tableau.shape
        m -= 1  # Enlever la ligne de la fonction objectif
        solution = np.zeros(self.n_vars, dtype=float)
        
        # Identifier les variables de base
        for j in range(self.n_vars):
            col = tableau[:m, j]
            # Une variable de base a exactement un 1 et des 0 dans sa colonne
            if np.count_nonzero(col) == 1:
                i = np.where(col != 0)[0][0]
                if abs(col[i] - 1.0) < 1e-10:
                    solution[j] = tableau[i, -1]
        
        return solution



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fonction')
def fonction():
    n_vars = request.args.get('variables', 1, type=int)
    n_constraints = request.args.get('contraintes', 1, type=int)
    method = request.args.get('method', 'big_m')
    
    return render_template('fonction.html',
                         n_vars=n_vars,
                         n_constraints=n_constraints,
                         method=method)


@app.route('/resultat')
def resultat():
    return render_template('resultat.html')


@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    
    c = data.get('c', [])
    A = data.get('A', [])
    b = data.get('b', [])
    signs = data.get('signs', [])
    method = data.get('method', 'big_m')
    objective_type = data.get('objective_type', 'max')
    
    try:
        # Valider les entrées
        if not c or not A or not b or not signs:
            return jsonify({'success': False, 'message': 'Données incomplètes'}), 400
        
        # Convertir en tableaux numpy
        c = np.array(c, dtype=float)
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        
        # Déterminer si c'est une maximisation ou minimisation
        is_maximization = (objective_type == 'max')
        
        # IMPORTANT: L'algorithme du simplexe minimise toujours
        # Pour maximisation: minimiser -c, puis inverser le résultat
        # Pour minimisation: minimiser c directement
        if is_maximization:
            c = -c
        
        # Valider les dimensions
        if A.shape[0] != len(b) or A.shape[1] != len(c):
            return jsonify({'success': False, 'message': 'Dimensions incompatibles'}), 400
        
        # Valider les signes
        for sign in signs:
            if sign not in ['<=', '>=', '=']:
                return jsonify({'success': False, 'message': f'Signe invalide: {sign}'}), 400
        
        # Gérer les valeurs b négatives - nécessite inversion de l'inégalité
        for i in range(len(b)):
            if b[i] < 0:
                A[i] = -A[i]
                b[i] = -b[i]
                # Inverser le signe
                if signs[i] == '<=':
                    signs[i] = '>='
                elif signs[i] == '>=':
                    signs[i] = '<='
                # '=' reste '='
        
        # Résoudre
        solver = SimplexSolver(c.tolist(), A.tolist(), b.tolist(), signs, method, is_maximization)
        
        if method == 'big_m':
            result = solver.solve_big_m()
        else:
            result = solver.solve_two_phase()
        
        # Inverser la valeur optimale si c'était une MAXIMISATION (car on a minimisé -c)
        if result.get('success') and is_maximization:
            result['optimal_value'] = -result['optimal_value']
        
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'success': False, 'message': f'Erreur de valeur: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erreur: {str(e)}'}), 400


if __name__ == '__main__':
    app.run(debug=True)
