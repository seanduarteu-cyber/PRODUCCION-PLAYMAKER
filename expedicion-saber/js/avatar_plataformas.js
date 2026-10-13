/* Avatar del Mundo de plataformas (Isla Brinco): escena colorida dibujada en una grilla lógica de 64 × 56.
   equipo = { skin, sombrero, mascota, gesto, objeto } con niveles 0-5. */
(function (raiz) {
  'use strict';
  const W = 64, H = 56, SUELO = 44;
  const TINTA = '#2b2118', BLANCO = '#ffffff', ORO = '#ffd23f';
  const ARCOIRIS = ['#ff595e', '#ff924c', '#ffca3a', '#8ac926', '#1982c4', '#6a4c93'];
  // ancho de cada fila del cuerpo redondo (16 filas)
  const FORMA = [6, 8, 10, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 10, 8, 6];

  function dibujar(ctx, ancho, alto, equipo, t = 0, op = {}) {
    const e = Object.assign({ skin: 0, sombrero: 0, mascota: 0, gesto: 0, objeto: 0 }, equipo || {});
    const esc = Math.max(1, Math.floor(Math.min(ancho / W, alto / H)));
    const ox = Math.floor((ancho - W * esc) / 2), oy = Math.floor((alto - H * esc) / 2);
    ctx.imageSmoothingEnabled = false;
    ctx.clearRect(0, 0, ancho, alto);
    const px = (x, y, w, h, c) => { ctx.fillStyle = c; ctx.fillRect(ox + Math.round(x) * esc, oy + Math.round(y) * esc, Math.round(w) * esc, Math.round(h) * esc); };
    const tt = op.quieto ? 0 : t;
    isla(px, tt);
    mascota(px, e.mascota, tt);
    personaje(px, e, tt, op.celebrar);
  }

  /* ---------- fondo: cielo, cerros, plataformas flotantes y monedas ---------- */
  function isla(px, t) {
    px(0, 0, W, SUELO, '#7fd3ff'); px(0, 30, W, SUELO - 30, '#a8e3ff');
    const nube = (x, y) => { px(x, y, 10, 3, BLANCO); px(x + 2, y - 2, 6, 2, BLANCO); px(x + 1, y + 3, 8, 1, '#d8f1ff'); };
    nube(((t * 1.5) % 84) - 14, 5); nube(((t * 1 + 44) % 84) - 14, 13);
    // cerros redondos
    for (const [cx, r, c] of [[8, 10, '#5cc46b'], [30, 13, '#4bb35c'], [56, 9, '#5cc46b']]) {
      for (let y = 0; y < r; y++) { const w = Math.round(Math.sqrt(r * r - (r - y) * (r - y)) * 2); px(cx - w / 2, SUELO - r + y, w, 1, c); }
    }
    // plataformas flotantes con monedas que giran
    for (const [x, y, w] of [[38, 18, 12], [50, 27, 10]]) {
      px(x, y, w, 2, '#6fd36b'); px(x, y, w, 1, '#a5ef8f'); px(x, y + 2, w, 3, '#b8743c'); px(x + 1, y + 5, w - 2, 1, '#8e5428');
      const giro = Math.floor(t * 4 + x) % 4, mw = [3, 2, 1, 2][giro];
      px(x + w / 2 - mw / 2, y - 5 + Math.round(Math.sin(t * 3 + x) * 1), mw, 3, ORO);
    }
    // suelo de pasto con flores
    px(0, SUELO, W, 3, '#6fd36b'); px(0, SUELO, W, 1, '#a5ef8f');
    px(0, SUELO + 3, W, H - SUELO - 3, '#c98a4b');
    for (let i = 0; i < 20; i++) px((i * 29) % W, SUELO + 5 + ((i * 11) % (H - SUELO - 6)), 2, 1, '#a86b35');
    for (const [x, c] of [[4, '#ff595e'], [27, '#ffca3a'], [47, '#ff8fd0'], [60, BLANCO]]) { px(x, SUELO - 2, 1, 2, '#3f9b4a'); px(x - 1, SUELO - 3, 3, 1, c); }
  }

  /* ---------- mascotas ---------- */
  function mascota(px, n, t) {
    if (!n) return;
    const salto = Math.round(Math.abs(Math.sin(t * 3)) * 2);
    if (n === 1) { // pollito
      const x = 30, y = SUELO - 5 - salto;
      px(x, y, 5, 5, '#ffe14d'); px(x + 1, y - 1, 3, 1, '#ffe14d'); px(x + 3, y + 1, 1, 1, TINTA); px(x + 5, y + 2, 1, 1, '#ff924c');
      px(x + 1, y + 5, 1, 1, '#ff924c'); px(x + 3, y + 5, 1, 1, '#ff924c');
      return;
    }
    if (n === 2) { // gato saltarín
      const s = Math.floor(t * 0.8) % 3 === 0 ? Math.round(Math.abs(Math.sin(t * 5)) * 5) : 0, x = 29, y = SUELO - 6 - s;
      px(x, y + 1, 8, 4, '#8f96a3'); px(x + 6, y - 2, 4, 4, '#8f96a3'); px(x + 6, y - 3, 1, 1, '#8f96a3'); px(x + 9, y - 3, 1, 1, '#8f96a3');
      px(x + 7, y - 1, 1, 1, TINTA); px(x + 9, y - 1, 1, 1, TINTA); px(x - 2, y - 1 + Math.round(Math.sin(t * 4)), 2, 1, '#8f96a3'); px(x - 1, y, 1, 2, '#8f96a3');
      px(x, y + 5, 1, 1, '#6b717c'); px(x + 6, y + 5, 1, 1, '#6b717c');
      return;
    }
    if (n === 3) { // zorrito
      const x = 29, y = SUELO - 6 - salto;
      px(x, y + 1, 8, 4, '#f07f1e'); px(x + 6, y - 2, 4, 4, '#f07f1e'); px(x + 6, y - 3, 1, 1, '#f07f1e'); px(x + 9, y - 3, 1, 1, '#f07f1e');
      px(x + 8, y, 2, 1, BLANCO); px(x + 9, y - 1, 1, 1, TINTA); px(x - 3, y, 3, 3, '#f07f1e'); px(x - 4, y + 1, 1, 2, BLANCO);
      px(x + 1, y + 5, 1, 1, TINTA); px(x + 6, y + 5, 1, 1, TINTA);
      return;
    }
    if (n === 4) { // dragoncito con bocanada
      const x = 28, y = SUELO - 9 - salto, ala = Math.floor(t * 6) % 2;
      px(x, y + 2, 9, 5, '#3fb56b'); px(x + 7, y - 1, 5, 4, '#3fb56b'); px(x + 10, y, 1, 1, TINTA); px(x - 2, y + 4, 2, 2, '#3fb56b');
      px(x + 2, y - ala, 4, 2, '#7be09c'); px(x + 1, y + 7, 2, 2, '#2c8a50'); px(x + 6, y + 7, 2, 2, '#2c8a50');
      for (let i = 0; i < 3; i++) px(x + 1 + i * 3, y + 1, 1, 1, '#ffca3a');
      if (Math.floor(t * 1.2) % 3 === 0) { px(x + 12, y + 1, 2, 1, '#ff924c'); px(x + 14, y, 2, 2, '#ffca3a'); }
      return;
    }
    // 5: ballena voladora en el cielo
    const x = ((t * 3 + 50) % 90) - 20, y = 20 + Math.round(Math.sin(t * 1.5) * 2);
    px(x, y, 16, 6, '#5aa9e6'); px(x + 2, y - 1, 11, 1, '#5aa9e6'); px(x + 1, y + 6, 13, 1, '#d9f0ff'); px(x + 2, y + 4, 12, 2, '#d9f0ff');
    px(x - 3, y + 1, 3, 2, '#5aa9e6'); px(x - 4, y - 1, 2, 2, '#5aa9e6'); px(x - 4, y + 3, 2, 2, '#5aa9e6');
    px(x + 13, y + 2, 1, 1, TINTA);
    if (Math.floor(t * 2) % 2) { px(x + 10, y - 4, 1, 3, '#bfe6ff'); px(x + 9, y - 5, 1, 1, '#bfe6ff'); px(x + 11, y - 5, 1, 1, '#bfe6ff'); }
  }

  /* ---------- personaje redondo ---------- */
  function colorFila(n, r, x, t) {
    if (n === 1) return Math.floor(r / 2) % 2 ? '#ffd0a8' : '#ff7a59';
    if (n === 3) return ARCOIRIS[Math.floor(r / 3) % 6];
    if (n === 4) return '#2b1d5c';
    if (n === 5) return (Math.floor(t * 6) + x + r) % 9 === 0 ? '#fff7c8' : r < 3 ? '#ffe37a' : ORO;
    if (n === 2) return '#5bc0eb';
    return '#ff8a3d';
  }

  function personaje(px, e, t, celebrar) {
    const g = e.gesto;
    // altura: patineta, cohete y alas levantan; gestos de salto
    let alza = e.objeto === 3 ? 3 : e.objeto === 4 ? 6 + Math.round(Math.sin(t * 3)) : e.objeto === 5 ? 4 + Math.round(Math.sin(t * 2)) : 0;
    const ciclo = t % 2.4;
    let salto = 0, alReves = false, dx = 0, mirada = 0;
    if (celebrar || g === 2) salto = celebrar ? Math.round(Math.abs(Math.sin(t * 7)) * 5) : ciclo < 0.6 ? Math.round(Math.sin((ciclo / 0.6) * Math.PI) * 6) : 0;
    if (g === 3 && ciclo < 0.8) mirada = [0, 1, 2, -1][Math.floor(ciclo / 0.2)]; // giro: de frente, de lado, de espalda, del otro lado
    if (g === 4 && ciclo < 0.8 && !celebrar) { salto = Math.round(Math.sin((ciclo / 0.8) * Math.PI) * 9); alReves = ciclo > 0.25 && ciclo < 0.55; }
    if (g === 5) dx = Math.round(Math.sin(t * 4) * 2);
    if (!salto && !alza && g !== 4) salto = Math.round(Math.sin(t * 2.2) * 0.6 + 0.4);
    const base = SUELO - alza - salto, cx = 16 + dx;
    // al revés: se dibuja reflejado en vertical alrededor del centro del cuerpo
    const cy = base - 9;
    const P = alReves ? (x, y, w, h, c) => px(x, 2 * cy - y - h, w, h, c) : px;

    if (e.objeto === 5) alas(P, cx, base, t);
    if (e.objeto === 4) mochila(P, cx, base, t);
    if (e.objeto === 3) patineta(px, cx, SUELO - 3 - salto + (salto ? 0 : 0), t);
    // pies
    P(cx - 5, base - 2, 4, 2, TINTA); P(cx + 1, base - 2, 4, 2, TINTA);
    // cuerpo por filas
    const top = base - 18;
    FORMA.forEach((w, r) => {
      for (let i = 0; i < w; i++) {
        const x = cx - w / 2 + i;
        let c = colorFila(e.skin, r, i, t);
        if (e.skin === 2 && ((r * 3 + i * 5) % 11 === 0)) c = BLANCO; // lunares
        if (e.skin === 4 && ((r * 7 + i * 3 + Math.floor(t * 2)) % 13 === 0)) c = (r + i) % 2 ? BLANCO : '#ffd23f'; // galaxia
        P(x, top + r, 1, 1, c);
      }
    });
    // cara (según la mirada del giro)
    if (mirada !== 2) {
      const ojoX = cx - 4 + mirada * 2;
      P(ojoX, top + 4, 3, 4, BLANCO); P(ojoX + 5, top + 4, 3, 4, BLANCO);
      P(ojoX + 1 + (mirada > 0 ? 1 : 0), top + 5, 2, 2, TINTA); P(ojoX + 6 + (mirada > 0 ? 1 : 0), top + 5, 2, 2, TINTA);
      P(cx - 2 + mirada, top + 10, 4, 1, '#8a2d1f'); P(cx - 3 + mirada, top + 9, 1, 1, '#8a2d1f'); P(cx + 2 + mirada, top + 9, 1, 1, '#8a2d1f');
      P(cx - 6 + mirada, top + 8, 2, 1, '#ff9fb1'); P(cx + 4 + mirada, top + 8, 2, 1, '#ff9fb1');
    }
    // brazos: el saludo levanta la mano derecha
    const brazo = colorFila(e.skin, 9, 0, t);
    P(cx - 8, top + 8, 2, 3, brazo);
    if (g === 1 || celebrar) { const ola = Math.floor(t * 6) % 2; P(cx + 6, top + 3 - ola, 2, 4, brazo); P(cx + 6 + ola, top + 1 - ola, 2, 2, brazo); }
    else P(cx + 6, top + 8, 2, 3, brazo);
    if (e.objeto === 1) globo(P, cx + 7, top + 8, t);
    if (e.objeto === 2) yoyo(P, cx + 7, top + 11, t);
    sombrero(P, e.sombrero, cx, top, t);
    if (g === 5) for (let i = 0; i < 5; i++) if ((Math.floor(t * 4) + i) % 2) px(cx - 12 + i * 6, top - 4 + ((i * 7) % 12), 1, 1, i % 2 ? ORO : BLANCO);
  }

  function sombrero(P, n, cx, top, t) {
    if (!n) return;
    if (n === 1) { P(cx - 4, top - 2, 8, 3, '#e63946'); P(cx - 4, top, 8, 1, BLANCO); P(cx - 1, top - 4, 2, 2, BLANCO); return; } // gorrito
    if (n === 2) { P(cx - 5, top - 1, 10, 2, '#264653'); P(cx - 3, top - 2, 6, 1, '#264653'); P(cx, top - 3, 1, 1, '#264653'); return; } // boina
    if (n === 3) { P(cx - 6, top, 12, 1, TINTA); P(cx - 4, top - 7, 8, 7, TINTA); P(cx - 4, top - 2, 8, 1, '#e63946'); return; } // sombrero de copa
    if (n === 4) { // casco espacial transparente
      for (let r = 0; r < 10; r++) { const w = [8, 12, 14, 14, 14, 14, 14, 14, 14, 14][r]; P(cx - w / 2, top - 2 + r, w, 1, 'rgba(200,240,255,0.35)'); }
      P(cx - 7, top + 8, 14, 1, '#c9ced6'); P(cx + 3, top - 1, 2, 1, BLANCO);
      return;
    }
    // 5: corona de luz con halo que late
    const halo = Math.floor(t * 3) % 2 ? 'rgba(255,240,160,0.6)' : 'rgba(255,240,160,0.25)';
    P(cx - 6, top - 6, 12, 1, halo);
    P(cx - 4, top - 2, 8, 2, ORO); P(cx - 4, top - 4, 2, 2, ORO); P(cx - 1, top - 5, 2, 3, ORO); P(cx + 2, top - 4, 2, 2, ORO);
    P(cx - 3, top - 1, 1, 1, '#ff595e'); P(cx, top - 1, 1, 1, '#1982c4'); P(cx + 2, top - 1, 1, 1, '#8ac926');
  }

  function globo(P, x, y, t) {
    const v = Math.round(Math.sin(t * 2));
    for (let i = 0; i < 10; i++) P(x + Math.round(i * 0.3) + (i > 6 ? v : 0), y - i, 1, 1, '#5b5b5b');
    const gx = x + 1 + v, gy = y - 17;
    P(gx, gy + 1, 6, 5, '#ff595e'); P(gx + 1, gy, 4, 1, '#ff595e'); P(gx + 1, gy + 6, 4, 1, '#ff595e'); P(gx + 1, gy + 1, 1, 2, '#ffb3b5'); P(gx + 2, gy + 7, 2, 1, '#c9302c');
  }

  function yoyo(P, x, y, t) {
    const largo = Math.round((Math.sin(t * 4) + 1) * 4);
    P(x, y, 1, largo, '#5b5b5b'); P(x - 1, y + largo, 3, 3, '#1982c4'); P(x, y + largo + 1, 1, 1, ORO);
  }

  function patineta(px, cx, y, t) {
    px(cx - 8, y, 16, 1, '#e76f51'); px(cx - 9, y - 1, 1, 1, '#e76f51'); px(cx + 8, y - 1, 1, 1, '#e76f51');
    const r = Math.floor(t * 8) % 2 ? '#6b717c' : TINTA;
    px(cx - 6, y + 1, 2, 2, r); px(cx + 4, y + 1, 2, 2, r);
  }

  function mochila(P, cx, base, t) {
    P(cx - 9, base - 15, 3, 9, '#9aa0a8'); P(cx + 6, base - 15, 3, 9, '#9aa0a8'); P(cx - 9, base - 15, 3, 1, '#c9ced6'); P(cx + 6, base - 15, 3, 1, '#c9ced6');
    const f = Math.floor(t * 10) % 2;
    for (const x of [cx - 9, cx + 6]) { P(x, base - 6, 3, 2 + f, '#ff924c'); P(x + 1, base - 4 + f, 1, 2, '#ffca3a'); }
  }

  function alas(P, cx, base, t) {
    const a = Math.floor(t * 4) % 2, c = 'rgba(255,247,200,0.75)', borde = 'rgba(255,210,63,0.9)';
    for (let r = 0; r < 8; r++) {
      const w = 8 - r + (a ? 1 : 0);
      P(cx - 7 - w, base - 18 + r - a, w, 1, r === 0 ? borde : c);
      P(cx + 7, base - 18 + r - a, w, 1, r === 0 ? borde : c);
    }
  }

  raiz.AvatarPlataformas = { dibujar, ANCHO: W, ALTO: H };
})(typeof window !== 'undefined' ? window : globalThis);
