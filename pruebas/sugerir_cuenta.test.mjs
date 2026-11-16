// Función «sugerir-cuenta» (Supabase Edge Function de Ventas) probada en Node con el SDK oficial de Anthropic:
// Anthropic simulado (se revisa lo que se le envía) y Supabase atendido por un Postgres local con los SQL 21A, 21B y 21C
// (se usan de verdad gasto_ia_contexto, gasto_ia_reservar y gasto_ia_completar y el tope diario).
// Requiere: node_modules con @anthropic-ai/sdk 1.8.0 (SDK=ruta a esa carpeta) y Postgres local con la base indicada en
// PGBASE (gastos ya clasificados con los SQL 21A–21C) y el rol service_role.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const SDK = process.env.SDK || path.resolve(aqui, 'node_modules/@anthropic-ai/sdk');
const PSQL = process.env.PSQL || '/usr/lib/postgresql/16/bin/psql';
const PG = ['-h', process.env.PGHOST || '/home/postgres', '-p', process.env.PGPORT || '5499', '-U', 'postgres', '-d', process.env.PGBASE || 'v21'];
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if (!c) fallas++; };
const psql = sql => execFileSync(PSQL, [...PG, '-q', '-At', '-v', 'ON_ERROR_STOP=1'], { input: sql, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
const lit = v => '$J$' + String(v).replace(/\$J\$/g, '') + '$J$';

// ── Supabase simulado: /rest/v1/rpc/<fn> como service_role contra el Postgres local ──
const sb = http.createServer((req, res) => {
  let cuerpo = ''; req.on('data', d => cuerpo += d); req.on('end', () => {
    const fn = req.url.match(/\/rest\/v1\/rpc\/(\w+)/)[1], args = JSON.parse(cuerpo || '{}');
    try {
      const sql = `set role service_role; select coalesce(to_jsonb(public.${fn}(${Object.entries(args).map(([k, v]) => `${k} => ${v === null ? 'null' : typeof v === 'object' ? lit(JSON.stringify(v)) + '::jsonb' : lit(v)}`).join(', ')}))::text, 'null')`;
      const t = psql(sql).split('\n').pop();
      res.writeHead(200, { 'Content-Type': 'application/json' }); res.end(t);
    } catch (e) { res.writeHead(400, { 'Content-Type': 'application/json' }); res.end(JSON.stringify({ message: String(e.stderr || e.message) })); }
  });
});
// ── Anthropic simulado ──
let pedidos = [], respuesta = null;
const an = http.createServer((req, res) => {
  let cuerpo = ''; req.on('data', d => cuerpo += d); req.on('end', () => {
    pedidos.push({ url: req.url, headers: req.headers, body: JSON.parse(cuerpo) });
    const r = typeof respuesta === 'function' ? respuesta(JSON.parse(cuerpo)) : respuesta;
    res.writeHead(r.status || 200, { 'Content-Type': 'application/json', 'request-id': 'req_prueba' }); res.end(JSON.stringify(r.body));
  });
});
const escuchar = s => new Promise(r => s.listen(0, '127.0.0.1', () => r(s.address().port)));
const pSb = await escuchar(sb), pAn = await escuchar(an);
const mensaje = (texto, extra) => ({ body: Object.assign({ id: 'msg_1', type: 'message', role: 'assistant', model: 'claude-opus-5-5', stop_reason: 'end_turn', stop_sequence: null,
  content: [{ type: 'thinking', thinking: '', signature: 'x' }, { type: 'text', text: texto }],
  usage: { input_tokens: 400, output_tokens: 150, cache_read_input_tokens: 7000, cache_creation_input_tokens: 0 } }, extra || {}) });

// ── La función, tal como se publica, con Deno simulado ──
const vars = { SUPABASE_URL: `http://127.0.0.1:${pSb}`, SUPABASE_SERVICE_ROLE_KEY: 'llave-servicio', ANTHROPIC_API_KEY: 'sk-ant-prueba' };
globalThis.Deno = { env: { get: k => vars[k] }, serve() {} };
process.env.ANTHROPIC_BASE_URL = `http://127.0.0.1:${pAn}`;
const fuente = fs.readFileSync(path.resolve(aqui, '../sistemas/ventas/funciones/sugerir-cuenta/index.ts'), 'utf8')
  .replace('"npm:@anthropic-ai/sdk@1.8.0"', JSON.stringify(pathToFileURL(path.join(SDK, 'index.mjs')).href));
const tmp = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'fn-')), 'index.mjs'); fs.writeFileSync(tmp, fuente);
const F = await import(pathToFileURL(tmp).href);
const llamar = async b => { const r = await F.atender(new Request('http://x/', { method: 'POST', body: JSON.stringify(b) })); return { status: r.status, j: await r.json() }; };

