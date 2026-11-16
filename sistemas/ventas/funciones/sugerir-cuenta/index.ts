// Supabase Edge Function «sugerir-cuenta» · base de VENTAS (nnisdusdujcpkrbjqnhe)
// Claude sugiere a qué cuenta del plan corresponde un gasto. La usa Ventas › Gastos con el botón
// «Preguntar a Claude» (formulario y Revisión) y la «Prueba de Claude».
//
// - La clave de Anthropic se lee del secreto ANTHROPIC_API_KEY (Edge Functions › Secrets): nunca llega a la página.
// - Lo que ve Claude (plan de cuentas, reglas, ejemplos ya clasificados y gastos anteriores del proveedor) lo arma
//   la base con gasto_ia_contexto (SQL 21C); cada consulta queda registrada en gasto_ia_consultas con su costo, y
//   gasto_ia_reservar aplica el tope diario.
// - Claude solo puede responder una cuenta del plan (lista cerrada): no puede inventar cuentas.
// - Nada se guarda en el gasto: la persona acepta o elige otra cuenta en Ventas.
import Anthropic from "npm:@anthropic-ai/sdk@1.8.0";

// Precios de lista en dólares por millón de tokens (entrada, salida, lectura y escritura del caché de 5 minutos)
const PRECIOS = {
  "claude-opus-5-5": { entrada: 4, salida: 20, lectura: 0.2, escritura: 5 },
  "claude-haiku-5-5": { entrada: 0.1, salida: 0.5, lectura: 0.01, escritura: 0.125 },
};
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const NIVELES = {
  "1": "Ingresos", "2": "Costo directo variable", "3": "Gasto general de producción", "4": "Gasto general de venta y marketing",
  "5": "Gasto general de administración", "6": "Bajo el EBITDA", "F": "Fuera del estado de resultados",
};

const pesos = (n) => "$" + Math.round(Number(n) || 0).toLocaleString("es-CL");
const limpio = (s) => String(s ?? "").replace(/\s+/g, " ").trim();

// ── Lo que lee Claude ────────────────────────────────────────────────────────────────────────────────
// Parte fija (igual en todas las consultas, para que el caché la reutilice): instrucciones, plan, reglas y ejemplos
export function armarSistema(ctx) {
  const cuentas = ctx.cuentas || [], nombre = {};
  cuentas.forEach((c) => { nombre[c.codigo] = c.nombre; });
  const reglas = (ctx.reglas || []).map((r) => {
    const si = r.tipo === "palabra" ? `la descripción dice «${r.palabra}»`
      : r.tipo === "proveedor" ? `el proveedor es «${r.proveedor}»`
      : `el proveedor es «${r.proveedor}» y la descripción dice «${r.palabra}»`;
    return `- Si ${si}: ${r.accion === "revisar" ? "se revisa a mano" : `${r.cuenta} ${nombre[r.cuenta] || ""}`}${r.motivo ? ` (${limpio(r.motivo)})` : ""}`;
  });
  const plan = cuentas.map((c) => `${c.codigo} ${c.nombre} [${NIVELES[c.nivel] || c.nivel}]: ${limpio(c.que_entra)}`);
  const ejemplos = (ctx.ejemplos || []).map((e) => `- ${limpio(e.descripcion) || "(sin descripción)"} | ${limpio(e.proveedor) || "(sin proveedor)"} | ${pesos(e.monto)} → ${e.cuenta}`);
  return [
    "Eres el asistente contable de Playmaker, una fábrica chilena de uniformes deportivos sublimados (camisetas, shorts, medias, polerones) que vende a clubes y colegios. Tu tarea es elegir a qué cuenta del plan de cuentas corresponde un gasto, para separar bien el costo directo de las prendas del gasto general de la empresa.",
    "",
    "Cómo está ordenado el plan:",
    "- Nivel 1: ingresos (las devoluciones a clientes restan de las ventas).",
    "- Nivel 2: costo directo variable, lo que se consume en los pedidos (tela, talleres, papel y tinta, aplicaciones, avíos, packaging, prendas para reventa, comisiones de venta, despachos a clientes).",
    "- Niveles 3, 4 y 5: gasto general de producción, de venta y marketing, y de administración.",
    "- Nivel 6: bajo el EBITDA (intereses, impuesto a la renta).",
    "- F: fuera del estado de resultados (pago de IVA, inversiones y mejoras del local, garantía, cuotas de préstamos, retiros y gastos personales de socios, ajustes).",
    "",
    "Criterios:",
    "- Lee la descripción y el proveedor. Los gastos anteriores del mismo proveedor, si vienen, son la mejor pista, pero un mismo proveedor puede ir a cuentas distintas según lo que se compró.",
    "- Los insumos que se gastan (tintas, papel, agujas, repuestos) nunca son inversión.",
    "- Una máquina o mueble de $300.000 o más que dura más de un año es inversión; bajo ese monto es gasto.",
    "- Pagos a los socios (Sean Duarte, Silvia Urbina): pueden ser remuneración, reembolso de un gasto de la empresa (va a la cuenta de ese gasto), gasto personal o retiro. Si no se sabe cuál, baja la confianza.",
    "- Si la descripción es vaga («compra», «pago», «no sé»), elige la cuenta más probable y baja la confianza.",
    "- confianza: número entre 0 y 1; usa 0,9 o más solo si estás seguro. motivo: una frase corta en español. alternativa: la segunda cuenta más probable, o «ninguna».",
    "",
    "Reglas fijas de la empresa (se aplican antes de preguntarte; úsalas como criterio):",
    ...(reglas.length ? reglas : ["- (sin reglas)"]),
    "",
    "Plan de cuentas (código, nombre, nivel y qué entra):",
    ...plan,
    "",
    "Ejemplos de gastos ya clasificados (descripción | proveedor | monto con impuestos → cuenta):",
    ...(ejemplos.length ? ejemplos : ["- (sin ejemplos todavía)"]),
  ].join("\n");
}

