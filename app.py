from flask import Flask, request, render_template
import re
from scipy.optimize import linprog

app = Flask(__name__)


# --- Parser simple pour fonction objectif (ex: 0.2x1 + 0.1x2 - 3x3) ---
def parse_objective(text):
    if not text:
        return []
    s = text.replace('−', '-').replace(' ', '')
    pattern = re.compile(r'([+-]?\d*\.?\d*)(?:\s*)x(\d+)', flags=re.IGNORECASE)
    coeffs = {}
    for m in pattern.finditer(s):
        coef_str = m.group(1)
        idx = int(m.group(2))
        if coef_str in ('', '+'):
            coef = 1.0
        elif coef_str == '-':
            coef = -1.0
        else:
            coef = float(coef_str)
        coeffs[idx] = coef
    # convert dict to list ordered by index
    if not coeffs:
        return []
    max_idx = max(coeffs.keys())
    return [coeffs.get(i, 0.0) for i in range(1, max_idx + 1)]


def parse_constraints(text):
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    parsed = []
    pattern = re.compile(r'([+-]?\d*\.?\d*)x(\d+)', flags=re.IGNORECASE)
    for ln in lines:
        if '<=' in ln:
            left, right = ln.split('<=', 1)
            sense = '<='
        elif '>=' in ln:
            left, right = ln.split('>=', 1)
            sense = '>='
        elif '=' in ln:
            left, right = ln.split('=', 1)
            sense = '='
        else:
            continue
        s = left.replace(' ', '').replace('−', '-')
        coeffs = {}
        for m in pattern.finditer(s):
            coef_str = m.group(1)
            idx = int(m.group(2))
            if coef_str in ('', '+'):
                coef = 1.0
            elif coef_str == '-':
                coef = -1.0
            else:
                coef = float(coef_str)
            coeffs[idx] = coef
        try:
            rhs = float(right.strip())
        except:
            rhs = None
        
        # Validate constraint
        if not coeffs or rhs is None:
            parsed.append({'coeffs': coeffs, 'sense': sense, 'rhs': rhs, 'raw': ln, 'valid': False})
        else:
            parsed.append({'coeffs': coeffs, 'sense': sense, 'rhs': rhs, 'raw': ln, 'valid': True})
    return parsed


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fonction', methods=['GET', 'POST'])
def fonction():
    from flask import make_response
    
    if request.method == 'POST':
        # Read form values
        problem_type = request.form.get('type', 'max')
        method = request.form.get('method', '')
        objective_text = request.form.get('objective', '') or ''
        constraints_text = request.form.get('constraints', '') or ''
        
        # DEBUG: Log incoming form data
        print(f"\n=== DEBUG POST DATA ===")
        print(f"problem_type: {problem_type}")
        print(f"objective_text: '{objective_text}'")
        print(f"constraints_text: '{constraints_text}'")
        print(f"========================\n")

        # Basic validation: require objective and constraints
        if not objective_text.strip() or not constraints_text.strip():
            error = 'Veuillez saisir la fonction objectif et les contraintes avant de continuer.'
            resp = make_response(render_template('fonction.html', method_selected=problem_type,
                                   objective_text=objective_text,
                                   constraints_text=constraints_text,
                                   error=error))
            resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            resp.headers['Pragma'] = 'no-cache'
            resp.headers['Expires'] = '0'
            return resp

        obj = parse_objective(objective_text)
        cons_parsed = parse_constraints(constraints_text)
        
        # Validate parsed data
        if not obj:
            error = 'Format de fonction objectif invalide. Utilise : 2x1 + 3x2 - x3'
            resp = make_response(render_template('fonction.html', method_selected=problem_type,
                                   objective_text=objective_text,
                                   constraints_text=constraints_text,
                                   error=error))
            resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            resp.headers['Pragma'] = 'no-cache'
            resp.headers['Expires'] = '0'
            return resp
        
        # Filter valid constraints
        cons_parsed = [c for c in cons_parsed if c.get('valid', True)]
        if not cons_parsed:
            error = 'Aucune contrainte valide trouvée. Format attendu : x1 + 2x2 <= 100'
            resp = make_response(render_template('fonction.html', method_selected=problem_type,
                                   objective_text=objective_text,
                                   constraints_text=constraints_text,
                                   error=error))
            resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            resp.headers['Pragma'] = 'no-cache'
            resp.headers['Expires'] = '0'
            return resp

        # build matrices for linprog
        A_ub, b_ub, A_eq, b_eq = [], [], [], []
        # determine number of variables from objective or constraints
        n = len(obj) if obj else 0
        for c in cons_parsed:
            if c['coeffs']:
                n = max(n, max(c['coeffs'].keys()))
        
        # build coefficient rows (skip invalid constraints)
        for c in cons_parsed:
            if c['coeffs'] and c['rhs'] is not None:
                row = [c['coeffs'].get(i, 0.0) for i in range(1, n + 1)]
                if c['sense'] == '<=':
                    A_ub.append(row); b_ub.append(c['rhs'])
                elif c['sense'] == '>=':
                    A_ub.append([-x for x in row]); b_ub.append(-c['rhs'])
                elif c['sense'] == '=':
                    A_eq.append(row); b_eq.append(c['rhs'])

        c = obj + [0.0] * (n - len(obj))
        if problem_type.lower() == 'max':
            c = [-x for x in c]
        
        # Add bounds for non-negativity: each variable x_i >= 0
        bounds = [(0, None) for _ in range(n)]

        try:
            res = linprog(c=c, A_ub=A_ub or None, b_ub=b_ub or None,
                          A_eq=A_eq or None, b_eq=b_eq or None, 
                          bounds=bounds, method='highs')
            if res.success:
                Z = -res.fun if problem_type.lower() == 'max' else res.fun
                # Format solution with reasonable precision
                x_vals = [round(v, 6) for v in res.x.tolist()]
                
                # Build formatted result for display
                result_data = {
                    'success': True,
                    'objective_type': 'MAXIMISER' if problem_type.lower() == 'max' else 'MINIMISER',
                    'objective': objective_text,
                    'constraints': constraints_text,
                    'variables': [f'x{i+1}' for i in range(len(x_vals))],
                    'values': x_vals,
                    'Z': round(Z, 6),
                    'message': f'Solution optimale trouvée'
                }
            else:
                result_data = {
                    'success': False,
                    'message': f"Pas de solution optimale : {res.message}"
                }
        except Exception as e:
            result_data = {
                'success': False,
                'message': f"Erreur lors du calcul : {str(e)}"
            }
        
        # DEBUG: Log result
        print(f"\n=== DEBUG RESULT ===")
        print(f"result_data: {result_data}")
        print(f"===================\n")

        resp = make_response(render_template('resultat.html', result=result_data))
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
        return resp

    # GET: prefill fonction form if query params provided
    # Prefill fonction form when coming from index (GET params)
    method_selected = request.args.get('method', '')
    variables = request.args.get('variables', '')
    contraintes = request.args.get('contraintes', '')
    # Pass counts so template can optionally use them
    resp = make_response(render_template('fonction.html', method_selected=method_selected,
                           objective_text='', constraints_text='',
                           variables_count=variables, contraintes_count=contraintes,
                           error=None))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp


if __name__ == '__main__':
    app.run(debug=True)