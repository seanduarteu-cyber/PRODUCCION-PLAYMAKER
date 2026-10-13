/* Motor de progresión y economía de Expedición Saber.
   Sin DOM: lo usan la interfaz (window.Motor) y las pruebas (require). */
(function (raiz) {
  'use strict';

  const NIVELES_ESCOLARES = ['1_basico', '2_basico', '3_basico', '4_basico', '5_basico', '6_basico', '7_basico', '8_basico',
    '1_medio', '2_medio', '3_medio', '4_medio'];
  const NOMBRE_NIVEL = {
    '1_basico': '1° básico', '2_basico': '2° básico', '3_basico': '3° básico', '4_basico': '4° básico', '5_basico': '5° básico',
    '6_basico': '6° básico', '7_basico': '7° básico', '8_basico': '8° básico', '1_medio': '1° medio', '2_medio': '2° medio',
    '3_medio': '3° medio', '4_medio': '4° medio',
  };
  const idxNivel = n => NIVELES_ESCOLARES.indexOf(n);

  /* ---------- datos ---------- */
  // bancos: arreglo de bloques OA (contenido de los JSON). mundos: mundos.json. indice: contenido/indice.json
  function prepararDatos(bancos, mundos, indice) {
    const objetivos = {};
    bancos.forEach(oa => { objetivos[oa.id_objetivo] = oa; });
    const numOA = id => Number(id.split('.OA')[1]);
    const orden = Object.keys(objetivos).sort((a, b) => {
      const A = objetivos[a], B = objetivos[b];
      return idxNivel(A.nivel) - idxNivel(B.nivel) || A.dificultad - B.dificultad || numOA(a) - numOA(b);
    });
    const mundoPorId = {};
    mundos.mundos.forEach(m => { mundoPorId[m.id] = m; });
    return { objetivos, orden, mundos: mundos.mundos, mundoPorId, eco: mundos.economia, prog: mundos.progresion, tramos: indice.tramos, indice };
  }

  /* ---------- perfiles ---------- */
  function crearPerfil(nombre, nivelEscolar, datos) {
    const avatares = {};
    datos.mundos.forEach(m => { avatares[m.id] = {}; m.espacios.forEach(e => { avatares[m.id][e.id] = 0; }); });
    return {
      id: 'p' + Date.now().toString(36) + Math.floor(Math.random() * 1e4).toString(36),
      nombre: String(nombre).trim().slice(0, 20) || 'Explorador',
      nivel_escolar: nivelEscolar, mundo: 'bloques', monedas: 0,
      racha: { dias: 0, ultimo: null }, oas: {}, avatares,
      historial: { sesiones: 0, desafios: 0, primer_intento: 0 },
      creado: new Date().toISOString(),
    };
  }

  function estadoOA(perfil, oaId) {
    if (!perfil.oas[oaId]) perfil.oas[oaId] = { nivel: 1, ok: 0, fallos: 0, dominado: false, vistos: [], respondidos: 0, aciertos: 0 };
    return perfil.oas[oaId];
  }

  /* ---------- árbol de prerequisitos ---------- */
  const asumido = (perfil, oa) => idxNivel(oa.nivel) < idxNivel(perfil.nivel_escolar);

  function prerequisitoCumplido(perfil, pid, datos) {
    const p = datos.objetivos[pid];
    if (!p) return true; // fuera del banco actual: no bloquea
    const st = perfil.oas[pid];
    return asumido(perfil, p) || (st && (st.dominado || st.nivel >= 3));
  }

  function disponibilidad(perfil, oaId, datos) {
    const oa = datos.objetivos[oaId];
    if (idxNivel(oa.nivel) > idxNivel(perfil.nivel_escolar)) return { ok: false, motivo: 'superior', faltan: [] };
    const faltan = oa.prerequisitos.filter(p => !prerequisitoCumplido(perfil, p, datos));
    return { ok: faltan.length === 0, motivo: faltan.length ? 'prerequisitos' : '', faltan };
  }

  // Nivel con contenido más cercano al del jugador, sin pasarse de su curso. Con asignatura, mira solo esa asignatura.
  function nivelDeTrabajo(perfil, datos, asignatura) {
    const ids = asignatura ? datos.orden.filter(id => datos.objetivos[id].asignatura === asignatura) : datos.orden;
    const conContenido = [...new Set(ids.map(id => datos.objetivos[id].nivel))];
    const propios = conContenido.filter(n => idxNivel(n) <= idxNivel(perfil.nivel_escolar));
    return propios.length ? propios[propios.length - 1] : conContenido[0];
  }

  function recomendar(perfil, asignatura, datos) {
    const nivel = nivelDeTrabajo(perfil, datos, asignatura);
    const candidatos = datos.orden.filter(id => datos.objetivos[id].asignatura === asignatura);
    const delNivel = candidatos.filter(id => datos.objetivos[id].nivel === nivel);
    const libre = lista => lista.find(id => !estadoOA(perfil, id).dominado && disponibilidad(perfil, id, datos).ok);
    // primero el nivel del jugador; si ya lo dominó todo, el primero pendiente de cualquier nivel permitido
    return libre(delNivel) || libre(candidatos) || null;
  }

  /* ---------- selección y ambientación de desafíos ---------- */
  function elegirDesafio(perfil, oaId, datos, rnd = Math.random) {
    const st = estadoOA(perfil, oaId);
    const delNivel = datos.objetivos[oaId].desafios.filter(d => d.dificultad === st.nivel);
    let nuevos = delNivel.filter(d => !st.vistos.includes(d.id));
    if (!nuevos.length) { st.vistos = st.vistos.filter(v => !delNivel.some(d => d.id === v)); nuevos = delNivel; }
    const d = nuevos[Math.floor(rnd() * nuevos.length)];
    st.vistos.push(d.id);
    if (st.vistos.length > 60) st.vistos.splice(0, st.vistos.length - 60);
    return d;
  }

  function ambientar(valor, tokens) {
    if (typeof valor === 'string') return valor.replace(/\{(\w+)\}/g, (m, k) => (k in tokens ? tokens[k] : m));
    if (Array.isArray(valor)) return valor.map(v => ambientar(v, tokens));
    if (valor && typeof valor === 'object') { const o = {}; for (const k in valor) o[k] = ambientar(valor[k], tokens); return o; }
    return valor;
  }

  /* ---------- corrección ---------- */
  function corregir(d, r) {
    switch (d.tipo) {
      case 'opcion_multiple':
      case 'completar':
        return { ok: r === d.correcta, malos: r === d.correcta ? [] : [r] };
      case 'ordenar_secuencia': {
        const malos = d.elementos.map((e, i) => (r[i] === e ? -1 : i)).filter(i => i >= 0);
        return { ok: r.length === d.elementos.length && malos.length === 0, malos };
      }
      case 'emparejar': {
        const malos = d.pares.filter(([a, b]) => r[a] !== b).map(([a]) => a);
        return { ok: malos.length === 0, malos };
      }
      case 'arrastrar_categoria': {
        const malos = d.elementos.map((e, i) => (r[i] === e.categoria ? -1 : i)).filter(i => i >= 0);
        return { ok: malos.length === 0, malos };
      }
      case 'respuesta_numerica': {
        const n = typeof r === 'number' ? r : Number(String(r).replace(/\./g, '').replace(',', '.'));
        const ok = Number.isFinite(n) && Math.abs(n - d.respuesta) <= d.tolerancia;
        return { ok, malos: ok ? [] : [n] };
      }
    }
    return { ok: false, malos: [] };
  }

  /* ---------- economía y dificultad adaptativa ---------- */
  const monedasPorIntento = (intento, datos) => (datos.eco.monedas_por_intento[intento - 1] || 0);

  // resultado: { resuelto: bool, intento: 1..3 }. Acierto = resuelto al primer intento.
  function registrarResultado(perfil, oaId, resultado, datos) {
    const st = estadoOA(perfil, oaId), prog = datos.prog, ev = { monedas: 0, subio: false, bajo: false, dominado: false, repaso: [] };
    const acierto = resultado.resuelto && resultado.intento === 1;
    st.respondidos++; perfil.historial.desafios++;
    if (resultado.resuelto) ev.monedas += monedasPorIntento(resultado.intento, datos);
    if (acierto) {
      st.aciertos++; perfil.historial.primer_intento++; st.fallos = 0; st.ok++;
      if (st.ok >= prog.aciertos_seguidos_para_subir) {
        st.ok = 0;
        if (st.nivel < 5) { st.nivel++; ev.subio = true; } else if (!st.dominado) { st.dominado = true; ev.dominado = true; ev.monedas += datos.eco.bono_dominio_objetivo; }
      }
    } else {
      st.ok = 0; st.fallos++;
      if (st.fallos >= prog.fallos_seguidos_para_bajar) {
        st.fallos = 0;
        if (st.nivel > 1) { st.nivel--; ev.bajo = true; } else {
          ev.repaso = datos.objetivos[oaId].prerequisitos.filter(p => datos.objetivos[p] && !(perfil.oas[p] && perfil.oas[p].dominado));
        }
      }
    }
    perfil.monedas += ev.monedas; // nunca se descuentan monedas por equivocarse
    return ev;
  }

  const fechaLocal = (d = new Date()) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  function diaAnterior(hoy) { const [y, m, d] = hoy.split('-').map(Number); return fechaLocal(new Date(y, m - 1, d - 1)); }

  // Se llama al completar una sesión de 10 desafíos. El bono de racha se paga una vez por día.
  function cerrarSesion(perfil, datos, hoy = fechaLocal()) {
    const eco = datos.eco, r = perfil.racha;
    let bonoRacha = 0;
    if (r.ultimo !== hoy) {
      r.dias = r.ultimo === diaAnterior(hoy) ? r.dias + 1 : 1;
      r.ultimo = hoy;
      bonoRacha = Math.min(r.dias * eco.racha.bono_por_dia, eco.racha.tope);
    }
    perfil.historial.sesiones++;
    perfil.monedas += eco.bono_sesion + bonoRacha;
    return { bonoSesion: eco.bono_sesion, bonoRacha, dias: r.dias };
  }

  /* ---------- tramos y avatar ---------- */
  function tramosDominados(perfil, datos) {
    return datos.tramos.filter(t => t.objetivos.every(id => perfil.oas[id] && perfil.oas[id].dominado)).map(t => t.id);
  }

  function infoMejora(perfil, mundoId, espacioId, datos) {
    const nivelActual = perfil.avatares[mundoId][espacioId], eco = datos.eco, maximo = eco.costos_por_nivel.length;
    if (nivelActual >= maximo) return { nivelActual, siguiente: null, costo: 0, puede: false, motivo: 'completo' };
    const siguiente = nivelActual + 1, costo = eco.costos_por_nivel[nivelActual];
    let tramosNecesarios = 0;
    if (siguiente === eco.nivel_final.nivel) {
      const finales = Object.values(perfil.avatares[mundoId]).filter(v => v >= eco.nivel_final.nivel).length;
      tramosNecesarios = finales + 1;
    }
    const tramos = tramosDominados(perfil, datos).length;
    const motivo = tramos < tramosNecesarios ? 'tramos' : perfil.monedas < costo ? 'monedas' : '';
    return { nivelActual, siguiente, costo, tramosNecesarios, tramos, puede: !motivo, motivo };
  }

  function comprarMejora(perfil, mundoId, espacioId, datos) {
    const info = infoMejora(perfil, mundoId, espacioId, datos);
    if (!info.puede) return { ok: false, info };
    perfil.monedas -= info.costo;
    perfil.avatares[mundoId][espacioId] = info.siguiente;
    return { ok: true, info };
  }

  /* ---------- persistencia local ---------- */
  const CLAVE = 'expedicion-saber-v1';
  function cargar(storage) {
    try { const raw = storage.getItem(CLAVE); if (raw) return JSON.parse(raw); } catch (e) { /* almacenamiento bloqueado */ }
    return { perfiles: {}, orden: [], activo: null, ajustes: { voz: true, sonido: true } };
  }
  function guardar(storage, estado) { try { storage.setItem(CLAVE, JSON.stringify(estado)); return true; } catch (e) { return false; } }

  const Motor = {
    NIVELES_ESCOLARES, NOMBRE_NIVEL, idxNivel, prepararDatos, crearPerfil, estadoOA, disponibilidad, nivelDeTrabajo, recomendar,
    elegirDesafio, ambientar, corregir, monedasPorIntento, registrarResultado, cerrarSesion, fechaLocal, diaAnterior,
    tramosDominados, infoMejora, comprarMejora, cargar, guardar, CLAVE,
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = Motor; else raiz.Motor = Motor;
})(typeof window !== 'undefined' ? window : globalThis);