// Parte que cambia: el gasto y los anteriores de su proveedor
export function armarMensaje(gasto, ctx) {
  const nombre = {};
  (ctx.cuentas || []).forEach((c) => { nombre[c.codigo] = c.nombre; });
  const hist = (ctx.historial || []).map((h) => `- ${h.fecha || ""} · ${limpio(h.descripcion) || "(sin descripción)"} · ${pesos(h.monto)} → ${h.cuenta} ${nombre[h.cuenta] || ""}`.trimEnd());
  return [
    "Gasto a clasificar:",
    `- Descripción: ${limpio(gasto.descripcion) || "(sin descripción)"}`,
    `- Proveedor: ${limpio(gasto.proveedor) || "(sin proveedor)"}`,
    `- Monto (con impuestos): ${pesos(gasto.monto)}`,
    `- Fecha de pago: ${gasto.fecha || "(sin fecha)"}`,
    "",
    "Gastos anteriores de este proveedor:",
    ...(hist.length ? hist : ["- (ninguno)"]),
  ].join("\n");
}

// Respuesta obligada: una cuenta del plan, la confianza, el motivo y una alternativa
export function esquema(ctx) {
  const codigos = (ctx.cuentas || []).map((c) => c.codigo);
  return {
    type: "object",
    properties: {
      cuenta: { type: "string", enum: codigos },
      confianza: { type: "number" },
      motivo: { type: "string" },
      alternativa: { type: "string", enum: [...codigos, "ninguna"] },
    },
    required: ["cuenta", "confianza", "motivo", "alternativa"],
    additionalProperties: false,
  };
}

export function costoUsd(modelo, u) {
  const p = PRECIOS[modelo] || PRECIOS["claude-opus-5-5"];
  return ((u.input_tokens || 0) * p.entrada + (u.output_tokens || 0) * p.salida +
    (u.cache_read_input_tokens || 0) * p.lectura + (u.cache_creation_input_tokens || 0) * p.escritura) / 1e6;
}

// Una consulta a Claude. Opus 5.5 lleva el respaldo del servidor: si declinara por seguridad, responde otro modelo.
export async function preguntarAClaude(cliente, modelo, ctx, gasto) {
  const params = {
    model: modelo,
    max_tokens: 2000,
    system: [{ type: "text", text: armarSistema(ctx), cache_control: { type: "ephemeral" } }],
    messages: [{ role: "user", content: armarMensaje(gasto, ctx) }],
    output_config: { effort: "low", format: { type: "json_schema", schema: esquema(ctx) } },
  };
  const r = modelo === "claude-opus-5-5"
    ? await cliente.beta.messages.create({ ...params, betas: ["server-side-fallback-2026-07-01"], fallbacks: "default" })
    : await cliente.messages.create(params);
  if (r.stop_reason === "refusal") throw new Error("Claude no quiso responder esta consulta.");
  if (r.stop_reason === "max_tokens") throw new Error("La respuesta de Claude quedó cortada.");
  const texto = r.content.filter((b) => b.type === "text").map((b) => b.text).join("");
  let x;
  try { x = JSON.parse(texto); } catch (_e) { throw new Error("Claude respondió en un formato inesperado."); }
  const codigos = new Set((ctx.cuentas || []).map((c) => c.codigo));
  if (!codigos.has(x.cuenta)) throw new Error("Claude respondió una cuenta que no está en el plan.");
  const confianza = Math.max(0, Math.min(1, Number(x.confianza) || 0));
  return {
    cuenta: x.cuenta, confianza, motivo: limpio(x.motivo).slice(0, 300),
    alternativa: codigos.has(x.alternativa) && x.alternativa !== x.cuenta ? x.alternativa : null,
    modelo_respuesta: r.model, usage: r.usage || {},
  };
}

// ── Servicio ─────────────────────────────────────────────────────────────────────────────────────────
const env = (k) => (typeof Deno !== "undefined" ? Deno.env.get(k) : undefined);
const responder = (cuerpo, estado = 200) =>
  new Response(JSON.stringify(cuerpo), { status: estado, headers: { ...CORS, "Content-Type": "application/json" } });

