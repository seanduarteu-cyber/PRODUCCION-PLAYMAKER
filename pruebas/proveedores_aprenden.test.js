// Gastos › Proveedores aprende de los gastos ya clasificados (SQL 24C + Ventas): cuenta habitual, reglas por palabra
// y tipo de documento; y la cuenta habitual clasifica sola los gastos nuevos. De punta a punta contra un Postgres de
// verdad, que atiende las llamadas de la página como Supabase (igual que clasif_gastos.test.js).
// Requiere Postgres local (PGHOST/PGPORT; por defecto el socket /home/postgres, puerto 5499) con los roles anon y authenticated.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const HTML = fs.readFileSync(path.resolve(__dirname, '../sistemas/ventas/index.html'));
const sql = n => fs.readFileSync(path.resolve(__dirname, '../sql/' + n), 'utf8');
const SQL21 = sql('SQL_21A_VENTAS_clasificacion_gastos.sql'), SQL21B = sql('SQL_21B_VENTAS_neto_y_socios.sql'), SQL24C = sql('SQL_24C_VENTAS_cuenta_habitual_clasifica.sql');
const PSQL = process.env.PSQL || '/usr/lib/postgresql/16/bin/psql';
const PG = ['-h', process.env.PGHOST || '/home/postgres', '-p', process.env.PGPORT || '5499', '-U', 'postgres'];
const BASE = 'ventas_prueba_24c';
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const psql = (q, db = BASE) => execFileSync(PSQL, [...PG, '-d', db, '-q', '-At', '-v', 'ON_ERROR_STOP=1'], { input: q, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
const uno = q => { const t = psql(q).split('\n').pop(); return t ? JSON.parse(t) : null; };
const lit = v => '$J$' + String(v).replace(/\$J\$/g, '') + '$J$';

// ── Gastos de prueba: [fecha, descripción, categoría, proveedor, monto, cuenta elegida por una persona, documento] ──
const G = [
  ['2026-05-02', 'ENVIOS', '', 'UBER', 5000, '2.11'],
  ['2026-05-09', 'ENVIOS', '', 'UBER', 6000, '2.11'],
  ['2026-06-02', 'ENVIOS', '', 'Uber', 7000, '2.11'],
  ['2026-06-12', 'ENVIOS CLIENTE', '', 'UBER', 5500, '2.11'],
  ['2026-07-02', 'ENVIOS', '', 'UBER', 6100, '2.11'],
  ['2026-07-05', 'UBER A TALLER DE SONIA', '', 'UBER', 8000, '3.11'],
  ['2026-07-06', 'ENVIO TALLER PAOLA', '', 'UBER', 8500, '3.11'],
  ['2026-08-06', 'TALLER SONIA', '', 'UBER', 8200, '3.11'],
  ['2026-08-07', 'UBER FRANKLIN', '', 'UBER', 4000, '5.09'],
  ['2026-10-07', 'ENVIO TALLER ROSA', 'POR IDENTIFICAR', 'UBER', 9100, null],            // 9: en revisión → regla Uber + TALLER
  ['2026-08-03', 'MENSUALIDAD', 'HERRAMIENTAS DE MARKETING', 'HEAT SUIT', 26000, null],   // 10-12: por su categoría (4.05)
  ['2026-09-03', 'MENSUALIDAD', 'HERRAMIENTAS DE MARKETING', 'HEAT SUIT', 26000, null],
  ['2026-10-03', 'MENSUALIDAD', 'HERRAMIENTAS DE MARKETING', 'HEAT SUIT', 26000, null],
  ['2026-05-10', 'TRANSFER ESCUDOS', '', 'MUNDO TRANSFER', 30000, '2.04', 'afecta'],
  ['2026-06-10', 'TRANSFER ESCUDOS', '', 'MUNDO TRANSFER', 31000, '2.04', 'afecta'],
  ['2026-07-10', 'TRANSFER NUMEROS', '', 'MUNDO TRANSFER', 32000, '2.04', 'afecta'],
  ['2026-08-10', 'TRANSFER', '', 'MUNDO TRANSFER', 33000, '2.04'],
  ['2026-10-20', 'PEDIDO OCTUBRE', 'POR IDENTIFICAR', 'MUNDO TRANSFER', 34000, null],     // 17: en revisión → cuenta habitual
  ['2026-06-30', 'SUELDO JUNIO', '', 'RODOLFO GARCIA', 500000, '3.01'],
  ['2026-07-31', 'SUELDO JULIO', '', 'RODOLFO GARCIA', 500000, '3.01'],
  ['2026-08-31', 'SUELDO AGOSTO', '', 'RODOLFO GARCIA', 500000, '3.01'],
  ['2026-07-10', 'ANTICIPO', '', 'SEAN DUARTE', 500000, '5.10'],
  ['2026-08-10', 'ANTICIPO', '', 'SEAN DUARTE', 500000, '5.10'],
  ['2026-09-10', 'ANTICIPO', '', 'SEAN DUARTE', 500000, '5.10'],
  ['2026-09-11', 'CINTA', '', 'PROVEEDOR CHICO', 3000, '5.04'],
  ['2026-09-12', 'CINTA', '', 'PROVEEDOR CHICO', 3000, '5.04'],
];
const ID0 = 1760000000000000, id = i => ID0 + i * 1000;
psql(`drop database if exists ${BASE}`, 'postgres'); psql(`create database ${BASE}`, 'postgres');
psql(`create table gastos (id bigint primary key, fecha date, monto numeric, descripcion text, categoria text, proveedor text, metodo_pago text, observaciones text);
  create table proveedores (id bigint primary key, nombre text, centro_costo text, rut text, telefono text, email text, direccion text);
  create table pedidos (id bigint primary key, cot text, cliente text, fecha date, total numeric, saldo numeric, abonos jsonb, docs jsonb, vendedor text, observaciones text, estado text);
  grant all on gastos, proveedores, pedidos to anon;
  insert into pedidos values (1, 'COT-1', 'Club Uno', '2026-10-01', 1190000, 0, '[]', '[]', 'Sean Duarte', '[]', 'Pagado');
  insert into proveedores (id, nombre, rut) values (11, 'UBER', ''), (12, 'HEAT SUIT', '2-7'), (13, 'MUNDO TRANSFER', '78950040-1'),
    (14, 'RODOLFO GARCIA', ''), (15, 'SEAN DUARTE', ''), (16, 'PROVEEDOR CHICO', '');
  ${G.map((g, i) => `insert into gastos values (${id(i)}, '${g[0]}', ${g[4]}, ${lit(g[1])}, ${lit(g[2])}, ${lit(g[3])}, 'Transferencia electrónica', '');`).join('\n')}`);
psql(SQL21); psql(SQL21B);
psql(`update proveedores set cuenta_codigo = '4.04', tipo_documento = 'afecta' where id = 12; update proveedores set es_socio = true where id = 15;
  ${G.map((g, i) => g[5] ? `update gasto_clasif set cuenta_codigo = '${g[5]}', estado = 'clasificado', origen = 'manual', sugerencia_codigo = null, documento = ${g[6] ? `'${g[6]}'` : 'null'} where gasto_id = ${id(i)};` : '').join('\n')}`);
const k = i => uno(`select row_to_json(c) from gasto_clasif c where gasto_id = ${id(i)}`);
ok(k(9).estado === 'revision' && k(17).estado === 'revision' && k(10).cuenta_codigo === '4.05' && k(10).origen === 'alias', 'antes: dos gastos en revisión; Heat Suit por su categoría (4.05)');

// ── SQL 24C ──
const f24 = psql(SQL24C).split('\n').pop().split('|');
ok(f24[0] === 'SQL 24C listo' && +f24[1] === 1, 'SQL 24C: corre (' + f24.join(' | ') + ')');
ok(psql(SQL24C).split('\n').pop().split('|')[0] === 'SQL 24C listo', 'SQL 24C: se puede volver a correr');
ok(k(10).cuenta_codigo === '4.05' && k(10).origen === 'alias', 'lo clasificado por su categoría no cambia aunque la cuenta habitual sea otra (Heat Suit sigue en 4.05)');

// ── Supabase de mentira atendido por Postgres (lo justo de PostgREST que usa Ventas) ──
const PK = { gastos: 'id', proveedores: 'id', pedidos: 'id', plan_cuentas: 'codigo', gasto_cuenta_alias: 'categoria', gestion_parametros: 'clave', gasto_clasif: 'gasto_id', gasto_reglas: 'id' };
let sin24C = false;
function filtros(u) {
  const w = [];
  for (const [c, v] of u.searchParams) { if (['select', 'order', 'limit', 'offset', 'on_conflict'].includes(c)) continue; const m = v.match(/^eq\.(.*)$/); if (m) w.push(`"${c}" = ${lit(m[1])}`); }
  return w.length ? ' where ' + w.join(' and ') : '';
}
function atender(req, u) {
  if (/^\/functions\//.test(u.pathname)) return [404, { code: 'NOT_FOUND' }];
  const m = u.pathname.match(/^\/rest\/v1\/(rpc\/)?([a-z_0-9]+)$/); if (!m) return [404, { message: 'ruta' }];
  const t = m[2], met = req.method();
  if (m[1]) {
    if (t === 'pedidos_livianos') return [404, { code: 'PGRST202' }];
    const args = JSON.parse(req.postData() || '{}');
    return [200, uno(`set role anon; select coalesce(to_json(public.${t}(${Object.entries(args).map(([a, v]) => `${a} => ${v === null ? 'null' : lit(v)}`).join(', ')})), 'null')`)];
  }
  if (met === 'GET') {
    const orden = (u.searchParams.get('order') || '').split(',').filter(Boolean).map(o => { const [c, d] = o.split('.'); return `"${c}" ${d === 'desc' ? 'desc' : 'asc'}`; }).join(', ');
    let lim = ''; const r = req.headers()['range']; if (r) { const [a, z] = r.split('-').map(Number); lim = ` limit ${z - a + 1} offset ${a}`; }
    if (u.searchParams.get('limit')) lim = ' limit ' + (+u.searchParams.get('limit'));
    let filas = uno(`set role anon; select coalesce(jsonb_agg(x), '[]') from (select * from public.${t}${filtros(u)}${orden ? ' order by ' + orden : ''}${lim}) x`);
    if (sin24C && t === 'gestion_parametros') filas = filas.filter(x => x.clave !== 'clasif_por_proveedor');
    return [200, filas];
  }
  if (met === 'POST') {
    const body = JSON.parse(req.postData()); const filas = Array.isArray(body) ? body : [body]; const cols = Object.keys(filas[0]).map(c => `"${c}"`);
    const conflicto = /merge-duplicates/.test(req.headers()['prefer'] || '') ? ` on conflict ("${PK[t]}") do update set ${cols.filter(c => c !== `"${PK[t]}"`).map(c => `${c} = excluded.${c}`).join(', ')}` : '';
    const res = uno(`set role anon; with x as (insert into public.${t} (${cols}) select ${cols} from json_populate_recordset(null::public.${t}, ${lit(JSON.stringify(filas))})${conflicto} returning *) select coalesce(jsonb_agg(x), '[]') from x`);
    return [201, /return=representation/.test(req.headers()['prefer'] || '') ? res : null];
  }
  if (met === 'PATCH') {
    const body = JSON.parse(req.postData()); const cols = Object.keys(body).map(c => `"${c}"`);
    psql(`set role anon; update public.${t} set (${cols}) = (select ${cols} from json_populate_record(null::public.${t}, ${lit(JSON.stringify(body))}))${filtros(u)}`);
    return [204, null];
  }
  return [405, null];
}

(async () => {
  const b = await chromium.launch();
  async function abrir(viewport) {
    const ctx = await b.newContext({ viewport: viewport || { width: 1280, height: 860 }, serviceWorkers: 'block' });
    await ctx.route('**/*', async r => {
      const req = r.request(), u = new URL(req.url());
      if (u.host === 'ventas-playmaker.netlify.app') return r.fulfill({ body: HTML, contentType: 'text/html' });
      if (u.host === 'ygcsqrylpibhofvetdyh.supabase.co') return r.fulfill({ contentType: 'application/json', body: JSON.stringify(/plan_sesion/.test(u.pathname) ? { usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'] } : []) });
      if (u.host === 'nnisdusdujcpkrbjqnhe.supabase.co') {
        let st, body;
        try { [st, body] = atender(req, u); } catch (e) { st = 400; body = { message: String(e.stderr || e.message).slice(0, 300) }; }
        return r.fulfill({ status: st, contentType: 'application/json', body: body == null ? '' : JSON.stringify(body) });
      }
      if (/fonts/.test(u.host)) return r.fulfill({ body: '' });
      return r.abort();
    });
    const p = await ctx.newPage(); p.errores = []; p.on('pageerror', e => p.errores.push(e.message)); p.on('dialog', d => { if (process.env.DEPURAR) console.log('DIALOGO', d.message()); d.accept(); });
    await p.goto('https://ventas-playmaker.netlify.app/#pmk_acceso=tok1');
    await p.waitForFunction(() => typeof DB !== 'undefined' && DB.length >= 1 && typeof GASTOS !== 'undefined' && GASTOS.length > 0, null, { timeout: 30000 });
    await p.evaluate(() => showView('gastos'));
    await p.waitForSelector('[data-gsub="proveedores"]', { timeout: 10000 });
    await p.click('[data-gsub="proveedores"]'); await p.waitForTimeout(200);
    return p;
  }
  const p = await abrir();
  const fila = async n => (await p.textContent(`#gsub-proveedores tr:has(td b:text-is("${n}")) .prov-segun`)).replace(/\s+/g, ' ').trim();
  const uber = await fila('UBER');
  ok(/2\.11 Despachos a clientes/.test(uber) && /5 de 9 clasificados/.test(uber) && /3\.11 \(3\)/.test(uber), 'Según sus gastos: Uber → Despachos, 5 de 9, también Traslados (3): «' + uber + '»');
  ok(/Su cuenta habitual es otra/.test(await fila('HEAT SUIT')), 'avisa cuando la cuenta habitual no es la de sus gastos (Heat Suit)');
  ok(/clasificados solos/.test(await p.textContent('#gsub-proveedores')), 'con el SQL 24C dice que los gastos nuevos quedan clasificados solos');

  // ── Completar con lo que dicen los gastos ──
  await p.click('text=Completar con lo que dicen los gastos'); await p.waitForSelector('#pp-overlay');
  const modal = (await p.textContent('#pp-overlay')).replace(/\s+/g, ' ');
  const secHab = (await p.locator('#pp-overlay .pp-sec').nth(0).textContent()).replace(/\s+/g, ' ');
  ok(/UBER → 2\.11 Despachos a clientes · 5 de 6 gastos/.test(modal) && /MUNDO TRANSFER → 2\.04/.test(modal) && /RODOLFO GARCIA → 3\.01/.test(modal),
    'propone cuenta habitual: Uber (sin contar los de su regla), Mundo Transfer y Rodolfo García');
  ok(!/SEAN DUARTE/.test(secHab) && !/PROVEEDOR CHICO/.test(modal) && !/HEAT SUIT/.test(modal), 'no propone cuenta habitual a socios, a proveedores con pocos gastos ni a los que ya tienen');
  ok(/SEAN DUARTE → Sin documento/.test(modal), 'al socio sí le propone el documento (sin documento, por Remuneración de socios)');
  ok(/UBER \+ «TALLER» → 3\.11 Traslados a talleres · 3 gastos/.test(modal) && !/FRANKLIN/.test(modal), 'aprende la regla Uber + «taller» → Traslados (un solo gasto no alcanza)');
  ok(/MUNDO TRANSFER → Factura afecta.*marcado en 3 de sus gastos/.test(modal) && /RODOLFO GARCIA → Sin documento.*Sueldos de producci/.test(modal), 'propone el tipo de documento: lo marcado en sus gastos o según su cuenta');
  await p.locator('#pp-overlay .pp-caja').screenshot({ path: path.join(__dirname, 'proveedores_completar.png') });
  await p.locator('.pp-doc').nth(1).uncheck();   // Rodolfo García: no se guarda su documento
  await p.click('#pp-guardar'); await p.waitForSelector('#pp-overlay', { state: 'detached', timeout: 10000 });
  await p.waitForTimeout(300);
  const prov = n => uno(`select row_to_json(x) from (select cuenta_codigo, centro_costo, tipo_documento from proveedores where nombre = ${lit(n)}) x`);
  ok(prov('UBER').cuenta_codigo === '2.11' && prov('UBER').centro_costo === 'Despachos a clientes' && prov('MUNDO TRANSFER').cuenta_codigo === '2.04' && prov('MUNDO TRANSFER').tipo_documento === 'afecta',
    'guardado: cuenta habitual y documento (' + JSON.stringify([prov('UBER'), prov('MUNDO TRANSFER')]) + ')');
  ok(prov('RODOLFO GARCIA').cuenta_codigo === '3.01' && prov('RODOLFO GARCIA').tipo_documento === null, 'lo desmarcado no se guarda');
  ok(psql(`select tipo || '|' || proveedor || '|' || palabra || '|' || cuenta_codigo || '|' || prioridad from gasto_reglas where palabra = 'TALLER'`) === 'proveedor_palabra|UBER|TALLER|3.11|60', 'regla aprendida guardada (prioridad 60: después de las de revisión)');
  ok(k(9).estado === 'clasificado' && k(9).cuenta_codigo === '3.11' && k(9).origen === 'regla', 'el gasto en revisión «ENVIO TALLER ROSA» queda en Traslados a talleres');
  ok(k(17).estado === 'clasificado' && k(17).cuenta_codigo === '2.04' && k(17).origen === 'proveedor', 'el gasto en revisión de Mundo Transfer queda en su cuenta habitual');
  ok(k(5).origen === 'manual' && k(8).cuenta_codigo === '5.09', 'lo elegido por una persona no cambia');
  const aviso = await p.textContent('#toast');
  ok(/Guardado: 4 proveedores y 1 regla · 2 gastos salieron de Revisi/.test(aviso), 'aviso: ' + aviso);

  // ── Gastos nuevos: la base los clasifica sola ──
  psql(`insert into gastos values (${id(90)}, '2026-11-15', 35000, 'TRANSFER', '', 'MUNDO TRANSFER', 'Transferencia electrónica', '');
        insert into gastos values (${id(91)}, '2026-11-15', 9000, 'UBER TALLER SONIA', 'MOVILIZACIÓN', 'UBER', 'Tarjeta', '');
        insert into gastos values (${id(92)}, '2026-11-15', 500000, 'ANTICIPO', '', 'SEAN DUARTE', 'Transferencia electrónica', '');`);
  ok(k(90).cuenta_codigo === '2.04' && k(90).origen === 'proveedor' && k(90).estado === 'clasificado', 'gasto nuevo sin categoría → cuenta habitual, clasificado');
  ok(k(91).cuenta_codigo === '3.11', 'gasto nuevo de Uber que dice «taller» → la regla manda sobre su categoría');
  ok(k(92).estado === 'revision', 'pago a un socio → sigue a revisión');

  // ── Formulario: al escribir el proveedor sugiere la cuenta sin preguntarle a Claude ──
  await p.evaluate(() => abrirNuevoGasto());
  await p.fill('#g-fecha', '2026-11-16'); await p.fill('#g-monto', '7000');
  await p.fill('#g-prov', 'UBER'); await p.fill('#g-desc', 'Envios clientes');
  ok(await p.inputValue('#g-cta') === '2.11' && /Cuenta habitual del proveedor/.test(await p.textContent('#g-sug')), 'formulario: Uber → Despachos (cuenta habitual)');
  await p.fill('#g-desc', 'Uber a taller de Paola');
  ok(await p.inputValue('#g-cta') === '3.11' && /UBER.*TALLER/.test(await p.textContent('#g-sug')), 'formulario: Uber + «taller» → Traslados (regla aprendida)');
  await p.evaluate(() => closeGastoModal());

  // ── Volver a abrir: ya no propone lo guardado ──
  await p.click('[data-gsub="proveedores"]'); await p.waitForTimeout(200);
  await p.click('text=Completar con lo que dicen los gastos'); await p.waitForSelector('#pp-overlay');
  const modal2 = (await p.textContent('#pp-overlay')).replace(/\s+/g, ' ');
  ok(!/UBER →/.test(modal2) && !/«TALLER»/.test(modal2) && /RODOLFO GARCIA → Sin documento/.test(modal2), 'al volver a abrir solo queda lo que no se guardó');
  await p.click('#pp-overlay >> text=Cancelar');
  ok(/1 regla por palabra/.test(await fila('UBER')), 'la columna muestra las reglas por palabra del proveedor');
  ok(p.errores.length === 0, 'sin errores en la página ' + JSON.stringify(p.errores));

  // ── Celular ──
  const m = await abrir({ width: 390, height: 844 });
  await m.click('text=Completar con lo que dicen los gastos'); await m.waitForSelector('#pp-overlay');
  const anchoOk = await m.evaluate(() => document.querySelector('#pp-overlay .pp-caja').getBoundingClientRect().width <= 390);
  ok(anchoOk, 'celular: la ventana cabe en la pantalla');
  await m.screenshot({ path: path.join(__dirname, 'proveedores_completar_movil.png') });
  ok(m.errores.length === 0, 'celular: sin errores ' + JSON.stringify(m.errores));

  // ── Sin el SQL 24C: avisa que falta para clasificar sola ──
  sin24C = true;
  const q = await abrir();
  ok(/falta correr el SQL 24C/.test(await q.textContent('#gsub-proveedores')), 'sin el SQL 24C: avisa que la base todavía no clasifica sola');
  ok(q.errores.length === 0, 'sin SQL 24C: sin errores ' + JSON.stringify(q.errores));
  await b.close();
  psql(`drop database if exists ${BASE}`, 'postgres');
  console.log(fallas ? `\n${fallas} FALLAS` : '\nTODO OK');
  process.exit(fallas ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
