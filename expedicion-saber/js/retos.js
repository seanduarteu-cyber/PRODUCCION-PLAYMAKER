/* Sesión de 10 desafíos y los seis tipos de desafío. Depende de js/ui.js (window.ES). */
(function () {
  'use strict';
  const ES = window.ES, A = ES.A, { $, $$, esc } = ES;
  const barajar = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const barajarDistinto = (a, igual) => { let b = barajar(a); for (let k = 0; k < 8 && igual(b); k++) b = barajar(a); return b; };

  /* ---------- voz (lectura en voz alta en español) y sonidos ---------- */
  const Voz = {
    ok: 'speechSynthesis' in window && typeof SpeechSynthesisUtterance !== 'undefined', v: null,
    elegir() { try { const vs = speechSynthesis.getVoices(); const p = v => { const l = (v.lang || '').replace('_', '-'); return l.startsWith('es-CL') ? 4 : l.startsWith('es-419') || l.startsWith('es-MX') || l.startsWith('es-US') ? 3 : l.startsWith('es') ? 2 : 0; }; const b = vs.slice().sort((x, y) => p(y) - p(x))[0]; if (b && p(b)) this.v = b; } catch (e) { /* sin voces */ } },
    decir(t) { if (!this.ok) return; try { speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(t); u.lang = 'es-CL'; if (this.v) u.voice = this.v; u.rate = 0.92; speechSynthesis.speak(u); } catch (e) { /* ignorar */ } },
  };
  if (Voz.ok) { Voz.elegir(); try { speechSynthesis.addEventListener('voiceschanged', () => Voz.elegir()); } catch (e) { /* ignorar */ } }
  ES.detenerVoz = () => { try { if (Voz.ok) speechSynthesis.cancel(); } catch (e) { /* ignorar */ } };
  const paraVoz = t => t.replace(/\p{Extended_Pictographic}|\u{1F7E9}|⬜|️/gu, '').replace(/_{3}/g, ' espacio en blanco ').replace(/[«»]/g, '').replace(/−/g, ' menos ').replace(/×/g, ' por ').replace(/÷/g, ' dividido en ');

  let audio = null;
  ES.sonido = tipo => {
    if (!A.estado.ajustes || A.estado.ajustes.sonido === false) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      const notas = { bien: [660, 990], mal: [220], moneda: [1320, 1760], mejora: [523, 659, 784, 1047], nivel: [784, 1047] }[tipo] || [440];
      notas.forEach((f, i) => {
        const o = audio.createOscillator(), g = audio.createGain(), t0 = audio.currentTime + i * 0.09;
        o.type = tipo === 'mal' ? 'sawtooth' : 'square'; o.frequency.value = f;
        g.gain.setValueAtTime(0.05, t0); g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.16);
        o.connect(g); g.connect(audio.destination); o.start(t0); o.stop(t0 + 0.18);
      });
    } catch (e) { /* sin audio */ }
  };

  /* ---------- sesión ---------- */
  ES.iniciarSesion = (asig, oaId) => {
    const p = ES.perfil(), id = oaId || Motor.recomendar(p, asig, A.datos);
    if (!id) { ES.aviso('No hay objetivos disponibles en esta asignatura.'); return; }
    A.ses = { asig, oaId: id, i: 0, total: A.datos.eco.desafios_por_sesion, aciertos: 0, monedasDesafios: 0, dominios: 0, repaso: new Set() };
    ES.ir('sesion');
  };

  ES.registrarPantalla('sesion', main => {
    const s = A.ses, p = ES.perfil();
    if (!s) return ES.ir('base');
    if (p.oas[s.oaId] && p.oas[s.oaId].dominado) { const otro = Motor.recomendar(p, s.asig, A.datos); if (otro) s.oaId = otro; }
    s.d = Motor.ambientar(Motor.elegirDesafio(p, s.oaId, A.datos), ES.mundoActual().tokens);
    s.intento = 1; s.terminado = false;
    const d = s.d, st = Motor.estadoOA(p, s.oaId);
    const enun = d.tipo === 'completar' ? esc(d.enunciado).replace('___', '<span class="hueco" id="hueco">?</span>') : esc(d.enunciado);
    main.innerHTML = `<section class="pantalla"><article class="bloque pantalla reto">
      <div class="reto-cab"><span class="nota"><strong>${ES.NOMBRE_ASIG[s.asig]}</strong> · ${esc(ES.codigoCorto(s.oaId))}</span><span class="nota">Dificultad ${ES.pips(st.nivel)}</span></div>
      <div class="progreso" role="img" aria-label="Desafío ${s.i + 1} de ${s.total}">${Array.from({ length: s.total }, (_, k) => `<i class="${k < s.i ? 'hecho' : k === s.i ? 'actual' : ''}"></i>`).join('')}</div>
      ${d.texto ? `<div class="texto-lectura">${esc(d.texto)}</div>` : ''}
      <div class="enunciado"><p id="enunciado">${enun}</p>${Voz.ok ? '<button class="voz" type="button" id="btn-voz" aria-label="Escuchar el desafío">🔊</button>' : ''}</div>
      <p class="intento" id="intento"></p>
      <div id="zona"></div>
      <div id="retro" aria-live="polite"></div>
      <div class="fila"><button class="btn" type="button" id="btn-comprobar" hidden>Comprobar</button><button class="btn" type="button" id="btn-sig" hidden>Siguiente</button>
        <span id="salir"><button class="btn chico piedra" type="button" id="btn-salir">Salir</button></span></div>
    </article></section>`;
    actualizarIntento();
    const api = { intentar, comprobar: v => { $('#btn-comprobar').hidden = !v; } };
    WIDGETS[d.tipo](d, $('#zona', main), api);
    const leer = () => Voz.decir(paraVoz(`${d.texto ? d.texto + '. ' : ''}${d.enunciado}`));
    const vb = $('#btn-voz', main); if (vb) vb.addEventListener('click', leer);
    if (A.estado.ajustes.voz !== false && ['1_basico', '2_basico'].includes(p.nivel_escolar)) setTimeout(leer, 300);
    $('#btn-sig', main).addEventListener('click', siguiente);
    $('#btn-salir', main).addEventListener('click', () => {
      $('#salir').innerHTML = '<span class="nota">¿Salir? Las monedas ganadas se guardan, pero no recibes el bono de sesión.</span> <button class="btn chico tierra" type="button" id="si-salir">Salir</button> <button class="btn chico" type="button" id="no-salir">Seguir jugando</button>';
      $('#si-salir').addEventListener('click', () => { A.ses = null; ES.ir('base'); });
      $('#no-salir').addEventListener('click', () => { $('#salir').innerHTML = '<button class="btn chico piedra" type="button" id="btn-salir2">Salir</button>'; $('#btn-salir2').addEventListener('click', () => $('#btn-salir').click()); });
    });
  });

  function actualizarIntento() {
    const s = A.ses, m = Motor.monedasPorIntento(s.intento, A.datos);
    $('#intento').textContent = s.terminado ? '' : `Intento ${s.intento} de 3 · vale ${m} moneda${m === 1 ? '' : 's'}`;
  }

  function intentar(resp, marcar) {
    const s = A.ses; if (s.terminado) return;
    const r = Motor.corregir(s.d, resp);
    if (r.ok) return terminar(true);
    if (marcar) marcar(r);
    if (s.intento < 3) {
      s.intento++; ES.sonido('mal'); actualizarIntento();
      $('#retro').innerHTML = `<div class="retro pista">Pista: ${esc(s.d.pista)}${s.intento === 3 ? '<p>Es el último intento.</p>' : ''}</div>`;
    } else terminar(false);
  }

  function correctaTexto(d) {
    switch (d.tipo) {
      case 'opcion_multiple': case 'completar': return d.alternativas[d.correcta];
      case 'ordenar_secuencia': return d.elementos.join(' → ');
      case 'emparejar': return d.pares.map(([a, b]) => `${a} con ${b}`).join('; ');
      case 'arrastrar_categoria': return d.categorias.map((c, i) => `${c}: ${d.elementos.filter(e => e.categoria === i).map(e => e.texto).join(', ')}`).join(' · ');
      case 'respuesta_numerica': return `${d.tolerancia ? 'cerca de ' : ''}${d.respuesta.toLocaleString('es-CL')}${d.unidad ? ' ' + d.unidad : ''}`;
    }
    return '';
  }

  function terminar(ok) {
    const s = A.ses, p = ES.perfil(); s.terminado = true;
    const ganadas = ok ? Motor.monedasPorIntento(s.intento, A.datos) : 0;
    const ev = Motor.registrarResultado(p, s.oaId, { resuelto: ok, intento: s.intento }, A.datos);
    s.monedasDesafios += ganadas; if (ok && s.intento === 1) s.aciertos++;
    if (ev.dominado) s.dominios++;
    ev.repaso.forEach(x => s.repaso.add(x));
    ES.guardar(); ES.actualizarDock(ganadas > 0);
    $$('#zona button').forEach(b => { b.disabled = true; });
    $('#btn-comprobar').hidden = true; actualizarIntento();
    $('#retro').innerHTML = ok
      ? `<div class="retro bien">¡Correcto! +${ganadas} monedas</div>`
      : `<div class="retro mal">La respuesta correcta es: ${esc(correctaTexto(s.d))}<p>${esc(s.d.explicacion_error)}</p><p>Equivocarse no te quita monedas. ¡Sigue!</p></div>`;
    if (ok) { ES.sonido('moneda'); ES.celebrar(1.2); }
    if (ev.dominado) { ES.sonido('mejora'); ES.celebrar(2.5); ES.aviso('¡Dominaste el objetivo! +100 monedas', 3200); }
    else if (ev.subio) { ES.sonido('nivel'); ES.aviso(`¡Subes a dificultad ${Motor.estadoOA(p, s.oaId).nivel}!`); }
    else if (ev.bajo) ES.aviso(`Practiquemos en dificultad ${Motor.estadoOA(p, s.oaId).nivel}`);
    const sig = $('#btn-sig'); sig.hidden = false; sig.textContent = s.i + 1 >= s.total ? 'Ver resultado' : 'Siguiente'; sig.focus({ preventScroll: true });
  }

  function siguiente() {
    const s = A.ses; s.i++;
    if (s.i < s.total) return ES.ir('sesion');
    const p = ES.perfil(), r = Motor.cerrarSesion(p, A.datos);
    ES.guardar();
    const resumen = {
      asig: s.asig, aciertos: s.aciertos, total: s.total, monedasDesafios: s.monedasDesafios, dominios: s.dominios,
      bonoSesion: r.bonoSesion, bonoRacha: r.bonoRacha, repaso: [...s.repaso],
      total_monedas: s.monedasDesafios + s.dominios * A.datos.eco.bono_dominio_objetivo + r.bonoSesion + r.bonoRacha,
    };
    A.ses = null; ES.sonido('mejora'); ES.celebrar(2);
    ES.ir('fin', resumen);
  }

  document.addEventListener('keydown', e => {
    if (!A.ses || e.target.closest('input,select,textarea')) return;
    if (e.key === 'Enter') { const c = $('#btn-comprobar'), sg = $('#btn-sig'); if (sg && !sg.hidden) { e.preventDefault(); sg.click(); } else if (c && !c.hidden) { e.preventDefault(); c.click(); } return; }
    if (/^[1-4]$/.test(e.key)) { const b = $$('#zona [data-i]')[Number(e.key) - 1]; if (b && !b.disabled) b.click(); }
  });

  /* ---------- widgets por tipo ---------- */
  const WIDGETS = {};

  WIDGETS.opcion_multiple = (d, zona, api) => {
    zona.innerHTML = `<div class="opciones">${d.alternativas.map((a, i) => `<button class="opcion" type="button" data-i="${i}">${esc(a)}</button>`).join('')}</div>`;
    zona.addEventListener('click', e => {
      const b = e.target.closest('[data-i]'); if (!b || b.disabled) return;
      const i = Number(b.dataset.i);
      api.intentar(i, () => { b.classList.add('mala'); b.disabled = true; });
      if (A.ses.terminado) $$('[data-i]', zona)[d.correcta].classList.add('buena');
    });
  };

  WIDGETS.completar = (d, zona, api) => {
    zona.innerHTML = `<div class="fichas" role="group" aria-label="Elige la palabra que falta">${d.alternativas.map((a, i) => `<button class="ficha" type="button" data-i="${i}">${esc(a)}</button>`).join('')}</div>`;
    zona.addEventListener('click', e => {
      const b = e.target.closest('[data-i]'); if (!b || b.disabled) return;
      const hueco = $('#hueco'); hueco.textContent = d.alternativas[Number(b.dataset.i)];
      api.intentar(Number(b.dataset.i), () => { b.classList.add('mala'); b.disabled = true; setTimeout(() => { if (!A.ses.terminado) hueco.textContent = '?'; }, 700); });
      if (A.ses.terminado) hueco.textContent = d.alternativas[d.correcta];
    });
  };

  WIDGETS.ordenar_secuencia = (d, zona, api) => {
    let banco = barajarDistinto(d.elementos, b => b.join('|') === d.elementos.join('|')), fila = [], malos = [];
    const dibujar = () => {
      zona.innerHTML = `<p class="nota">Toca los elementos en orden. Toca uno de arriba para devolverlo.</p>
        <div class="fichas fila-respuesta" aria-label="Tu orden">${fila.map((t, i) => `<button class="ficha ${malos.includes(i) ? 'mala' : ''}" type="button" data-fila="${i}">${i + 1}. ${esc(t)}</button>`).join('') || '<span class="nota">Aquí va tu orden</span>'}</div>
        <div class="fichas" aria-label="Elementos por ordenar">${banco.map((t, i) => `<button class="ficha" type="button" data-banco="${i}">${esc(t)}</button>`).join('')}</div>`;
      api.comprobar(banco.length === 0 && !A.ses.terminado);
    };
    zona.addEventListener('click', e => {
      if (A.ses.terminado) return;
      const b = e.target.closest('[data-banco]'), f = e.target.closest('[data-fila]');
      if (b) { fila.push(banco.splice(Number(b.dataset.banco), 1)[0]); malos = []; dibujar(); }
      if (f) { banco.push(fila.splice(Number(f.dataset.fila), 1)[0]); malos = []; dibujar(); }
    });
    $('#btn-comprobar').onclick = () => api.intentar(fila.slice(), r => { malos = r.malos; dibujar(); });
    dibujar();
  };

  WIDGETS.emparejar = (d, zona, api) => {
    const izq = barajar(d.pares.map(p => p[0])), der = barajarDistinto(d.pares.map(p => p[1]), b => b.every((x, i) => d.pares.find(p => p[0] === izq[i])[1] === x));
    let sel = null; const par = {};
    const numero = a => izq.indexOf(a) + 1;
    const dibujar = (malos = []) => {
      const usado = Object.fromEntries(Object.entries(par).map(([a, b]) => [b, a]));
      zona.innerHTML = `<p class="nota">Toca un elemento de la izquierda y luego su pareja de la derecha.</p><div class="parejas">
        <div class="col">${izq.map(a => `<button class="ficha ${sel === a ? 'sel' : ''} ${malos.includes(a) ? 'mala' : ''}" type="button" data-izq="${esc(a)}" ${par[a] ? `data-par="${numero(a)}"` : ''}>${esc(a)}</button>`).join('')}</div>
        <div class="col">${der.map(b => `<button class="ficha" type="button" data-der="${esc(b)}" ${usado[b] ? `data-par="${numero(usado[b])}"` : ''}>${esc(b)}</button>`).join('')}</div></div>`;
      api.comprobar(Object.keys(par).length === izq.length && !A.ses.terminado);
    };
    zona.addEventListener('click', e => {
      if (A.ses.terminado) return;
      const a = e.target.closest('[data-izq]'), b = e.target.closest('[data-der]');
      if (a) { const k = a.dataset.izq; if (par[k] && sel !== k) delete par[k]; sel = sel === k ? null : k; dibujar(); }
      if (b && sel) { const v = b.dataset.der; for (const k in par) if (par[k] === v) delete par[k]; par[sel] = v; sel = null; dibujar(); }
    });
    $('#btn-comprobar').onclick = () => api.intentar({ ...par }, r => { r.malos.forEach(k => delete par[k]); dibujar(r.malos); });
    dibujar();
  };

  WIDGETS.arrastrar_categoria = (d, zona, api) => {
    const orden = barajar(d.elementos.map((_, i) => i)), asign = d.elementos.map(() => null);
    let sel = null, malos = [];
    const ficha = i => `<button class="ficha ${sel === i ? 'sel' : ''} ${malos.includes(i) ? 'mala' : ''}" type="button" data-el="${i}">${esc(d.elementos[i].texto)}</button>`;
    const dibujar = () => {
      zona.innerHTML = `<p class="nota">Arrastra cada elemento a su grupo, o tócalo y luego toca el grupo.</p>
        <div class="fichas" data-bandeja="-1" aria-label="Elementos sin ordenar">${orden.filter(i => asign[i] === null).map(ficha).join('') || '<span class="nota">¡Todo ubicado!</span>'}</div>
        <div class="bandejas">${d.categorias.map((c, k) => `<div class="bandeja" data-bandeja="${k}" role="button" tabindex="0" aria-label="Grupo ${esc(c)}"><h4>${esc(c)}</h4><div class="fichas">${orden.filter(i => asign[i] === k).map(ficha).join('')}</div></div>`).join('')}</div>`;
      api.comprobar(asign.every(a => a !== null) && !A.ses.terminado);
    };
    const mover = (i, k) => { asign[i] = k < 0 ? null : k; sel = null; malos = malos.filter(m => m !== i); dibujar(); };
    zona.addEventListener('click', e => {
      if (A.ses.terminado || arrastre.movido) return;
      const f = e.target.closest('[data-el]');
      if (f) { const i = Number(f.dataset.el); sel = sel === i ? null : i; dibujar(); return; }
      const b = e.target.closest('[data-bandeja]'); if (b && sel !== null) mover(sel, Number(b.dataset.bandeja));
    });
    zona.addEventListener('keydown', e => { const b = e.target.closest('.bandeja'); if (b && (e.key === 'Enter' || e.key === ' ') && sel !== null) { e.preventDefault(); mover(sel, Number(b.dataset.bandeja)); } });
    // arrastre con dedo o mouse
    const arrastre = { i: null, x: 0, y: 0, movido: false, el: null };
    zona.addEventListener('pointerdown', e => { const f = e.target.closest('[data-el]'); if (!f || A.ses.terminado) return; Object.assign(arrastre, { i: Number(f.dataset.el), x: e.clientX, y: e.clientY, movido: false, el: f }); });
    zona.addEventListener('pointermove', e => {
      if (arrastre.i === null) return;
      const dx = e.clientX - arrastre.x, dy = e.clientY - arrastre.y;
      if (!arrastre.movido && Math.hypot(dx, dy) > 8) { arrastre.movido = true; arrastre.el.style.position = 'relative'; arrastre.el.style.zIndex = 10; arrastre.el.style.pointerEvents = 'none'; }
      if (arrastre.movido) { arrastre.el.style.transform = `translate(${dx}px, ${dy}px)`; $$('.bandeja', zona).forEach(b => b.classList.toggle('blanco', b.contains(document.elementFromPoint(e.clientX, e.clientY)))); }
    });
    const soltar = e => {
      if (arrastre.i === null) return;
      if (arrastre.movido) { const destino = document.elementFromPoint(e.clientX, e.clientY), b = destino && destino.closest('[data-bandeja]'); mover(arrastre.i, b ? Number(b.dataset.bandeja) : -1); setTimeout(() => { arrastre.movido = false; }, 0); }
      arrastre.i = null;
    };
    zona.addEventListener('pointerup', soltar); zona.addEventListener('pointercancel', soltar);
    $('#btn-comprobar').onclick = () => api.intentar(asign.slice(), r => { malos = r.malos; r.malos.forEach(i => { asign[i] = null; }); dibujar(); });
    dibujar();
  };

  WIDGETS.respuesta_numerica = (d, zona, api) => {
    let valor = '';
    const dibujar = () => {
      zona.innerHTML = `<div class="fila"><output class="pantalla-num" id="num" aria-live="polite">${valor ? Number(valor).toLocaleString('es-CL') : '…'}</output>${d.unidad ? `<span>${esc(d.unidad)}</span>` : ''}${d.tolerancia ? '<span class="nota">Basta con una buena estimación.</span>' : ''}</div>
        <div class="teclado" role="group" aria-label="Teclado numérico">${['1', '2', '3', '4', '5', '6', '7', '8', '9', 'borrar', '0'].map(k => `<button class="tecla" type="button" data-k="${k}" aria-label="${k === 'borrar' ? 'Borrar' : k}">${k === 'borrar' ? '⌫' : k}</button>`).join('')}</div>`;
      api.comprobar(valor.length > 0 && !A.ses.terminado);
    };
    const pulsar = k => { if (A.ses.terminado) return; if (k === 'borrar') valor = valor.slice(0, -1); else if (valor.length < 6) valor = (valor + k).replace(/^0+(?=\d)/, ''); dibujar(); };
    zona.addEventListener('click', e => { const b = e.target.closest('[data-k]'); if (b) pulsar(b.dataset.k); });
    const teclas = e => { if (!A.ses || A.ses.d !== d) return document.removeEventListener('keydown', teclas); if (/^\d$/.test(e.key)) pulsar(e.key); else if (e.key === 'Backspace') pulsar('borrar'); };
    document.addEventListener('keydown', teclas);
    $('#btn-comprobar').onclick = () => api.intentar(Number(valor), () => { valor = ''; dibujar(); });
    dibujar();
  };
})();