psql(`update gestion_parametros set valor = '100' where clave = 'ia_tope_diario'; delete from gasto_ia_consultas;`);
const gasto = { id: 999, fecha: '2026-11-14', monto: 85000, descripcion: 'ESTAMPADO 2 DIAS', proveedor: 'VICTORIA COFRE' };

// 1 · Opus: lo que se envía y lo que se guarda
respuesta = mensaje(JSON.stringify({ cuenta: '3.04', confianza: 0.93, motivo: 'El estampado es jornal de producción.', alternativa: '3.09' }));
let r = await llamar({ modo: 'sugerir', usuario: 'Sean Duarte', gasto });
const p = pedidos.pop();
ok(r.status === 200 && r.j.cuenta === '3.04' && r.j.nombre === 'Jornales de producción' && r.j.alternativa === '3.09' && r.j.confianza === 0.93, 'responde la cuenta, su nombre, la confianza y la alternativa: ' + JSON.stringify(r.j));
ok(p.body.model === 'claude-opus-5-5' && (p.headers['x-api-key'] === 'sk-ant-prueba' || p.headers['authorization'] === 'Bearer sk-ant-prueba') && /server-side-fallback-2026-07-01/.test(p.headers['anthropic-beta'] || '') && p.body.fallbacks === 'default', 'Opus 5.5 con la clave del secreto y el respaldo del servidor');
const sch = p.body.output_config && p.body.output_config.format && p.body.output_config.format.schema;
ok(p.body.output_config.effort === 'low' && sch && sch.properties.cuenta.enum.length === 52 && sch.properties.cuenta.enum.includes('3.04') && sch.additionalProperties === false, 'la respuesta está obligada a una de las 52 cuentas (esfuerzo bajo)');
ok(p.body.system[0].cache_control && p.body.system[0].cache_control.type === 'ephemeral' && /Plan de cuentas/.test(p.body.system[0].text) && /ESTAMPADO/.test(p.body.system[0].text), 'el plan, las reglas y los ejemplos van en la parte fija, con caché');
ok(/Gasto a clasificar:[\s\S]*ESTAMPADO 2 DIAS[\s\S]*VICTORIA COFRE[\s\S]*\$85\.000[\s\S]*Gastos anteriores de este proveedor:\n- 2026-10-26 · ESTAMPADO · \$120\.000 → 3\.04 Jornales de producción/.test(p.body.messages[0].content), 'el gasto y los anteriores del proveedor van en el mensaje');
const tokens = Math.round(p.body.system[0].text.length / 3.5);
console.log('     parte fija ≈', tokens, 'tokens (estimado por caracteres)');
let fila = JSON.parse(psql(`select row_to_json(c) from gasto_ia_consultas c order by id desc limit 1`));
const costoEsp = (400 * 4 + 150 * 20 + 7000 * 0.2) / 1e6;
ok(fila.modo === 'sugerir' && fila.cuenta_sugerida === '3.04' && +fila.confianza === 0.93 && fila.usuario === 'Sean Duarte' && Math.abs(+fila.costo_usd - costoEsp) < 1e-9 && fila.cache_lectura === 7000 && fila.gasto_id === 999,
  'queda registrada con tokens y costo (US$' + (+fila.costo_usd).toFixed(4) + ')');
