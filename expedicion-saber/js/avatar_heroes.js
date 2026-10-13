/* Avatar del Mundo de héroes (Ciudad Voltia): escena de cómic dibujada en una grilla lógica de 64 × 56.
   equipo = { mascara, traje, capa, poder, vehiculo } con niveles 0-5. op.colores = índice de COLORES del traje. */
(function (raiz) {
  'use strict';
  const W = 64, H = 56, SUELO = 44;
  // Colores del traje que elige el jugador (gratis, en el Taller). [principal, secundario]
  const COLORES = [
    { nombre: 'Rojo y azul', p: '#d23a32', s: '#2c58c4' },
    { nombre: 'Negro y dorado', p: '#30303a', s: '#e8b72c' },
    { nombre: 'Verde y negro', p: '#2f9e4f', s: '#24242c' },
    { nombre: 'Morado y turquesa', p: '#7a3fc4', s: '#1fb5c4' },
    { nombre: 'Azul y blanco', p: '#2563c9', s: '#eef1f6' },
    { nombre: 'Naranjo y gris', p: '#ef7d1d', s: '#5d6470' },
  ];
  const PIEL = '#f1c27d', PIEL_SOMBRA = '#d9a35f', PELO = '#3b2a1e', TINTA = '#1f1a24';
  const LUZ = '#7df9ff', ORO = '#ffd23f', BLANCO = '#ffffff';

  // aclara (f > 0) u oscurece (f < 0) un color #rrggbb
  function tono(hex, f) {
    const n = parseInt(hex.slice(1), 16), c = [n >> 16, (n >> 8) & 255, n & 255];
    const r = c.map(v => Math.round(f >= 0 ? v + (255 - v) * f : v * (1 + f)));
    return '#' + r.map(v => v.toString(16).padStart(2, '0')).join('');
  }

  function dibujar(ctx, ancho, alto, equipo, t = 0, op = {}) {
    const e = Object.assign({ mascara: 0, traje: 0, capa: 0, poder: 0, vehiculo: 0 }, equipo || {});
    const col = COLORES[op.colores | 0] || COLORES[0];
    const esc = Math.max(1, Math.floor(Math.min(ancho / W, alto / H)));
    const ox = Math.floor((ancho - W * esc) / 2), oy = Math.floor((alto - H * esc) / 2);
    ctx.imageSmoothingEnabled = false;
    ctx.clearRect(0, 0, ancho, alto);
    const px = (x, y, w, h, c) => { ctx.fillStyle = c; ctx.fillRect(ox + Math.round(x) * esc, oy + Math.round(y) * esc, Math.round(w) * esc, Math.round(h) * esc); };
    const tt = op.quieto ? 0 : t;

    ciudad(px, tt);
    if (e.poder === 5) tormenta(px, tt);
    vehiculo(px, e.vehiculo, tt, col);
    heroe(px, e, tt, op.celebrar, col);
  }

  /* ---------- fondo: atardecer, edificios con ventanas y calle ---------- */
  function ciudad(px, t) {
    const bandas = ['#2b2d5c', '#3b3470', '#5a3f82', '#8a4f86', '#c8667a', '#f28c5b'];
    bandas.forEach((c, i) => px(0, i * 5, W, 5, c));
    px(0, 30, W, SUELO - 30, '#f6a96b');
    px(52, 4, 4, 4, '#fff3c4'); px(53, 3, 2, 6, '#fff3c4'); px(51, 5, 6, 2, '#fff3c4'); // luna
    for (let i = 0; i < 7; i++) if ((Math.floor(t * 1.5) + i) % 3) px((i * 23 + 5) % 50, (i * 7) % 12 + 1, 1, 1, BLANCO);
    // edificios lejanos y cercanos (posiciones fijas)
    const lejos = [[0, 22, 8], [7, 18, 7], [13, 24, 9], [21, 14, 6], [26, 20, 9], [34, 16, 7], [40, 23, 8], [47, 12, 7], [53, 19, 11]];
    lejos.forEach(([x, y, w]) => px(x, y, w, SUELO - y, '#4a3f6e'));
    const cerca = [[2, 28, 10], [15, 31, 8], [29, 26, 10], [44, 30, 9], [55, 27, 9]];
    cerca.forEach(([x, y, w], k) => {
      px(x, y, w, SUELO - y, '#2e2846'); px(x, y, w, 1, '#57507a');
      for (let wy = y + 2; wy < SUELO - 2; wy += 3) for (let wx = x + 1; wx < x + w - 1; wx += 3) {
        if ((wx * 7 + wy * 3 + k) % 5 > 1) px(wx, wy, 1, 1, (wx + wy + k) % 4 ? '#ffd56b' : '#ffeaa8');
      }
    });
    // vereda y calle
    px(0, SUELO, W, 2, '#b8bcc6'); px(0, SUELO, W, 1, '#d7dae1'); px(0, SUELO + 2, W, 1, '#7c8190');
    px(0, SUELO + 3, W, H - SUELO - 3, '#3d4250');
    for (let x = 2; x < W; x += 8) px(x, SUELO + 7, 4, 1, ORO);
  }

  function tormenta(px, t) {
    for (const [x, y, w] of [[2, 3, 14], [5, 1, 9], [12, 4, 12], [8, 6, 14]]) px(x, y, w, 3, '#5b5f73');
    px(4, 8, 22, 1, '#45485a');
    if (Math.floor(t * 3) % 3 === 0) { // relámpago que cae junto al héroe
      const rx = 26; let y = 9, x = rx;
      for (let i = 0; i < 6; i++) { px(x, y, 2, 3, i % 2 ? ORO : '#fff7c8'); y += 3; x += i % 2 ? 2 : -2; }
    }
  }

  /* ---------- vehículos a la derecha ---------- */
  function vehiculo(px, n, t, col) {
    if (!n) return;
    if (n === 1) { // patines sobre la vereda
      for (const x of [42, 51]) { px(x, SUELO - 5, 6, 4, col.s); px(x, SUELO - 5, 6, 1, tono(col.s, 0.4)); px(x + 4, SUELO - 8, 2, 3, col.s); px(x, SUELO - 1, 2, 2, ORO); px(x + 4, SUELO - 1, 2, 2, ORO); }
      return;
    }
    if (n === 2) { // moto
      const x = 40, y = SUELO - 1;
      for (const rx of [x, x + 13]) { px(rx, y - 4, 5, 5, TINTA); px(rx + 1, y - 3, 3, 3, '#8a90a0'); px(rx + 2, y - 2, 1, 1, TINTA); }
      px(x + 3, y - 7, 13, 3, col.p); px(x + 3, y - 7, 13, 1, tono(col.p, 0.35)); px(x + 6, y - 9, 6, 2, TINTA);
      px(x + 15, y - 10, 2, 4, '#8a90a0'); px(x + 17, y - 10, 2, 1, '#8a90a0'); px(x + 17, y - 7, 2, 2, Math.floor(t * 4) % 2 ? '#fff3c4' : ORO);
      return;
    }
    const vuelo = Math.round(Math.sin(t * 1.6) * 1.5);
    if (n === 3) { // planeador
      const x = 40, y = 12 + vuelo;
      for (let i = 0; i < 9; i++) px(x + 9 - i, y + i, 2 + i * 2, 1, i % 3 ? col.s : tono(col.s, -0.25));
      px(x + 10, y + 9, 1, 5, TINTA); px(x + 5, y + 14, 11, 1, TINTA);
      return;
    }
    if (n === 4) { // jet con estela
      const x = 38, y = 14 + vuelo;
      px(x + 4, y, 18, 4, '#c9ced6'); px(x + 4, y, 18, 1, BLANCO); px(x + 22, y + 1, 2, 2, '#c9ced6');
      px(x + 16, y + 1, 4, 2, LUZ); px(x + 8, y - 4, 5, 4, col.p); px(x + 8, y + 4, 5, 3, col.p); px(x + 4, y - 2, 2, 2, col.p);
      const f = Math.floor(t * 8) % 2;
      px(x + 1 - f, y + 1, 3 + f, 2, '#ff9c3a'); px(x - 3 - f, y + 1, 4, 2, '#ffd56b');
      return;
    }
    // 5: nave relámpago flotando sobre la calle
    const x = 38, y = 20 + vuelo, luz = Math.floor(t * 4) % 2;
    px(x + 2, y + 4, 22, 5, tono(col.p, -0.2)); px(x, y + 6, 26, 2, col.p); px(x + 6, y, 14, 5, col.s); px(x + 8, y + 1, 10, 3, LUZ);
    px(x + 11, y + 5, 2, 1, ORO); px(x + 12, y + 6, 2, 1, ORO); px(x + 13, y + 7, 2, 1, ORO); // rayo pintado
    for (let i = 0; i < 4; i++) px(x + 3 + i * 6, y + 9, 2, 1, (i + luz) % 2 ? ORO : LUZ);
    px(x + 10, y + 10, 6, SUELO - y - 10, 'rgba(125,249,255,0.25)');
  }

  /* ---------- el héroe ---------- */
  function heroe(px, e, t, celebrar, col) {
    const flota = e.poder >= 4;
    const salto = celebrar ? Math.round(Math.abs(Math.sin(t * 7)) * 4) : flota ? 7 + Math.round(Math.sin(t * 2.4) * 1.5) : Math.round(Math.sin(t * 2.2) * 0.6 + 0.4);
    const y0 = SUELO - salto;
    if (flota) { px(11, SUELO - 1, 10, 1, 'rgba(0,0,0,0.25)'); if (Math.floor(t * 6) % 2) { px(13, y0 + 1, 1, 3, LUZ); px(18, y0 + 2, 1, 2, LUZ); } }
    capa(px, e.capa, y0, t, col);
    traje(px, e.traje, y0, t, col, celebrar);
    cabeza(px, e.mascara, y0, t, col);
    poder(px, e.poder, y0, t, celebrar);
  }

  function capa(px, n, y0, t, col) {
    if (!n) return;
    const ondea = Math.round(Math.sin(t * 5) * 1.2);
    if (n === 1) { // bufanda con punta al viento
      px(11, y0 - 17, 10, 2, col.s); px(20, y0 - 16, 3, 2, col.s); px(23 + ondea, y0 - 15, 3, 2, tono(col.s, -0.2));
      return;
    }
    const color = n === 4 ? 'rgba(125,249,255,0.55)' : n === 5 ? '#1c1f4a' : tono(col.p, -0.3);
    const largo = n === 2 ? 9 : 15;
    for (let r = 0; r < largo; r++) {
      const w = 12 + Math.floor(r / 3), x = 16 - Math.floor(w / 2) - (r > largo - 4 ? ondea : 0);
      px(x, y0 - 16 + r, w, 1, color);
    }
    if (n === 5) { // estrellas que titilan y borde dorado
      for (let i = 0; i < 6; i++) if ((Math.floor(t * 3) + i) % 2) px(11 + (i * 5) % 11, y0 - 13 + (i * 4) % 11, 1, 1, i % 2 ? ORO : BLANCO);
      px(16 - 8 - ondea, y0 - 2, 17, 1, ORO);
    }
  }

  function traje(px, n, y0, t, col, celebrar) {
    // colores de cada parte según el nivel
    const casual = n === 0, buzo = n === 1;
    const torso = col.p, piernas = casual ? '#3f5f8f' : buzo ? tono(col.p, -0.25) : col.s;
    const guante = n >= 2 ? (n === 5 ? ORO : col.s) : PIEL, bota = casual ? '#2b2b33' : n === 5 ? ORO : col.s;
    // piernas y botas
    px(12, y0 - 7, 3, 7, piernas); px(17, y0 - 7, 3, 7, piernas);
    px(11, y0 - 2, 4, 2, bota); px(17, y0 - 2, 4, 2, bota);
    if (buzo) { px(12, y0 - 7, 1, 5, BLANCO); px(19, y0 - 7, 1, 5, BLANCO); }
    // torso
    px(11, y0 - 16, 10, 9, torso); px(11, y0 - 16, 10, 1, tono(torso, 0.3));
    if (casual) { px(14, y0 - 16, 4, 2, tono(col.p, -0.3)); px(13, y0 - 11, 6, 3, tono(col.p, -0.2)); } // capucha y bolsillo del polerón
    if (buzo) { px(15, y0 - 16, 2, 9, BLANCO); }
    if (n >= 2) { px(11, y0 - 8, 10, 1, TINTA); px(15, y0 - 8, 2, 1, n >= 3 ? ORO : col.s); } // cinturón
    if (n === 2) { px(15, y0 - 14, 2, 2, col.s); px(14, y0 - 13, 4, 1, col.s); } // emblema simple
    if (n >= 3) { px(12, y0 - 15, 8, 5, col.s); px(12, y0 - 15, 8, 1, tono(col.s, 0.4)); px(10, y0 - 16, 2, 2, col.s); px(20, y0 - 16, 2, 2, col.s); }
    if (n >= 4) { // líneas de energía que pulsan
      const brilla = Math.floor(t * 4) % 2 ? LUZ : '#c9fbff';
      px(12, y0 - 6, 1, 4, brilla); px(19, y0 - 6, 1, 4, brilla); px(11, y0 - 10, 1, 2, brilla); px(20, y0 - 10, 1, 2, brilla);
    }
    if (n === 5) { // rayo en el pecho
      px(16, y0 - 15, 2, 1, ORO); px(15, y0 - 14, 2, 1, ORO); px(14, y0 - 13, 4, 1, ORO); px(16, y0 - 12, 2, 1, ORO); px(15, y0 - 11, 2, 1, ORO);
    }
    // brazos
    const brazo = col.p;
    if (celebrar) {
      px(8, y0 - 21, 3, 7, brazo); px(21, y0 - 21, 3, 7, brazo); px(8, y0 - 23, 3, 2, guante); px(21, y0 - 23, 3, 2, guante);
    } else {
      px(8, y0 - 16, 3, 7, brazo); px(21, y0 - 16, 3, 7, brazo); px(8, y0 - 9, 3, 2, guante); px(21, y0 - 9, 3, 2, guante);
      if (buzo) { px(8, y0 - 16, 1, 6, BLANCO); px(23, y0 - 16, 1, 6, BLANCO); }
    }
  }

  function cabeza(px, n, y0, t, col) {
    const y = y0 - 28;
    px(10, y, 12, 12, PIEL); px(10, y + 11, 12, 1, PIEL_SOMBRA);
    const ojos = () => { px(13, y + 6, 2, 2, TINTA); px(18, y + 6, 2, 2, TINTA); };
    const pelo = () => { px(10, y, 12, 3, PELO); px(10, y + 3, 2, 3, PELO); px(20, y + 3, 2, 2, PELO); px(13, y - 1, 5, 1, PELO); };
    if (n <= 2) { pelo(); ojos(); px(15, y + 10, 3, 1, '#a0522d'); }
    if (n === 1) { px(10, y + 5, 12, 4, col.s); px(9, y + 5, 1, 2, col.s); px(13, y + 6, 2, 2, BLANCO); px(18, y + 6, 2, 2, BLANCO); px(14, y + 7, 1, 1, TINTA); px(19, y + 7, 1, 1, TINTA); }
    if (n === 2) { px(10, y + 5, 12, 3, Math.floor(t * 3) % 2 ? LUZ : '#c9fbff'); px(10, y + 5, 12, 1, BLANCO); }
    if (n === 3) { // casco ligero: cubre cabeza y orejas, cara a la vista
      px(9, y - 1, 14, 5, col.p); px(9, y - 1, 14, 1, tono(col.p, 0.35)); px(9, y + 4, 2, 6, col.p); px(21, y + 4, 2, 6, col.p);
      ojos(); px(15, y + 10, 3, 1, '#a0522d');
    }
    if (n >= 4) { // casco blindado con visor
      px(9, y - 1, 14, 13, col.p); px(9, y - 1, 14, 1, tono(col.p, 0.35)); px(9, y + 11, 14, 1, tono(col.p, -0.3));
      const visor = n === 5 && Math.floor(t * 4) % 2 ? '#c9fbff' : LUZ;
      px(11, y + 5, 10, 3, TINTA); px(12, y + 6, 8, 1, visor); px(12, y + 9, 8, 2, col.s);
    }
    if (n === 5) { // cresta de rayo
      px(15, y - 4, 2, 3, ORO); px(16, y - 6, 2, 2, ORO); px(14, y - 2, 2, 1, ORO);
      if (Math.floor(t * 5) % 2) { px(24, y - 2, 1, 1, ORO); px(7, y + 1, 1, 1, ORO); }
    }
  }

  function poder(px, n, y0, t, celebrar) {
    if (!n) return;
    const hx = 22, hy = celebrar ? y0 - 24 : y0 - 9, f = Math.floor(t * 8) % 2;
    if (n === 1 || n >= 4) { // chispas en la mano
      px(hx + 2 + f, hy - 2, 1, 1, ORO); px(hx + 3, hy + 1 - f, 1, 1, '#fff7c8'); px(hx - 1 - f, hy - 3, 1, 1, ORO);
    }
    if (n === 2) { // escudo de energía
      for (let a = 0; a < 12; a++) { const ang = -Math.PI / 2 + (a / 11) * Math.PI; px(hx + 4 + Math.round(Math.cos(ang) * 5), hy - 1 + Math.round(Math.sin(ang) * 6), 1, 1, a % 2 ? LUZ : '#c9fbff'); }
      px(hx + 3, hy - 6, 1, 11, 'rgba(125,249,255,0.35)');
    }
    if (n === 3) { // rayo desde la mano
      const largo = 10 + (f ? 2 : 0);
      px(hx + 2, hy, largo, 1, '#fff7c8'); px(hx + 2, hy - 1, largo, 1, ORO); px(hx + 2, hy + 1, largo - 3, 1, ORO);
    }
  }

  raiz.AvatarHeroes = { dibujar, COLORES, ANCHO: W, ALTO: H };
})(typeof window !== 'undefined' ? window : globalThis);
