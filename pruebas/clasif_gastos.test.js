// Clasificación de gastos (SQL 21A + Ventas › Gastos): de punta a punta contra un Postgres de verdad.
// Corre el SQL 21A en una base local con gastos de prueba y atiende las llamadas de la página con psql, como
// Supabase: así se prueban juntos la pantalla, los disparadores, los permisos de la llave pública y la conciliación.
// Requiere Postgres local (PGHOST/PGPORT; por defecto el socket /home/postgres, puerto 5499) con los roles anon y authenticated.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const HTML = fs.readFileSync(path.resolve(__dirname, '../sistemas/ventas/index.html'));
const SQL21 = fs.readFileSync(path.resolve(__dirname, '../sql/SQL_21A_VENTAS_clasificacion_gastos.sql'), 'utf8');
const PSQL = process.env.PSQL || '/usr/lib/postgresql/16/bin/psql';
const PG = ['-h', process.env.PGHOST || '/home/postgres', '-p', process.env.PGPORT || '5499', '-U', 'postgres'];
const BASE = 'ventas_prueba_21a';
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const psql = (sql, db = BASE) => execFileSync(PSQL, [...PG, '-d', db, '-q', '-At', '-v', 'ON_ERROR_STOP=1'], { input: sql, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
const uno = sql => { const t = psql(sql).split('\n').pop(); return t ? JSON.parse(t) : null; };
const lit = v => '$J$' + String(v).replace(/\$J\$/g, '') + '$J$';

// ── Base de prueba: tablas como las de Ventas y gastos que cubren los casos del documento ──
const G = [
  // [fecha, descripción, categoría, proveedor, monto]
  ['2026-10-26', 'ESTAMPADO', 'ASEO', 'VICTORIA COFRE', 120000],
  ['2026-10-09', 'TEFLON MAQUINA ESTAMPADORA', 'MANTENCIÓN Y REPUESTOS DE MÁQUINAS', 'MUNDO TRANSFER', 38999],
  ['2026-09-01', 'TINTAS MIMAKI', 'INVERSIÓN EN MÁQUINAS Y EQUIPOS', 'FERROSTAAL', 311937],
  ['2026-04-15', 'PIE COMPRA PLOTER MIMAKI', 'INVERSIÓN EN MÁQUINAS Y EQUIPOS', 'FERROSTAAL', 3750000],
  ['2026-04-13', 'ESPEJOS PMK', 'INVERSIÓN EN MÁQUINAS Y EQUIPOS', 'HOMECENTER QUILICURA', 37960],
  ['2026-08-31', 'CONFECCION DE PRENDAS', 'HONORARIOS DE PRODUCCIÓN', 'RAMIRO PONCE', 99237],
  ['2026-04-06', 'COMPRA TELA SCUBA 22.2 METROS', 'IMPUESTOS (IVA)', 'LLABUR HERMANOS', 208702],
  ['2026-10-19', 'IVA', 'IMPUESTOS (IVA)', 'MIGUEL ANGEL M', 1035949],
  ['2026-09-30', 'HONORARIOS', 'SUELDOS VENTAS Y MARKETING', 'ANTONIA HERMOSILLA', 691695],
  ['2026-10-05', 'ENVIOS', 'DESPACHOS A CLIENTES', 'ANTONIA HERMOSILLA', 15000],
  ['2026-11-04', 'ELECTRICO (TALLER PMK)', 'OTROS', 'RODOLFO RIQUELME', 964188],
  ['2026-11-10', 'NO SE', 'OTROS', 'LA MAISON', 16000],
  ['2026-09-07', 'COMPRA', 'POR IDENTIFICAR', 'DODO MARKET SPA', 45000],
  ['2026-06-17', 'REEMBOLSO GASTO', 'POR IDENTIFICAR', 'SEAN DUARTE', 483000],
  ['2026-07-10', 'ANTICIPO SUELDO', 'REMUNERACIÓN DE SOCIOS', 'SEAN DUARTE', 500000],
  ['2026-08-10', 'ANTICIPO SUELDO', 'REMUNERACIÓN DE SOCIOS', 'SEAN DUARTE', 500000],
  ['2026-10-01', 'TELA DRY FIT', 'TELAS', 'TEXTILES DEL SUR', 2500000],
  ['2026-10-02', 'CONFECCION 40 CAMISETAS', 'TALLER EXTERNO', 'TALLER ROSA', 320000],
  ['2026-10-03', 'MENSUALIDAD', 'HERRAMIENTAS DE MARKETING', 'HEAT SUIT', 26000],
  ['2026-09-03', 'MENSUALIDAD', 'HERRAMIENTAS DE MARKETING', 'HEAT SUIT', 26000],
  ['2026-08-03', 'MENSUALIDAD', 'HERRAMIENTAS DE MARKETING', 'HEAT SUIT', 26000],
  ['2026-10-05', 'ARRIENDO OCTUBRE', 'ARRIENDO', 'INMOBILIARIA', 2200000],
  ['2026-10-20', 'UBER A CLIENTE', 'DESPACHOS A CLIENTES', 'UBER', 9000],
  ['2026-10-21', 'UBER REUNION', 'MOVILIZACIÓN', 'UBER', 7000],
  ['2026-03-12', 'NO ME ACUERDO', 'POR IDENTIFICAR', 'NO ME ACUERDO', 50000],   // antes de abril
  ['2026-10-22', 'BOLSAS', 'INSUMOS PRODUCCION', 'PLASTICOS HOMS', 212296],
];
const ID0 = 1760000000000000;
psql(`drop database if exists ${BASE}`, 'postgres'); psql(`create database ${BASE}`, 'postgres');
psql(`create table gastos (id bigint primary key, fecha date, monto numeric, descripcion text, categoria text, proveedor text, metodo_pago text, observaciones text);
  create table proveedores (id bigint primary key, nombre text, centro_costo text, rut text, telefono text, email text, direccion text);
  create table pedidos (id bigint primary key, cot text, cliente text, fecha date, total numeric, saldo numeric, abonos jsonb, docs jsonb, vendedor text, observaciones text, estado text);
  grant all on gastos, proveedores, pedidos to anon;
  insert into pedidos values (1, 'COT-1', 'Club Uno', '2026-10-01', 1190000, 0, '[]', '[]', 'Sean Duarte', '[]', 'Pagado');
  insert into proveedores (id, nombre, rut) values (11, 'VICTORIA COFRE', '1-9'), (12, 'HEAT SUIT', '2-7'), (13, 'FERROSTAAL', '3-5');
  ${G.map((g, i) => `insert into gastos values (${ID0 + i * 1000}, '${g[0]}', ${g[4]}, ${lit(g[1])}, ${lit(g[2])}, ${lit(g[3])}, 'Transferencia electrónica', '');`).join('\n')}`);
const fin = psql(SQL21).split('\n').pop().split('|');
const TOTAL = G.reduce((s, g) => s + g[4], 0);
ok(fin[0] === 'clasificación lista' && +fin[2] === TOTAL && +fin[3] === TOTAL && +fin[9] === 0, 'SQL 21A: corre y concilia (' + fin.join(' | ') + ')');
ok(psql(SQL21).split('\n').pop().split('|')[0] === 'clasificación lista' && +psql('select count(*) from gasto_raw') === G.length && +psql('select count(*) from gasto_reglas') === 11, 'SQL 21A: se puede volver a correr sin duplicar');
const k = i => uno(`select row_to_json(c) from gasto_clasif c where gasto_id = ${ID0 + i * 1000}`);
ok(k(0).cuenta_codigo === '3.04' && k(0).origen === 'regla', 'regla: «ESTAMPADO» en ASEO → Jornales de producción');
ok(k(1).cuenta_codigo === '3.06', 'regla: «estampadora» no calza con «estampado»');
ok(k(2).cuenta_codigo === '2.03' && k(3).cuenta_codigo === 'F.02' && k(4).estado === 'revision' && /umbral/.test(k(4).motivo), 'tintas → sublimación; plotter → inversión; espejos bajo $300.000 → revisión');
ok(k(5).cuenta_codigo === '2.02' && k(6).cuenta_codigo === '2.01' && k(7).cuenta_codigo === 'F.01', 'confección → talleres; compra de tela en IVA → telas; pago de IVA fuera del resultado');
ok(k(8).cuenta_codigo === '2.09' && k(9).cuenta_codigo === '2.11', 'Antonia Hermosilla: honorarios → comisiones de venta; envíos → despachos');
ok(k(10).cuenta_codigo === 'F.03' && k(11).estado === 'revision' && k(12).estado === 'revision', 'eléctrico Taller PMK → mejoras al local; «no sé» y «por identificar» → revisión');
ok(k(14).estado === 'revision' && k(14).sugerencia_codigo === 'F.06' && k(13).estado === 'revision', 'pagos a Sean Duarte → revisión con sugerencia «Pagos a socios»');
ok(k(17).cuenta_codigo === '2.02' && k(21).cuenta_codigo === '3.07' && k(25).estado === 'revision' && k(25).sugerencia_codigo === '2.05', 'TALLER EXTERNO → talleres; arriendo; insumos producción → revisión (avíos o packaging)');
let err = ''; try { psql(`set role anon; update gasto_raw set monto_bruto = 1;`); } catch (e) { err = String(e.stderr || e.message); }
ok(/permission denied/.test(err), 'la llave pública no puede modificar el dato crudo');
err = ''; try { psql(`delete from gasto_raw where id = 1;`); } catch (e) { err = String(e.stderr || e.message); }
ok(/no se modifica ni se borra/.test(err), 'ni siquiera el dueño de la base puede borrar el dato crudo');

// ── Supabase de mentira atendido por Postgres: lo justo de PostgREST que usa Ventas ──
const PK = { gastos: 'id', proveedores: 'id', pedidos: 'id', plan_cuentas: 'codigo', gasto_cuenta_alias: 'categoria', gestion_parametros: 'clave', gasto_clasif: 'gasto_id', gasto_reglas: 'id' };
let sinSQL21 = false; const llamadas = [];
function filtros(u) {
  const w = [];
  for (const [c, v] of u.searchParams) { if (['select', 'order', 'limit', 'offset', 'on_conflict'].includes(c)) continue; const m = v.match(/^eq\.(.*)$/); if (m) w.push(`"${c}" = ${lit(m[1])}`); }
  return w.length ? ' where ' + w.join(' and ') : '';
}
function atender(req, u) {
  const m = u.pathname.match(/^\/rest\/v1\/(rpc\/)?([a-z_0-9]+)$/); if (!m) return [404, { message: 'ruta' }];
  const t = m[2], met = req.method();
  llamadas.push(met + ' ' + t);
  if (m[1]) {
    if (t === 'pedidos_livianos') return [404, { code: 'PGRST202' }];
    const args = JSON.parse(req.postData() || '{}');
    return [200, uno(`set role anon; select coalesce(to_json(public.${t}(${Object.entries(args).map(([a, v]) => `${a} => ${v === null ? 'null' : lit(v)}`).join(', ')})), 'null')`)];
  }
  if (sinSQL21 && /^(plan_cuentas|gasto_|gestion_|v_gastos)/.test(t)) return [404, { code: 'PGRST205', message: 'no existe ' + t }];
  if (met === 'GET') {
    const orden = (u.searchParams.get('order') || '').split(',').filter(Boolean).map(o => { const [c, d] = o.split('.'); return `"${c}" ${d === 'desc' ? 'desc' : 'asc'}`; }).join(', ');
    let lim = ''; const r = req.headers()['range']; if (r) { const [a, z] = r.split('-').map(Number); lim = ` limit ${z - a + 1} offset ${a}`; }
    if (u.searchParams.get('limit')) lim = ' limit ' + (+u.searchParams.get('limit'));
    return [200, uno(`set role anon; select coalesce(jsonb_agg(x), '[]') from (select * from public.${t}${filtros(u)}${orden ? ' order by ' + orden : ''}${lim}) x`)];
  }
  if (met === 'POST') {
    let body = JSON.parse(req.postData()); const filas = Array.isArray(body) ? body : [body]; const cols = Object.keys(filas[0]).map(c => `"${c}"`);
    const conflicto = /merge-duplicates/.test(req.headers()['prefer'] || '') ? ` on conflict ("${PK[t]}") do update set ${cols.filter(c => c !== `"${PK[t]}"`).map(c => `${c} = excluded.${c}`).join(', ')}` : '';
    const res = uno(`set role anon; with x as (insert into public.${t} (${cols}) select ${cols} from json_populate_recordset(null::public.${t}, ${lit(JSON.stringify(filas))})${conflicto} returning *) select coalesce(jsonb_agg(x), '[]') from x`);
    return [201, /return=representation/.test(req.headers()['prefer'] || '') ? res : null];
  }
  if (met === 'PATCH') {
    const body = JSON.parse(req.postData()); const cols = Object.keys(body).map(c => `"${c}"`);
    psql(`set role anon; update public.${t} set (${cols}) = (select ${cols} from json_populate_record(null::public.${t}, ${lit(JSON.stringify(body))}))${filtros(u)}`);
    return [204, null];
  }
  if (met === 'DELETE') { psql(`set role anon; delete from public.${t}${filtros(u)}`); return [204, null]; }
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
    const p = await ctx.newPage(); p.errores = []; p.on('pageerror', e => p.errores.push(e.message)); p.on('dialog', d => d.accept());
    await p.goto('https://ventas-playmaker.netlify.app/#pmk_acceso=tok1');
    await p.waitForFunction(() => typeof DB !== "undefined" && DB.length >= 1 && typeof GASTOS !== 'undefined' && GASTOS.length > 0, null, { timeout: 30000 });
    await p.evaluate(() => showView('gastos'));
    return p;
  }
  const p = await abrir();
  await p.waitForSelector('[data-gsub="revision"]', { timeout: 10000 });
  ok(await p.textContent('#th-cat-g') === 'Cuenta', 'la lista de gastos muestra la cuenta');
  ok(/Jornales de producci/.test(await p.textContent('#tabla-gastos')), 'el gasto de estampado aparece en Jornales de producción');
  ok(/Revisi.n\s*7/.test(await p.textContent('#gsub-bar')), 'la barra muestra 7 gastos por revisar desde abril (el de marzo no cuenta): «' + (await p.textContent('#gsub-bar')).replace(/\s+/g, ' ') + '»');

  // ── Gasto nuevo: la regla precarga la cuenta ──
  await p.evaluate(() => abrirNuevoGasto());
  await p.fill('#g-fecha', '2026-11-12'); await p.fill('#g-monto', '90000');
  await p.fill('#g-prov', 'VICTORIA COFRE'); await p.fill('#g-desc', 'Estampado dos días');
  ok(await p.inputValue('#g-cta') === '3.04' && /Regla: la descripción dice «ESTAMPADO»/.test(await p.textContent('#g-sug')), 'gasto nuevo: «estampado» precarga Jornales de producción y dice por qué');
  ok(await p.isHidden('#g-regla'), 'si se acepta la sugerencia no se ofrece crear regla');
  await p.click('#modal-gasto-body button.btn-primary'); await p.waitForTimeout(400);
  const nuevo = uno(`select row_to_json(x) from (select g.id, c.cuenta_codigo, c.origen, c.regla_id is not null as regla, c.periodo_devengo, c.actualizado_por, (select count(*) from gasto_raw r where r.gasto_id = g.id) as versiones from gastos g join gasto_clasif c on c.gasto_id = g.id where g.descripcion = 'Estampado dos días') x`);
  ok(nuevo && nuevo.cuenta_codigo === '3.04' && nuevo.origen === 'regla' && nuevo.regla && nuevo.periodo_devengo === '2026-11-01' && nuevo.actualizado_por === 'Sean Duarte' && nuevo.versiones === 1, 'guardado: cuenta, origen «regla», mes y dato original (' + JSON.stringify(nuevo) + ')');
  ok(psql(`select categoria from gastos where id = ${nuevo.id}`) === 'Jornales de producción', 'el gasto guarda el nombre de la cuenta como categoría (Flujo de caja y versiones anteriores siguen funcionando)');

  // ── Historial del proveedor + corrección que crea una regla ──
  await p.evaluate(() => abrirNuevoGasto());
  await p.fill('#g-fecha', '2026-11-03'); await p.fill('#g-monto', '26000');
  await p.fill('#g-prov', 'HEAT SUIT'); await p.fill('#g-desc', 'Mensualidad noviembre');
  ok(await p.inputValue('#g-cta') === '4.05' && /Historial: 3 de 3 gastos/.test(await p.textContent('#g-sug')), 'proveedor conocido: el historial sugiere Herramientas de marketing (3 de 3)');
  await p.selectOption('#g-cta', '5.02');
  ok(await p.isVisible('#g-regla-chk'), 'al cambiar la cuenta se ofrece crear una regla');
  await p.check('#g-regla-chk');
  await p.locator('#modal-gasto-overlay .modal').screenshot({ path: path.join(__dirname, 'clasif_formulario.png') });
  await p.click('#modal-gasto-body button.btn-primary'); await p.waitForTimeout(800);
  const heat = psql(`select string_agg(c.cuenta_codigo || ':' || c.origen, ',' order by g.fecha) from gastos g join gasto_clasif c on c.gasto_id = g.id where g.proveedor = 'HEAT SUIT'`);
  ok(heat === '5.02:regla,5.02:regla,5.02:regla,5.02:manual', 'la regla nueva reclasifica los gastos automáticos de Heat Suit (' + heat + ')');
  ok(psql(`select tipo || '|' || proveedor || '|' || cuenta_codigo || '|' || creada_por from gasto_reglas where proveedor = 'HEAT SUIT'`) === 'proveedor|HEAT SUIT|5.02|Sean Duarte', 'regla guardada con quién la creó');

  // ── Revisión ──
  await p.click('[data-gsub="revision"]'); await p.waitForTimeout(200);
  const filasRev = await p.$$eval('#gsub-revision tr[data-rev]', t => t.length);
  ok(filasRev === 7, 'Revisión: 7 gastos desde abril (' + filasRev + ')');
  const idDodo = ID0 + 12 * 1000;
  await p.selectOption('#rev-c-' + idDodo, '5.04');
  await p.click(`tr[data-rev="${idDodo}"] button`); await p.waitForTimeout(400);
  ok(psql(`select cuenta_codigo || '|' || origen || '|' || estado from gasto_clasif where gasto_id = ${idDodo}`) === '5.04|manual|clasificado', 'aceptar un gasto en revisión lo deja clasificado a mano');
  await p.selectOption('#rev-motivo', { label: 'Pago a socio: ¿gasto de la empresa, reembolso con respaldo o retiro? (2)' });
  await p.check('#rev-todos');
  await p.click('text=Aceptar la sugerencia de los seleccionados'); await p.waitForTimeout(500);
  ok(psql(`select string_agg(cuenta_codigo, ',') from gasto_clasif where gasto_id in (${ID0 + 14000}, ${ID0 + 15000}) and estado = 'clasificado'`) === 'F.06,F.06', 'aceptar sugerencias en grupo: los anticipos de sueldo quedan en Pagos a socios');
  ok(/Revisi.n\s*4/.test(await p.textContent('#gsub-bar')), 'el contador de revisión baja a 4');

  // ── Editar y eliminar: el dato original guarda cada versión ──
  await p.click('[data-gsub="lista"]');
  const idArr = ID0 + 21 * 1000;
  await p.evaluate(id => editarGasto(id), idArr);
  ok(await p.inputValue('#g-cta') === '3.07', 'editar: muestra la cuenta del gasto');
  await p.fill('#g-mes', '2026-09'); await p.fill('#g-monto', '2250000');
  await p.click('#modal-gasto-body button.btn-primary'); await p.waitForTimeout(400);
  ok(psql(`select string_agg(operacion || ':' || monto_bruto, ',' order by version) from gasto_raw where gasto_id = ${idArr}`) === 'carga_inicial:2200000,edicion:2250000', 'editar agrega una versión del dato original sin tocar la anterior');
  const arr = psql(`select periodo_devengo || '|' || origen from gasto_clasif where gasto_id = ${idArr}`);
  ok(arr === '2026-09-01|alias', 'arriendo pagado en octubre queda en septiembre y sigue siendo automático (' + arr + ')');
  await p.evaluate(id => editarGasto(id), idArr);
  await p.click('text=Ver dato original'); await p.waitForSelector('#capa-historial');
  ok(/Carga inicial[\s\S]*Editado/.test(await p.textContent('#capa-historial')), '«Ver dato original» muestra las versiones');
  await p.evaluate(() => { cerrarCapaGastos('capa-historial'); closeGastoModal(); });
  const idUber = ID0 + 23 * 1000;
  await p.evaluate(id => eliminarGasto(id), idUber); await p.waitForTimeout(400);
  ok(psql(`select string_agg(operacion, ',' order by version) from gasto_raw where gasto_id = ${idUber}`) === 'carga_inicial,baja' && psql(`select count(*) from gasto_clasif where gasto_id = ${idUber}`) === '0', 'eliminar: el dato original queda con la versión «baja»');

  // ── Plan de cuentas: traducción de una categoría ──
  await p.click('[data-gsub="plan"]'); await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(__dirname, 'clasif_plan.png') });
  ok(/Nivel 2 · Costo directo variable[\s\S]*= Margen de contribución[\s\S]*Nivel 3 · Gasto general de producción[\s\S]*= Margen bruto[\s\S]*Nivel 4 · Gasto general de venta y marketing[\s\S]*Nivel 5 · Gasto general de administración[\s\S]*= EBITDA[\s\S]*Fuera del estado de resultados/.test(await p.textContent('#gsub-plan')), 'plan de cuentas por niveles con sus resultados');
  const cats = await p.evaluate(() => JSON.parse(document.getElementById('gsub-plan').dataset.alias));
  const iTaller = cats.indexOf('TALLER EXTERNO');
  await p.check('#al-r-' + iTaller);
  await p.click(`#al-c-${iTaller} >> xpath=../following-sibling::td[2]/button`); await p.waitForTimeout(600);
  ok(psql(`select estado || '|' || sugerencia_codigo from gasto_clasif where gasto_id = ${ID0 + 17000}`) === 'revision|2.02', 'marcar «revisar» en TALLER EXTERNO manda sus gastos a revisión con la sugerencia');
  await p.evaluate(() => abrirCuentaForm('3.02'));
  await p.fill('#cf-sup', ''); await p.click('text=Guardar cuenta'); await p.waitForTimeout(400);
  ok(psql(`select coalesce(supuesto, '(vacío)') || '|' || actualizado_por from plan_cuentas where codigo = '3.02'`) === '(vacío)|Sean Duarte', 'editar una cuenta (quitar el «por confirmar» de Sueldos de diseño)');

  // ── Reglas: desactivar ESTAMPADO devuelve el gasto a su categoría, salvo los elegidos a mano ──
  await p.click('[data-gsub="reglas"]'); await p.waitForTimeout(200);
  const idEst = psql(`select id from gasto_reglas where palabra = 'ESTAMPADO'`);
  await p.uncheck(`input[onchange="activarReglaGasto(${idEst},this.checked)"]`); await p.waitForTimeout(600);
  ok(psql(`select cuenta_codigo from gasto_clasif where gasto_id = ${ID0}`) === '3.09', 'desactivar la regla: el estampado de Victoria Cofre vuelve a Aseo (su categoría)');
  await p.fill('#nr-pal', 'estampado');
  ok(/Calza con 2 gastos/.test(await p.textContent('#nr-prueba')), 'nueva regla: muestra con cuántos gastos calza antes de guardar');

  // ── Proveedores ──
  await p.click('[data-gsub="proveedores"]'); await p.waitForTimeout(200);
  await p.selectOption('#gsub-proveedores tr:has-text("FERROSTAAL") select >> nth=0', 'afecta');
  await p.waitForTimeout(300);
  ok(psql(`select tipo_documento from proveedores where id = 13`) === 'afecta', 'proveedor: tipo de documento guardado');

  // ── Conciliación ──
  await p.click('[data-gsub="conciliacion"]'); await p.waitForSelector('#conc-kpis .kpi:nth-child(4)');
  const conc = (await p.textContent('#conc-kpis')).replace(/\s+/g, ' ');
  ok(/Diferencia\s*\$0\s*✓ Cuadra/.test(conc), 'conciliación: diferencia $0 y cuadra (' + conc.slice(0, 160) + '…)');
  ok(/Oct 2026/.test(await p.textContent('#gsub-conciliacion')) && !/Mar 2026/.test(await p.textContent('#gsub-conciliacion')), 'por mes desde abril (marzo no aparece)');
  ok(p.errores.length === 0, 'sin errores en la página ' + JSON.stringify(p.errores));
  await p.setViewportSize({ width: 390, height: 844 }); await p.click('[data-gsub="revision"]'); await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(__dirname, 'clasif_revision_movil.png') });
  ok(await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), 'celular: Revisión no se sale del ancho');

  // ── Sin el SQL 21A: Gastos funciona como antes ──
  sinSQL21 = true;
  const q = await abrir();
  await q.waitForFunction(() => clasifEstado === 'no_existe', null, { timeout: 8000 });
  await q.evaluate(() => renderGastos());
  ok(/SQL 21A/.test(await q.textContent('#gsub-bar')) && await q.textContent('#th-cat-g') === 'Categoría', 'sin SQL 21A: aviso y lista con categorías');
  await q.evaluate(() => abrirNuevoGasto());
  ok(await q.isVisible('#g-cat') && !(await q.$('#g-cta')), 'sin SQL 21A: el formulario es el de siempre');
  ok(q.errores.length === 0, 'sin SQL 21A: sin errores ' + JSON.stringify(q.errores));
  await b.close();
  psql(`drop database if exists ${BASE}`, 'postgres');
  console.log(fallas ? `\n${fallas} FALLAS` : '\nTODO OK');
  process.exit(fallas ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