// Llave de servicio de la base: la de siempre (SUPABASE_SERVICE_ROLE_KEY) o, en proyectos con las llaves nuevas
// de Supabase, la secreta (sb_secret_…, que va solo en el encabezado apikey)
function llaveServicio() {
  const vieja = env("SUPABASE_SERVICE_ROLE_KEY");
  if (vieja) return vieja;
  try {
    const nuevas = JSON.parse(env("SUPABASE_SECRET_KEYS") || "{}");
    const k = nuevas.default || Object.values(nuevas)[0];
    if (k) return String(k);
  } catch (_e) { /* sin llaves nuevas */ }
  return env("SUPABASE_SECRET_KEY") || "";
}
async function rpc(fn, args) {
  const url = env("SUPABASE_URL"), llave = llaveServicio();
  if (!llave) throw new Error("La función no encuentra la llave de servicio de Supabase.");
  const headers = { apikey: llave, "Content-Type": "application/json" };
  if (!llave.startsWith("sb_")) headers.Authorization = `Bearer ${llave}`;
  const r = await fetch(`${url}/rest/v1/rpc/${fn}`, { method: "POST", headers, body: JSON.stringify(args) });
  const t = await r.text();
  if (!r.ok) throw new Error(t || `HTTP ${r.status}`);
  return t ? JSON.parse(t) : null;
}

export async function atender(req) {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return responder({ error: "Usa POST." }, 405);
  if (!env("ANTHROPIC_API_KEY")) return responder({ error: "Falta el secreto ANTHROPIC_API_KEY en Edge Functions › Secrets." }, 500);
  let id = null;
  try {
    const b = await req.json();
    const modo = b.modo === "prueba" ? "prueba" : "sugerir";
    const g = b.gasto || {};
    const gasto = { id: g.id ?? null, fecha: g.fecha || null, monto: g.monto, descripcion: g.descripcion || "", proveedor: g.proveedor || "" };
    const ctx = await rpc("gasto_ia_contexto", { p_gasto: gasto });
    if (!ctx || !(ctx.cuentas || []).length) return responder({ error: "No se pudo leer el plan de cuentas." }, 500);
    const modelo = PRECIOS[b.modelo] ? b.modelo : PRECIOS[ctx.modelo] ? ctx.modelo : "claude-opus-5-5";
    id = await rpc("gasto_ia_reservar", {
      p_modo: modo, p_modelo: modelo, p_gasto_id: gasto.id != null ? Number(gasto.id) : null, p_usuario: String(b.usuario || "").slice(0, 80),
      p_lote: b.lote ? String(b.lote).slice(0, 60) : null, p_grupo: b.grupo ? String(b.grupo).slice(0, 20) : null,
      p_cuenta_real: b.cuenta_real ? String(b.cuenta_real).slice(0, 10) : null,
    });
    const cliente = new Anthropic({ apiKey: env("ANTHROPIC_API_KEY"), timeout: 60000, maxRetries: 2 });
    const t0 = Date.now();
    const x = await preguntarAClaude(cliente, modelo, ctx, gasto);
    const u = x.usage, costo = costoUsd(modelo, u);
    await rpc("gasto_ia_completar", { p_id: id, p_datos: {
      modelo_respuesta: x.modelo_respuesta, cuenta_sugerida: x.cuenta, confianza: x.confianza, motivo: x.motivo, alternativa: x.alternativa,
      input_tokens: u.input_tokens, output_tokens: u.output_tokens, cache_lectura: u.cache_read_input_tokens, cache_escritura: u.cache_creation_input_tokens,
      costo_usd: costo, duracion_ms: Date.now() - t0 } });
    const nombre = (c) => ((ctx.cuentas || []).find((k) => k.codigo === c) || {}).nombre || c;
    return responder({ id, cuenta: x.cuenta, nombre: nombre(x.cuenta), confianza: x.confianza, motivo: x.motivo,
      alternativa: x.alternativa, alternativa_nombre: x.alternativa ? nombre(x.alternativa) : null, modelo: x.modelo_respuesta, costo_usd: costo });
  } catch (e) {
    let msg = e instanceof Error ? e.message : String(e), estado = 500;
    if (e instanceof Anthropic.AuthenticationError) msg = "La clave de Anthropic no es válida: revisa el secreto ANTHROPIC_API_KEY.";
    else if (e instanceof Anthropic.PermissionDeniedError) msg = "La clave de Anthropic no tiene permiso para este modelo.";
    else if (e instanceof Anthropic.RateLimitError) { msg = "Anthropic pidió esperar un momento: intenta de nuevo."; estado = 429; }
    else if (e instanceof Anthropic.APIError) msg = `Anthropic respondió ${e.status}: ${e.message}`;
    else if (/TOPE_DIARIO/.test(msg)) { msg = msg.replace(/^.*TOPE_DIARIO:\s*/s, "Se alcanzó el tope diario de consultas: ").replace(/".*$/s, ""); estado = 429; }
    if (id != null) { try { await rpc("gasto_ia_completar", { p_id: id, p_datos: { error: msg.slice(0, 500) } }); } catch (_e) { /* el registro no impide responder */ } }
    return responder({ error: msg }, estado);
  }
}

if (typeof Deno !== "undefined") Deno.serve(atender);
