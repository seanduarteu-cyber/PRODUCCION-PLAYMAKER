/* Avatar del Mundo de bloques (Valle Bloque): escena voxel dibujada en una grilla lógica de 64 × 56.
   equipo = { casco, armadura, herramienta, botas, estructura } con niveles 0-5. */
(function (raiz) {
  'use strict';
  const W = 64, H = 56, SUELO = 44;
  // materiales por nivel: 0 sin mejora, 1 cuero/madera, 2 cobre, 3 hierro, 4 lumita, 5 estelar
  const MAT = [null,
    { base: '#8b5a2b', luz: '#b07a45', sombra: '#5e3a1a' },
    { base: '#c8743a', luz: '#e89a5c', sombra: '#8d4b1f' },
    { base: '#c9ced6', luz: '#eef1f5', sombra: '#858b94' },
    { base: '#36c6d8', luz: '#9af0f7', sombra: '#1b7d8c' },
    { base: '#f2c230', luz: '#fff0a0', sombra: '#b07f12', gema: '#8a5cf6' }];
  const PIEL = '#f1c27d', PIEL_SOMBRA = '#d9a35f', PELO = '#5a3a22', TINTA = '#2b2118';

  function dibujar(ctx, ancho, alto, equipo, t = 0, op = {}) {
    const e = Object.assign({ casco: 0, armadura: 0, herramienta: 0, botas: 0, estructura: 0 }, equipo || {});
    const esc = Math.max(1, Math.floor(Math.min(ancho / W, alto / H)));
    const ox = Math.floor((ancho - W * esc) / 2), oy = Math.floor((alto - H * esc) / 2);
    ctx.imageSmoothingEnabled = false;
    ctx.clearRect(0, 0, ancho, alto);
    const px = (x, y, w, h, c) => { ctx.fillStyle = c; ctx.fillRect(ox + Math.round(x) * esc, oy + Math.round(y) * esc, Math.round(w) * esc, Math.round(h) * esc); };
    const quieto = op.quieto || false;
    const tt = quieto ? 0 : t;

    // cielo y nubes
    px(0, 0, W, SUELO, '#8ecdf2');
    const nube = (x, y) => { px(x, y, 9, 2, '#ffffff'); px(x + 2, y - 2, 5, 2, '#ffffff'); px(x + 1, y + 2, 7, 1, '#dff3ff'); };
    nube(((tt * 2) % 80) - 12, 6); nube(((tt * 1.3 + 40) % 80) - 12, 12);
    // suelo: pasto y tierra con manchas fijas
    px(0, SUELO, W, 2, '#5fae3d'); px(0, SUELO, W, 1, '#8fd16a');
    px(0, SUELO + 2, W, H - SUELO - 2, '#8a5a33');
    for (let i = 0; i < 24; i++) px((i * 37) % W, SUELO + 3 + ((i * 13) % (H - SUELO - 4)), 2, 1, '#5c3a1e');

    estructura(px, e.estructura, tt);
    personaje(px, e, tt, op.celebrar);
  }

  function estructura(px, n, t) {
    const x0 = 38;
    if (n === 0) { px(x0 + 10, SUELO - 3, 1, 3, '#6b4423'); px(x0 + 8, SUELO - 6, 5, 3, '#4f9a32'); return; }
    if (n === 1) { // fogata
      px(x0 + 6, SUELO - 2, 10, 2, '#6b4423'); px(x0 + 8, SUELO - 3, 6, 1, '#8b5a2b');
      const f = Math.floor(t * 8) % 2;
      px(x0 + 9, SUELO - 6 - f, 4, 3 + f, '#f28c28'); px(x0 + 10, SUELO - 8 - f, 2, 2, '#ffd34d'); px(x0 + 10, SUELO - 5, 2, 2, '#fff2a8');
      return;
    }
    if (n === 2) { // carpa a rayas
      for (let r = 0; r < 10; r++) {
        const w = 2 + r * 2, x = x0 + 11 - r;
        for (let c = 0; c < w; c++) px(x + c, SUELO - 10 + r, 1, 1, Math.floor((x + c) / 2) % 2 ? '#d9483b' : '#f6f1e3');
      }
      px(x0 + 10, SUELO - 5, 2, 5, TINTA); px(x0 + 11, SUELO - 12, 1, 2, '#6b4423');
      return;
    }
    if (n === 3) { // cabaña
      px(x0 + 3, SUELO - 10, 18, 10, '#a86b3c');
      for (let y = 0; y < 10; y += 2) px(x0 + 3, SUELO - 10 + y, 18, 1, '#8b5a2b');
      for (let r = 0; r < 6; r++) px(x0 + 6 - r + 3 - 3, SUELO - 16 + r, 12 + r * 2 - 0, 1, '#6b3b1d');
      px(x0 + 10, SUELO - 6, 4, 6, '#5e3a1a'); px(x0 + 5, SUELO - 8, 3, 3, '#ffe28a'); px(x0 + 16, SUELO - 8, 3, 3, '#ffe28a');
      return;
    }
    if (n === 4) { // torre de vigía de piedra
      px(x0 + 6, SUELO - 22, 12, 22, '#9aa0a8');
      for (let y = 0; y < 22; y += 3) px(x0 + 6 + ((y / 3) % 2) * 3, SUELO - 22 + y, 6, 1, '#7d838b');
      for (let c = 0; c < 4; c++) px(x0 + 6 + c * 3, SUELO - 25, 2, 3, '#9aa0a8');
      px(x0 + 10, SUELO - 6, 4, 6, TINTA); px(x0 + 10, SUELO - 16, 4, 3, '#ffe28a');
      px(x0 + 12, SUELO - 31, 1, 6, '#5e3a1a'); px(x0 + 13, SUELO - 31, 4, 3, '#d9483b');
      return;
    }
    // 5: castillo de lumita
    const brillo = (Math.sin(t * 4) + 1) / 2 > 0.5 ? '#9af0f7' : '#36c6d8';
    px(x0, SUELO - 14, 24, 14, '#a6adb6');
    for (let y = 0; y < 14; y += 3) px(x0 + ((y / 3) % 2) * 4, SUELO - 14 + y, 24, 1, '#8a9099');
    px(x0 - 1, SUELO - 22, 7, 22, '#9aa0a8'); px(x0 + 18, SUELO - 22, 7, 22, '#9aa0a8');
    for (const tx of [x0 - 1, x0 + 18]) { for (let c = 0; c < 3; c++) px(tx + c * 3, SUELO - 24, 2, 2, '#9aa0a8'); px(tx + 2, SUELO - 27, 3, 3, brillo); }
    px(x0 + 9, SUELO - 8, 6, 8, '#3b2a1e'); px(x0 + 3, SUELO - 11, 3, 3, brillo); px(x0 + 18, SUELO - 11, 3, 3, brillo);
    px(x0 + 11, SUELO - 22, 1, 8, '#5e3a1a'); px(x0 + 12, SUELO - 22, 5, 4, '#8a5cf6'); px(x0 + 14, SUELO - 21, 1, 1, '#f2c230');
  }

  function personaje(px, e, t, celebrar) {
    const salto = celebrar ? Math.round(Math.abs(Math.sin(t * 7)) * 4) : Math.round(Math.sin(t * 2.2) * 0.6 + 0.4);
    const y0 = SUELO - salto;
    const arm = MAT[e.armadura], bot = MAT[e.botas], cas = MAT[e.casco];
    // piernas y botas
    px(12, y0 - 6, 3, 6, '#3f5f8f'); px(17, y0 - 6, 3, 6, '#3f5f8f');
    const botaC = bot ? bot.base : '#6b4423', botaL = bot ? bot.luz : '#8b5a2b';
    px(11, y0 - 3, 4, 3, botaC); px(17, y0 - 3, 4, 3, botaC); px(11, y0 - 3, 4, 1, botaL); px(17, y0 - 3, 4, 1, botaL);
    if (e.botas === 5) { px(10, y0 - 2, 1, 1, MAT[5].gema); px(21, y0 - 2, 1, 1, MAT[5].gema); }
    // cuerpo
    const torso = arm ? arm.base : '#e2763b';
    px(11, y0 - 15, 10, 9, torso);
    if (arm) {
      px(11, y0 - 15, 10, 2, arm.luz); px(11, y0 - 8, 10, 2, arm.sombra);
      px(15, y0 - 13, 2, 4, e.armadura >= 4 ? (e.armadura === 5 ? MAT[5].gema : '#e9fdff') : arm.sombra);
    } else { px(15, y0 - 15, 2, 3, '#f6f1e3'); }
    px(11, y0 - 7, 10, 1, TINTA);
    // brazos (arriba si celebra)
    const brazo = arm ? arm.luz : '#e2763b';
    if (celebrar) {
      px(8, y0 - 20, 3, 7, brazo); px(21, y0 - 20, 3, 7, brazo); px(8, y0 - 22, 3, 2, PIEL); px(21, y0 - 22, 3, 2, PIEL);
    } else {
      px(8, y0 - 15, 3, 7, brazo); px(21, y0 - 15, 3, 7, brazo); px(8, y0 - 8, 3, 2, PIEL); px(21, y0 - 8, 3, 2, PIEL);
    }
    herramienta(px, e.herramienta, celebrar ? 22 : 23, celebrar ? y0 - 21 : y0 - 7, t);
    // cabeza
    px(10, y0 - 27, 12, 12, PIEL); px(10, y0 - 16, 12, 1, PIEL_SOMBRA);
    px(13, y0 - 22, 2, 2, TINTA); px(18, y0 - 22, 2, 2, TINTA); px(15, y0 - 18, 3, 1, '#a0522d');
    if (!cas) { px(10, y0 - 27, 12, 3, PELO); px(10, y0 - 24, 2, 4, PELO); px(20, y0 - 24, 2, 3, PELO); return; }
    if (e.casco === 5) { // corona estelar sobre el pelo
      px(10, y0 - 27, 12, 3, PELO); px(10, y0 - 24, 2, 4, PELO); px(20, y0 - 24, 2, 3, PELO);
      px(10, y0 - 30, 12, 3, cas.base); px(10, y0 - 33, 2, 3, cas.base); px(15, y0 - 34, 2, 4, cas.base); px(20, y0 - 33, 2, 3, cas.base);
      px(12, y0 - 29, 2, 1, cas.gema); px(18, y0 - 29, 2, 1, cas.gema); px(15, y0 - 30, 2, 1, '#ffffff');
      if (Math.floor(t * 3) % 2) px(24, y0 - 33, 1, 1, '#fff0a0');
      return;
    }
    px(9, y0 - 28, 14, 4, cas.base); px(9, y0 - 28, 14, 1, cas.luz);
    if (e.casco >= 2) { px(9, y0 - 24, 2, 6, cas.base); px(21, y0 - 24, 2, 6, cas.base); px(12, y0 - 26, 1, 1, cas.sombra); px(19, y0 - 26, 1, 1, cas.sombra); }
    else { px(8, y0 - 25, 16, 1, cas.sombra); }
    if (e.casco >= 3) px(15, y0 - 24, 2, 3, cas.sombra);
    if (e.casco === 4) { px(15, y0 - 30, 2, 2, (Math.floor(t * 4) % 2) ? '#e9fdff' : cas.base); }
  }

  function herramienta(px, n, x, y, t) {
    if (!n) return;
    const m = MAT[n];
    const mango = n === 1 ? '#a86b3c' : '#6b4423';
    for (let i = 0; i < 7; i++) px(x + Math.floor(i / 2), y - i, 1, 1, mango); // mango en diagonal
    const hx = x + 3, hy = y - 8;
    if (n === 1) { px(hx - 1, hy - 3, 3, 4, '#c79a62'); px(hx - 1, hy - 3, 3, 1, '#e0b77f'); return; } // pala de madera
    if (n === 2 || n === 3) { // pico
      px(hx - 3, hy, 8, 2, m.base); px(hx - 3, hy, 8, 1, m.luz); px(hx - 4, hy + 2, 1, 1, m.base); px(hx + 5, hy + 2, 1, 1, m.base);
      return;
    }
    if (n === 4) { px(hx - 2, hy - 2, 6, 4, m.base); px(hx - 2, hy - 2, 6, 1, m.luz); px(hx, hy - 1, 2, 2, '#e9fdff'); return; } // martillo de lumita
    // taladro estelar
    px(hx - 2, hy - 1, 5, 3, m.base); px(hx + 3, hy, 2, 1, m.sombra); px(hx + 5, hy, 1, 1, m.sombra);
    px(hx - 1, hy - 1, 1, 1, m.gema);
    if (Math.floor(t * 6) % 2) { px(hx + 7, hy - 1, 1, 1, '#fff0a0'); px(hx + 6, hy + 2, 1, 1, '#fff0a0'); }
  }

  raiz.AvatarBloques = { dibujar, ANCHO: W, ALTO: H };
})(typeof window !== 'undefined' ? window : globalThis);
