document.getElementById('build').addEventListener('click', () => {
  const n = parseInt(document.getElementById('num_vars').value);
  const m = parseInt(document.getElementById('num_cons').value);

  const objDiv = document.getElementById('obj_coeffs');
  objDiv.innerHTML = '';
  for (let i = 1; i <= n; i++) {
    const inp = document.createElement('input');
    inp.type = 'number';
    inp.step = 'any';
    inp.value = '0';
    inp.id = `obj_${i}`;
    inp.placeholder = `x${i}`;
    objDiv.appendChild(document.createTextNode(`x${i}: `));
    objDiv.appendChild(inp);
    objDiv.appendChild(document.createTextNode(' '));
  }

  const consArea = document.getElementById('constraints_area');
  consArea.innerHTML = '';
  for (let r = 1; r <= m; r++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'constraint';
    rowDiv.innerHTML = `<strong>Contr ${r} :</strong> `;
    for (let j = 1; j <= n; j++) {
      const inp = document.createElement('input');
      inp.type = 'number';
      inp.step = 'any';
      inp.value = '0';
      inp.id = `c${r}_${j}`;
      inp.style.width = '60px';
      rowDiv.appendChild(document.createTextNode(` x${j} * `));
      rowDiv.appendChild(inp);
    }
    // signe
    const sel = document.createElement('select');
    sel.id = `sign_${r}`;
    sel.innerHTML = `<option value="<=">&le;</option><option value=">=">&ge;</option><option value="=">=</option>`;
    rowDiv.appendChild(sel);
    // RHS
    const rhs = document.createElement('input');
    rhs.type = 'number';
    rhs.step = 'any';
    rhs.value = '0';
    rhs.id = `rhs_${r}`;
    rhs.style.width = '80px';
    rowDiv.appendChild(document.createTextNode(' RHS: '));
    rowDiv.appendChild(rhs);

    consArea.appendChild(rowDiv);
  }

  document.getElementById('problem').style.display = 'block';
});

document.getElementById('send').addEventListener('click', () => {
  const n = parseInt(document.getElementById('num_vars').value);
  const m = parseInt(document.getElementById('num_cons').value);
  const method = document.getElementById('method_select').value;
  const obj_type = document.getElementById('obj_type').value;

  const obj_coeffs = [];
  for (let i = 1; i <= n; i++) {
    obj_coeffs.push(parseFloat(document.getElementById(`obj_${i}`).value || 0));
  }

  const constraints = [];
  for (let r = 1; r <= m; r++) {
    const coeffs = [];
    for (let j = 1; j <= n; j++) {
      coeffs.push(parseFloat(document.getElementById(`c${r}_${j}`).value || 0));
    }
    const sign = document.getElementById(`sign_${r}`).value;
    const rhs = parseFloat(document.getElementById(`rhs_${r}`).value || 0);
    constraints.push({coeffs, sign, rhs});
  }

  const payload = {
    method,
    num_vars: n,
    constraints,
    objective: {coeffs: obj_coeffs, type: obj_type}
  };

  fetch('/solve', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(displayTable)
  .catch(err => {
    document.getElementById('result_area').innerText = 'Erreur: ' + err;
  });
});

function displayTable(data) {
  const headers = data.headers;
  const table = data.table;
  const obj = data.objective_row;

  let html = '<table border="1" cellpadding="6"><thead><tr>';
  headers.forEach(h => html += `<th>${h}</th>`);
  html += '</tr></thead><tbody>';

  table.forEach(row => {
    html += '<tr>';
    row.forEach(cell => {
      html += `<td>${Number(cell).toFixed(3)}</td>`;
    });
    html += '</tr>';
  });

  // Ligne objectif (affichage)
  html += '<tr style="background:#eef"><td colspan="' + (headers.length-1) + '"><strong>Objectif (coeffs)</strong></td>';
  html += `<td>${obj[obj.length-1].toFixed(3)}</td></tr>`;

  html += '</tbody></table>';
  document.getElementById('result_area').innerHTML = html;
}
