/* Interfaz de Expedición Saber: perfiles, mundos, base, árbol, taller y resumen de sesión.
   Los desafíos y la sesión están en js/retos.js. */
(function () {
  'use strict';
  const ES = (window.ES = window.ES || {});
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  ES.$ = $; ES.$$ = $$; ES.esc = esc;

  const A = (ES.A = { datos: null, estado: null, ses: null });
  const almacen = (() => {
    try { const s = window.localStorage; s.setItem('__es', '1'); s.removeItem('__es'); return s; } catch (e) {
      const d = {}; return { getItem: k => (k in d ? d[k] : null), setItem: (k, v) => { d[k] = String(v); } };
    }
  })();
  const perfil = (ES.perfil = () => (A.estado ? A.estado.perfiles[A.estado.activo] : null));
  const guardar = (ES.guardar = () => Motor.guardar(almacen, A.estado));
  const nombreNivel = n => Motor.NOMBRE_NIVEL[n] || n;
  const mundoActual = () => A.datos.mundoPorId[(perfil() && perfil().mundo) || 'bloques'];
  ES.mundoActual = mundoActual;
  const NOMBRE_ASIG = { matematica: 'Matemática', lenguaje: 'Lenguaje', ciencias: 'Ciencias Naturales', ingles: 'Inglés' };
  ES.NOMBRE_ASIG = NOMBRE_ASIG;
  // Asignaturas con contenido, en el orden del índice, y último curso que ya tiene contenido.
  const asignaturas = () => Object.keys(A.datos.indice.asignaturas).filter(a => A.datos.orden.some(id => A.datos.objetivos[id].asignatura === a));
  const ultimoNivel = () => A.datos.objetivos[A.datos.orden.reduce((m, id) => (Motor.idxNivel(A.datos.objetivos[id].nivel) > Motor.idxNivel(A.datos.objetivos[m].nivel) ? id : m))].nivel;
  const listaAsig = () => { const n = asignaturas().map(a => NOMBRE_ASIG[a] || a); return n.length > 1 ? `${n.slice(0, -1).join(', ')} y ${n[n.length - 1]}` : n.join(''); };
  const codigoCorto = oaId => { const o = A.datos.objetivos[oaId]; return `${o.objetivo_oficial.split(':')[0]} · ${nombreNivel(o.nivel)}`; };
  const resumenOA = oaId => A.datos.objetivos[oaId].objetivo_oficial.replace(/^OA \d+:\s*/, '');
  ES.codigoCorto = codigoCorto; ES.resumenOA = resumenOA;
  const pips = (n, total = 5) => `<span class="pips" role="img" aria-label="Dificultad ${n} de ${total}">${Array.from({ length: total }, (_, i) => `<i class="${i < n ? 'on' : ''}"></i>`).join('')}</span>`;
  ES.pips = pips;
  const monedasHTML = n => `<span class="monedas"><span class="moneda" aria-hidden="true"></span> ${n.toLocaleString('es-CL')}</span>`;
  ES.monedasHTML = monedasHTML;

  /* ---------- aviso y avatar ---------- */
  let avisoT = null;
  ES.aviso = (txt, ms = 2200) => { const a = $('#aviso'); a.textContent = txt; a.hidden = false; clearTimeout(avisoT); avisoT = setTimeout(() => { a.hidden = true; }, ms); };
  let tAnim = 0, celebrarHasta = 0;
  ES.celebrar = (seg = 1.6) => { celebrarHasta = tAnim + seg; };
  const DIBUJOS = { bloques: () => window.AvatarBloques, heroes: () => window.AvatarHeroes, plataformas: () => window.AvatarPlataformas };
  ES.estilo = pr => { pr.estilo = pr.estilo || { heroes: 0 }; return pr.estilo; };
  function dibujarAvatares() {
    const p = perfil();
    const op = { celebrar: tAnim < celebrarHasta };
    $$('canvas[data-avatar]').forEach(c => {
      const pr = c.dataset.avatar === 'activo' ? p : A.estado.perfiles[c.dataset.avatar];
      if (!pr) return;
      // data-vista permite mostrar el avatar de otro mundo (vista previa en «Elige tu mundo»)
      const mundo = c.dataset.vista || pr.mundo || 'bloques', dib = (DIBUJOS[mundo] || DIBUJOS.bloques)();
      const extra = { colores: ES.estilo(pr).heroes };
      const opc = c.dataset.avatar === 'activo' && !c.dataset.vista ? { ...op, ...extra } : { quieto: !c.dataset.vista, ...extra };
      dib.dibujar(c.getContext('2d'), c.width, c.height, (pr.avatares && pr.avatares[mundo]) || {}, tAnim, opc);
    });
  }
  function bucle(ts) { tAnim = ts / 1000; dibujarAvatares(); requestAnimationFrame(bucle); }

  ES.actualizarDock = (subir = false) => {
    const p = perfil(), dock = $('#dock');
    dock.hidden = !p; if (!p) return;
    $('#dock-canvas').dataset.avatar = 'activo';
    $('#dock-nombre').textContent = p.nombre;
    $('#dock-meta').textContent = `${nombreNivel(p.nivel_escolar)} · ${mundoActual().nombre}`;
    const m = $('#dock-monedas'); m.innerHTML = `<span class="moneda" aria-hidden="true"></span> ${p.monedas.toLocaleString('es-CL')}`;
    if (subir) { m.classList.remove('sube'); void m.offsetWidth; m.classList.add('sube'); }
    $('#dock-racha').textContent = p.racha.dias ? `Racha: ${p.racha.dias} día${p.racha.dias > 1 ? 's' : ''} seguidos` : 'Juega hoy para empezar una racha';
  };

  /* ---------- navegación ---------- */
  const PANTALLAS = {};
  ES.ir = (nombre, ...args) => {
    if (A.ses && nombre !== 'sesion') ES.detenerVoz && ES.detenerVoz();
    // un <main> nuevo por pantalla: así no se acumulan los listeners de pantallas anteriores
    const viejo = $('#principal'), main = viejo.cloneNode(false);
    viejo.replaceWith(main);
    PANTALLAS[nombre](main, ...args);
    ES.actualizarDock();
    window.scrollTo({ top: 0 });
    const h = main.querySelector('h1,h2'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
  };
  document.addEventListener('click', e => { const b = e.target.closest('[data-ir]'); if (b && perfil()) ES.ir(b.dataset.ir); });

  /* ---------- perfiles ---------- */
  PANTALLAS.perfiles = main => {
    const ids = A.estado.orden.filter(id => A.estado.perfiles[id]);
    if (!ids.length) return PANTALLAS.nuevo(main, true);
    A.estado.activo = null; guardar();
    main.innerHTML = `<section class="pantalla">
      <h1 class="titulo">¿Quién va de expedición?</h1>
      <p class="nota">Cada explorador guarda su curso, sus monedas y su avatar en este dispositivo.</p>
      <div class="perfiles">${ids.map(id => { const p = A.estado.perfiles[id]; return `
        <div class="bloque" data-pid="${esc(id)}">
          <button class="perfil" type="button" data-elegir="${esc(id)}" style="background:none;border:0;padding:0">
            <canvas width="128" height="112" data-avatar="${esc(id)}" aria-hidden="true"></canvas>
            <span><strong>${esc(p.nombre)}</strong>${esc(nombreNivel(p.nivel_escolar))}<br>${monedasHTML(p.monedas)}</span>
          </button>
          <div class="fila" style="margin-top:10px"><button class="btn chico piedra" type="button" data-borrar="${esc(id)}">Borrar</button></div>
        </div>`; }).join('')}</div>
      <div class="fila"><button class="btn" type="button" id="btn-nuevo">Nuevo explorador</button></div>
    </section>`;
    $('#btn-nuevo', main).addEventListener('click', () => ES.ir('nuevo'));
    main.addEventListener('click', e => {
      const el = e.target.closest('[data-elegir]');
      if (el) { A.estado.activo = el.dataset.elegir; guardar(); ES.ir('base'); return; }
      const bo = e.target.closest('[data-borrar]');
      if (bo) {
        const id = bo.dataset.borrar, p = A.estado.perfiles[id], caja = bo.parentElement;
        caja.innerHTML = `<span>¿Borrar a ${esc(p.nombre)} y todo su progreso?</span><button class="btn chico tierra" type="button" data-si="${esc(id)}">Sí, borrar</button><button class="btn chico piedra" type="button" data-no>Cancelar</button>`;
        return;
      }
      const si = e.target.closest('[data-si]');
      if (si) { delete A.estado.perfiles[si.dataset.si]; A.estado.orden = A.estado.orden.filter(x => x !== si.dataset.si); guardar(); ES.ir('perfiles'); return; }
      if (e.target.closest('[data-no]')) ES.ir('perfiles');
    });
  };

  PANTALLAS.nuevo = (main, primero) => {
    A.estado.activo = null;
    main.innerHTML = `<section class="pantalla bloque">
      <h1 class="titulo">${primero ? 'Bienvenido a Expedición Saber' : 'Nuevo explorador'}</h1>
      <p>Resuelve desafíos de ${esc(listaAsig())}, gana monedas y mejora tu avatar. Equivocarse nunca te quita monedas.</p>
      <form id="form-perfil" class="pantalla" style="gap:12px">
        <label class="campo" for="nombre">Nombre del explorador<input id="nombre" name="nombre" maxlength="20" autocomplete="off" required></label>
        <label class="campo" for="nivel">Curso<select id="nivel" name="nivel">${Motor.NIVELES_ESCOLARES.map(n => `<option value="${n}" ${n === '3_basico' ? 'selected' : ''}>${nombreNivel(n)}${Motor.idxNivel(n) > Motor.idxNivel(ultimoNivel()) ? ' (próximamente)' : ''}</option>`).join('')}</select></label>
        <p class="nota" id="nota-nivel"></p>
        <div class="fila"><button class="btn" type="submit">Crear y elegir mundo</button>${primero ? '' : '<button class="btn piedra" type="button" id="btn-volver">Volver</button>'}</div>
      </form></section>`;
    const nota = () => {
      const n = $('#nivel', main).value;
      $('#nota-nivel', main).textContent = Motor.idxNivel(n) > Motor.idxNivel(ultimoNivel())
        ? `Los desafíos de ${nombreNivel(n)} vienen pronto. Por ahora el contenido llega hasta ${nombreNivel(ultimoNivel())}: mientras tanto practicas con ese curso.` : '';
    };
    $('#nivel', main).addEventListener('change', nota); nota();
    const volver = $('#btn-volver', main); if (volver) volver.addEventListener('click', () => ES.ir('perfiles'));
    $('#form-perfil', main).addEventListener('submit', e => {
      e.preventDefault();
      const nombre = $('#nombre', main).value.trim(); if (!nombre) { $('#nombre', main).focus(); return; }
      const p = Motor.crearPerfil(nombre, $('#nivel', main).value, A.datos);
      A.estado.perfiles[p.id] = p; A.estado.orden.push(p.id); A.estado.activo = p.id; guardar();
      ES.ir('mundos');
    });
  };

  /* ---------- mundos ---------- */
  PANTALLAS.mundos = main => {
    const p = perfil(), ej = m => Motor.ambientar('Aquí los problemas hablan de {objetos}, de {el_contenedor} y de {la_construccion}.', m.tokens);
    main.innerHTML = `<section class="pantalla">
      <h1 class="titulo">Elige tu mundo</h1>
      <p class="nota">Tu avance en ${esc(listaAsig())} es el mismo en todos los mundos. Cada mundo tiene su propio avatar y sus propias mejoras.</p>
      <div class="mundos">${A.datos.mundos.map(m => `
        <article class="bloque mundo ${p.mundo === m.id ? 'activo' : ''}">
          <canvas class="vista-mundo" width="256" height="224" data-avatar="activo" data-vista="${esc(m.id)}" aria-hidden="true"></canvas>
          <h3>${esc(m.nombre)}</h3>
          <p>${esc(m.estilo)}</p>
          <p class="nota">Guía: ${esc(m.guia)}. ${esc(ej(m))}</p>
          <p class="nota">Mejoras: ${m.espacios.map(e => esc(e.nombre)).join(', ')}.</p>
          ${m.estado === 'jugable'
            ? `<button class="btn" type="button" data-mundo="${m.id}">${p.mundo === m.id ? 'Seguir aquí' : 'Elegir este mundo'}</button>`
            : '<span class="etiqueta">En construcción</span>'}
        </article>`).join('')}</div>
    </section>`;
    main.addEventListener('click', e => { const b = e.target.closest('[data-mundo]'); if (b) { perfil().mundo = b.dataset.mundo; guardar(); ES.ir('base'); } });
  };

  /* ---------- base ---------- */
  function estadoTexto(p, oaId) {
    const st = p.oas[oaId];
    if (st && st.dominado) return '<span class="etiqueta ok">Dominado</span>';
    if (st && st.respondidos) return `<span class="etiqueta lista">En curso</span> ${pips(st.nivel)}`;
    return '<span class="etiqueta lista">Nuevo</span>';
  }

  PANTALLAS.base = main => {
    const p = perfil(), m = mundoActual();
    const aviso = Motor.idxNivel(p.nivel_escolar) > Motor.idxNivel(ultimoNivel())
      ? `<p class="nota">Tu curso (${esc(nombreNivel(p.nivel_escolar))}) aún no tiene contenido. Mientras tanto practicas hasta ${esc(nombreNivel(ultimoNivel()))}.</p>` : '';
    const tarjeta = asig => {
      const alcance = A.datos.orden.some(id => A.datos.objetivos[id].asignatura === asig && Motor.idxNivel(A.datos.objetivos[id].nivel) <= Motor.idxNivel(p.nivel_escolar));
      if (!alcance) return `<article class="bloque asignatura"><h3>${NOMBRE_ASIG[asig]}</h3><p>Los desafíos de tu curso están en preparación. ¡Muy pronto!</p></article>`;
      const oaId = Motor.recomendar(p, asig, A.datos);
      if (!oaId) return `<article class="bloque asignatura"><h3>${NOMBRE_ASIG[asig]}</h3><p>Dominaste todo lo disponible en tu curso. ¡Excelente!</p>
        <button class="btn piedra" type="button" data-arbol="${asig}">Ver el árbol</button></article>`;
      return `<article class="bloque asignatura"><h3>${NOMBRE_ASIG[asig]}</h3>
        <p class="oa"><strong>${esc(codigoCorto(oaId))}</strong><br>${esc(resumenOA(oaId))}</p>
        <p>${estadoTexto(p, oaId)}</p>
        <div class="fila"><button class="btn" type="button" data-jugar="${asig}">Jugar 10 desafíos</button><button class="btn piedra" type="button" data-arbol="${asig}">Ver el árbol</button></div>
      </article>`;
    };
    const barata = m.espacios.map(e => ({ e, info: Motor.infoMejora(p, m.id, e.id, A.datos) })).filter(x => x.info.siguiente).sort((a, b) => a.info.costo - b.info.costo)[0];
    main.innerHTML = `<section class="pantalla">
      <h1 class="titulo">Hola, ${esc(p.nombre)}</h1>${aviso}
      <div class="asignaturas">${asignaturas().map(tarjeta).join('')}</div>
      <article class="bloque"><h3 class="subtitulo">Taller de ${esc(m.nombre)}</h3>
        <p>${barata ? `Próxima mejora: <strong>${esc(barata.e.niveles[barata.info.siguiente - 1])}</strong> por ${monedasHTML(barata.info.costo)}.` : 'Tu avatar está completo en este mundo.'}</p>
        <div class="fila"><button class="btn tierra" type="button" data-ir="taller">Ir al Taller</button><button class="btn piedra" type="button" data-ir="mundos">Cambiar mundo</button><button class="btn piedra" type="button" data-ir="perfiles">Cambiar explorador</button></div>
      </article>
    </section>`;
    main.addEventListener('click', e => {
      const j = e.target.closest('[data-jugar]'); if (j) return ES.iniciarSesion(j.dataset.jugar);
      const a = e.target.closest('[data-arbol]'); if (a) ES.ir('arbol', a.dataset.arbol);
    });
  };

  /* ---------- árbol de objetivos ---------- */
  PANTALLAS.arbol = (main, asig) => {
    const p = perfil(), D = A.datos;
    const ids = D.orden.filter(id => D.objetivos[id].asignatura === asig);
    const niveles = [...new Set(ids.map(id => D.objetivos[id].nivel))];
    const nodo = id => {
      const o = D.objetivos[id], st = p.oas[id], disp = Motor.disponibilidad(p, id, D);
      let estado, boton = '';
      if (st && st.dominado) estado = '<span class="etiqueta ok">Dominado</span>';
      else if (disp.ok) estado = st && st.respondidos ? `<span class="etiqueta lista">En curso</span> ${pips(st.nivel)}` : '<span class="etiqueta lista">Disponible</span>';
      else if (disp.motivo === 'superior') estado = '<span class="etiqueta bloqueado">De un curso más arriba</span>';
      else estado = `<span class="etiqueta bloqueado">Antes: ${disp.faltan.map(f => esc(codigoCorto(f))).join(', ')}</span>`;
      if (disp.ok) boton = `<button class="btn chico" type="button" data-practicar="${esc(id)}">${st && st.dominado ? 'Repasar' : 'Practicar'}</button>`;
      const pend = o.verificacion.codigo !== 'verificado' ? ' <span class="etiqueta pendiente" title="Código pendiente de verificación en curriculumnacional.cl">Código por verificar</span>' : '';
      return `<article class="bloque nodo"><div><span class="codigo">${esc(codigoCorto(id))}</span>${pend}<p>${esc(resumenOA(id))}</p><p>${estado}</p></div>${boton}</article>`;
    };
    main.innerHTML = `<section class="pantalla">
      <div class="fila"><button class="btn chico piedra" type="button" data-ir="base">← Base</button><h1 class="titulo">Árbol de ${NOMBRE_ASIG[asig]}</h1></div>
      <p class="nota">Cada objetivo se abre cuando sus prerequisitos están dominados o van en dificultad 3. Los cursos anteriores al tuyo se dan por aprendidos y quedan para repasar.</p>
      <div class="arbol">${niveles.map(n => `<h2 class="nivel-grupo">${esc(nombreNivel(n))}</h2>${ids.filter(id => D.objetivos[id].nivel === n).map(nodo).join('')}`).join('')}</div>
    </section>`;
    main.addEventListener('click', e => { const b = e.target.closest('[data-practicar]'); if (b) ES.iniciarSesion(asig, b.dataset.practicar); });
  };

  /* ---------- taller ---------- */
  PANTALLAS.taller = main => {
    const p = perfil(), m = mundoActual(), tramos = Motor.tramosDominados(p, A.datos).length;
    const fila = e => {
      const info = Motor.infoMejora(p, m.id, e.id, A.datos), actual = info.nivelActual;
      const razon = info.motivo === 'tramos' ? `Necesitas dominar ${info.tramosNecesarios} tramo${info.tramosNecesarios > 1 ? 's' : ''} completo${info.tramosNecesarios > 1 ? 's' : ''} (llevas ${info.tramos}).`
        : info.motivo === 'monedas' ? `Te faltan ${(info.costo - p.monedas).toLocaleString('es-CL')} monedas.` : '';
      return `<article class="bloque espacio"><div><h3>${esc(e.nombre)}: ${actual ? esc(e.niveles[actual - 1]) : 'sin mejora'}</h3>
        <p>${pips(actual)} Nivel ${actual} de 5</p>
        ${info.siguiente ? `<p>Siguiente: <strong>${esc(e.niveles[info.siguiente - 1])}</strong> · ${monedasHTML(info.costo)}</p>${razon ? `<p class="nota">${razon}</p>` : ''}` : '<p class="nota">¡Mejora máxima!</p>'}</div>
        ${info.siguiente ? `<button class="btn ${info.puede ? '' : 'piedra'}" type="button" data-mejorar="${e.id}" ${info.puede ? '' : 'disabled'}>Mejorar</button>` : ''}</article>`;
    };
    main.innerHTML = `<section class="pantalla">
      <div class="fila"><button class="btn chico piedra" type="button" data-ir="base">← Base</button><h1 class="titulo">Taller de ${esc(m.nombre)}</h1></div>
      <div class="bloque taller-escena"><canvas width="512" height="448" data-avatar="activo" aria-label="Tu avatar con sus mejoras"></canvas>
        <p class="nota">Tienes ${monedasHTML(p.monedas)} y ${tramos} tramo${tramos === 1 ? '' : 's'} dominado${tramos === 1 ? '' : 's'}. Las mejoras finales (nivel 5) piden dominar un tramo completo de contenido por cada una.</p></div>
      ${m.id === 'heroes' && window.AvatarHeroes ? `<article class="bloque"><h3>Colores del traje</h3><p class="nota">Elige los colores de tu héroe. Cambiarlos es gratis.</p>
        <div class="colores" role="group" aria-label="Colores del traje">${AvatarHeroes.COLORES.map((c, i) => `<button class="color ${ES.estilo(p).heroes === i ? 'sel' : ''}" type="button" data-color="${i}" aria-pressed="${ES.estilo(p).heroes === i}" title="${esc(c.nombre)}"><span style="background:${c.p}"></span><span style="background:${c.s}"></span><b>${esc(c.nombre)}</b></button>`).join('')}</div></article>` : ''}
      <div class="espacios">${m.espacios.map(fila).join('')}</div>
    </section>`;
    main.addEventListener('click', e => {
      const col = e.target.closest('[data-color]');
      if (col) { ES.estilo(p).heroes = Number(col.dataset.color); guardar(); ES.celebrar(1); ES.ir('taller'); return; }
      const b = e.target.closest('[data-mejorar]'); if (!b) return;
      const r = Motor.comprarMejora(p, m.id, b.dataset.mejorar, A.datos);
      if (!r.ok) return;
      guardar(); ES.sonido && ES.sonido('mejora'); ES.celebrar(2);
      const esp = m.espacios.find(x => x.id === b.dataset.mejorar);
      ES.aviso(`¡Nuevo: ${esp.niveles[r.info.siguiente - 1]}!`);
      ES.ir('taller');
    });
  };

  /* ---------- resumen de sesión ---------- */
  PANTALLAS.fin = (main, r) => {
    const p = perfil();
    main.innerHTML = `<section class="pantalla">
      <article class="bloque resumen"><h1 class="titulo">¡Sesión completa!</h1>
        <p>Resolviste ${r.aciertos} de ${r.total} desafíos al primer intento.</p>
        <dl>
          <dt>Monedas por desafíos</dt><dd>${r.monedasDesafios}</dd>
          ${r.dominios ? `<dt>Objetivos dominados (+100 c/u)</dt><dd>${r.dominios * 100}</dd>` : ''}
          <dt>Bono por completar la sesión</dt><dd>${r.bonoSesion}</dd>
          <dt>Bono de racha (${p.racha.dias} día${p.racha.dias > 1 ? 's' : ''})</dt><dd>${r.bonoRacha || '—'}</dd>
          <dt><strong>Total</strong></dt><dd>${r.total_monedas}</dd>
        </dl>
        ${r.repaso.length ? `<p class="retro pista">Te recomendamos repasar: ${r.repaso.map(id => esc(codigoCorto(id))).join(', ')}.</p>` : ''}
        <div class="fila"><button class="btn tierra" type="button" data-ir="taller">Ir al Taller</button>
          <button class="btn" type="button" id="btn-otra">Otra sesión</button>
          <button class="btn piedra" type="button" data-ir="base">Base</button></div>
      </article></section>`;
    $('#btn-otra', main).addEventListener('click', () => ES.iniciarSesion(r.asig));
  };

  /* ---------- arranque ---------- */
  ES.registrarPantalla = (nombre, fn) => { PANTALLAS[nombre] = fn; };
  async function iniciar() {
    $('#principal').innerHTML = '<p class="bloque">Cargando el valle…</p>';
    try { A.datos = await cargar(); } catch (e) {
      $('#principal').innerHTML = `<p class="bloque">No se pudo cargar el contenido (${esc(e.message)}). Abre el juego desde un servidor web, por ejemplo con <code>python3 -m http.server</code>.</p>`;
      return;
    }
    A.estado = Motor.cargar(almacen);
    requestAnimationFrame(bucle);
    ES.ir(A.estado.activo && A.estado.perfiles[A.estado.activo] ? 'base' : 'perfiles');
  }
  async function cargar() {
    const get = p => fetch(p).then(r => { if (!r.ok) throw new Error(p); return r.json(); });
    const [indice, mundos] = await Promise.all([get('contenido/indice.json'), get('mundos/mundos.json')]);
    const bancos = (await Promise.all(indice.archivos.map(a => get('contenido/' + a.archivo)))).flat();
    return Motor.prepararDatos(bancos, mundos, indice);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
