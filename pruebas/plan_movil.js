// Planificación en el celular: todas las pestañas (administrador) y el detalle de un proyecto
const { chromium, contexto, revisar } = require('./comun_movil');
const d = n => { const x = new Date(); x.setDate(x.getDate() + n); return x.toISOString().slice(0, 10); };
const ETS = ['ARMADO', 'CORTE', 'REVISION', 'PLOTEO', 'SUBL', 'CONFEC', 'ESTAMP', 'ENTREGA'];
const proys = Array.from({ length: 8 }, (_, i) => ({ id: i + 1, cot: 'COT-36' + (10 + i), cliente: 'Club Deportivo Universidad Católica Rugby Femenino ' + i, prendas: 40 + i,
  desglose: { 'FUT-HOMUC01|1 · MC': 20, 'SH-HOM|30': 20, 'MEDIAS-ADL': 20, 'VINILO': 20 }, moldes: [{ prenda: 'Camiseta', calce: 'Masculino', molde: '01 — Fútbol', codigo: 'FUT-HOMUC01', cant: 20, tallas: { S: 5, M: 10, L: 5 } }],
  fecha_ingreso_ficha: d(-5), fecha_entrega_cliente: d(10 + i), fecha_termino_interno: d(8 + i), tipo: 'Nacional', requiere_estampado: i % 2 === 0, requiere_sublimacion: true,
  observaciones: 'Entregar antes del torneo; revisar tallas especiales.', estado_general: 'en_produccion', responsable_ficha: 'Sean Duarte', created_at: new Date().toISOString() }));
const etapas = []; let eid = 1;
proys.forEach((p, i) => ETS.forEach((k, j) => etapas.push({ id: eid++, planificacion_id: p.id, etapa: k, estado: j < i % 5 ? 'terminado' : j === i % 5 ? 'en_proceso' : 'pendiente',
  fecha_limite: d(j + i - 3), fecha_inicio_real: j <= i % 5 ? d(-3) : null, fecha_termino_real: j < i % 5 ? d(-1) : null, responsable: j <= i % 5 ? 'Pedro Corte' : null })));
const datos = { tablas: { planificacion: u => /select=cot/.test(u.search) ? proys.map(p => ({ cot: p.cot })) : proys, planificacion_etapas: etapas,
  plan_usuarios: [{ usuario: 'sean.duarte', nombre: 'Sean Duarte', rol: 'admin', roles: ['admin'], activo: true }, { usuario: 'pedro.corte', nombre: 'Pedro Corte', rol: 'CORTE', roles: ['CORTE'], activo: true }],
  ejecutantes: [{ id: 1, nombre: 'Pedro Corte', area: 'Corte', activo: true }, { id: 2, nombre: 'Taller Las Rosas', area: 'Confección', activo: true }] } };
(async () => {
  const b = await chromium.launch();
  const ctx = await contexto(b, datos);
  const p = await ctx.newPage(); const errores = []; p.on('pageerror', e => errores.push(e.message)); p.on('dialog', x => x.accept());
  await p.goto('https://planificacion-playmaker.netlify.app/#pmk_acceso=tok1'); await p.waitForTimeout(3000);
  const tabs = await p.evaluate(() => tabsPara());
  const informe = {};
  for (const t of tabs) {
    await p.evaluate(t => { TAB = t; renderTabs(); renderVista(); }, t); await p.waitForTimeout(900);
    informe[t] = await revisar(p); await p.screenshot({ path: 'movil/plan_' + t + '.png', fullPage: true });
  }
  await p.evaluate(() => { TAB = 'proyectos'; renderTabs(); renderVista(); verProyecto(1); }); await p.waitForTimeout(900);
  informe.proyecto = await revisar(p); await p.screenshot({ path: 'movil/plan_proyecto.png', fullPage: true });
  for (const [k, v] of Object.entries(informe)) console.log(k.padEnd(12), 'página', v.anchoPagina + '/' + v.ancho, '| recortados', v.cortados.length, v.cortados.slice(0, 3).join(' | '), '| fuera', v.fuera.length, v.fuera.slice(0, 3).join(' | '));
  console.log('errores JS:', errores.join(' | ') || 'ninguno');
  await b.close();
})();