// la parte fija es igual para dos gastos distintos (el caché sirve)
await llamar({ modo: 'sugerir', usuario: 'Sean Duarte', gasto: { ...gasto, id: 998, descripcion: 'OTRA COSA', proveedor: 'OTRO' } });
ok(pedidos.pop().body.system[0].text === p.body.system[0].text, 'la parte fija no cambia entre consultas (el caché se reutiliza)');

// 2 · Haiku en la prueba de precisión: sin respaldo del servidor, con lote, grupo y cuenta real
respuesta = mensaje(JSON.stringify({ cuenta: '3.09', confianza: 0.55, motivo: 'Aseo.', alternativa: 'ninguna' }), { model: 'claude-haiku-5-5' });
r = await llamar({ modo: 'prueba', modelo: 'claude-haiku-5-5', lote: 'L1', grupo: 'dificil', cuenta_real: '3.04', usuario: 'Sean Duarte', gasto });
const p2 = pedidos.pop();
ok(r.status === 200 && p2.body.model === 'claude-haiku-5-5' && !p2.body.fallbacks && !/server-side-fallback/.test(p2.headers['anthropic-beta'] || '') && r.j.alternativa === null, 'Haiku 5.5: sin respaldo del servidor; «ninguna» queda sin alternativa');
fila = JSON.parse(psql(`select row_to_json(c) from gasto_ia_consultas c order by id desc limit 1`));
ok(fila.modo === 'prueba' && fila.lote === 'L1' && fila.grupo === 'dificil' && fila.cuenta_real === '3.04' && fila.modelo === 'claude-haiku-5-5', 'la prueba guarda lote, grupo y la cuenta real');

// 3 · errores: cuenta fuera del plan, clave inválida y tope diario
respuesta = mensaje(JSON.stringify({ cuenta: '9.99', confianza: 1, motivo: 'x', alternativa: 'ninguna' }));
r = await llamar({ modo: 'sugerir', gasto });
ok(r.status === 500 && /no está en el plan/.test(r.j.error) && /no está en el plan/.test(psql(`select error from gasto_ia_consultas order by id desc limit 1`)), 'una cuenta fuera del plan no se acepta y queda el error registrado');
respuesta = { status: 401, body: { type: 'error', error: { type: 'authentication_error', message: 'invalid x-api-key' } } };
r = await llamar({ modo: 'sugerir', gasto });
ok(/clave de Anthropic no es válida/.test(r.j.error), 'clave inválida: lo dice claro');
psql(`update gestion_parametros set valor = '4' where clave = 'ia_tope_diario'`);   // ya van 4 consultas «sugerir» hoy
respuesta = mensaje(JSON.stringify({ cuenta: '3.04', confianza: 0.9, motivo: 'x', alternativa: 'ninguna' }));
const n0 = pedidos.length;
r = await llamar({ modo: 'sugerir', gasto });
ok(r.status === 429 && /tope diario de consultas: hoy ya se hicieron 4 consultas \(tope 4\)/.test(r.j.error) && pedidos.length === n0, 'tope diario: no llama a Claude y lo dice: ' + r.j.error);
psql(`update gestion_parametros set valor = '100' where clave = 'ia_tope_diario'`);
delete vars.ANTHROPIC_API_KEY;
r = await llamar({ modo: 'sugerir', gasto });
ok(r.status === 500 && /Falta el secreto ANTHROPIC_API_KEY/.test(r.j.error), 'sin el secreto: lo dice');
r = await F.atender(new Request('http://x/', { method: 'OPTIONS' }));
ok(r.status === 200 && r.headers.get('access-control-allow-origin') === '*', 'responde el permiso del navegador (CORS)');

sb.close(); an.close();
console.log(fallas ? `\n${fallas} FALLAS` : '\nTODO OK');
process.exit(fallas ? 1 : 0);
