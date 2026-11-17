// Base simulada con estado para las pruebas: responde como Supabase (PostgREST) a GET, POST, PATCH y DELETE
// sobre tablas en memoria, con los filtros que usan las páginas (eq, neq, in, is, like, lt/lte/gt/gte).
const ahora = new Date().toISOString();
function calza(f, k, v) {
  const val = f[k], txt = val == null ? null : String(val), d = x => decodeURIComponent(x);
  if (v.startsWith('eq.')) return txt === d(v.slice(3));
  if (v.startsWith('neq.')) return txt !== d(v.slice(4));
  if (v === 'is.null') return val == null;
  if (v === 'is.true') return val !== false;
  if (v.startsWith('in.(')) return v.slice(4, -1).split(',').map(x => d(x).replace(/^"|"$/g, '')).includes(txt);
  if (v.startsWith('like.')) { const re = new RegExp('^' + d(v.slice(5)).replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*') + '$'); return txt != null && re.test(txt); }
  for (const [op, fn] of [['lte.', (a, b) => a <= b], ['gte.', (a, b) => a >= b], ['lt.', (a, b) => a < b], ['gt.', (a, b) => a > b]]) if (v.startsWith(op)) return txt != null && fn(txt, d(v.slice(op.length)));
  return true;
}
const filtrar = (filas, u) => { const fs = [...u.searchParams.entries()].filter(([k]) => !['select', 'order', 'limit', 'offset', 'or', 'on_conflict'].includes(k));
  return +u.searchParams.get('offset') > 0 ? [] : filas.filter(f => fs.every(([k, v]) => calza(f, k, v))); };
// claves de las tablas que se guardan con «merge-duplicates» (si no se indica on_conflict)
const CLAVE = { plan_proveedores_estado: ['clave'], plan_config: ['clave'], proveedores: ['id'] };
function rutaConEstado(tablas, escrituras) {
  return async r => {
    const q = r.request(), u = new URL(q.url());
    if (/\/rpc\//.test(u.pathname)) return r.fallback();
    const t = u.pathname.split('/').pop(), m = q.method();
    if (!tablas[t]) return m === 'GET' ? r.fulfill({ contentType: 'application/json', body: '[]' }) : r.fulfill({ status: 201, body: '' });
    if (m === 'GET') return r.fulfill({ contentType: 'application/json', body: JSON.stringify(filtrar(tablas[t], u)) });
    const body = q.postData() ? JSON.parse(q.postData()) : null;
    if (escrituras) escrituras.push({ t, m, q: decodeURIComponent(u.search), body });
    if (m === 'PATCH') { filtrar(tablas[t], u).forEach(f => Object.assign(f, body)); return r.fulfill({ status: 204, body: '' }); }
    if (m === 'DELETE') { const fuera = new Set(filtrar(tablas[t], u)); const quedan = tablas[t].filter(f => !fuera.has(f)); tablas[t].length = 0; tablas[t].push(...quedan); return r.fulfill({ status: 204, body: '' }); }
    const claves = (u.searchParams.get('on_conflict') || '').split(',').filter(Boolean), k = claves.length ? claves : CLAVE[t];
    const nuevas = [].concat(body).map(x => { const ya = k && tablas[t].find(y => k.every(c => String(y[c] ?? '') === String(x[c] ?? '')));
      if (ya) return Object.assign(ya, x);
      const n = { created_at: ahora, ...x }; if (n.id == null) n.id = Math.max(0, ...tablas[t].map(y => +y.id || 0)) + 1; tablas[t].push(n); return n; });
    return /return=representation/.test(q.headers()['prefer'] || '') ? r.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(nuevas) }) : r.fulfill({ status: 201, body: '' });
  };
}
module.exports = { rutaConEstado, filtrar };
