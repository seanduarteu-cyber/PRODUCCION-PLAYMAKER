/* Pruebas del motor: node pruebas/motor.test.js */
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const Motor = require('../js/motor.js');

const raiz = path.join(__dirname, '..');
const leer = p => JSON.parse(fs.readFileSync(path.join(raiz, p), 'utf8'));
const indice = leer('contenido/indice.json');
const bancos = indice.archivos.flatMap(a => leer('contenido/' + a.archivo));
const datos = Motor.prepararDatos(bancos, leer('mundos/mundos.json'), indice);

let n = 0;
const prueba = (nombre, fn) => { fn(); n++; console.log('✓', nombre); };
const nuevo = nivel => Motor.crearPerfil('Prueba', nivel, datos);
const OA1 = '1_basico.matematica.OA1', OA4 = '1_basico.matematica.OA4';

prueba('monedas por intento: 10, 5, 2 y 0 si no se resuelve', () => {
  const p = nuevo('1_basico');
  assert.strictEqual(Motor.registrarResultado(p, OA1, { resuelto: true, intento: 1 }, datos).monedas, 10);
  assert.strictEqual(Motor.registrarResultado(p, OA1, { resuelto: true, intento: 2 }, datos).monedas, 5);
  assert.strictEqual(Motor.registrarResultado(p, OA1, { resuelto: true, intento: 3 }, datos).monedas, 2);
  const antes = p.monedas;
  assert.strictEqual(Motor.registrarResultado(p, OA1, { resuelto: false, intento: 3 }, datos).monedas, 0);
  assert.strictEqual(p.monedas, antes, 'equivocarse nunca resta monedas');
});

prueba('dificultad adaptativa: sube con 3 aciertos seguidos y baja con 2 fallos seguidos', () => {
  const p = nuevo('1_basico');
  for (let i = 0; i < 3; i++) Motor.registrarResultado(p, OA1, { resuelto: true, intento: 1 }, datos);
  assert.strictEqual(Motor.estadoOA(p, OA1).nivel, 2);
  Motor.registrarResultado(p, OA1, { resuelto: true, intento: 2 }, datos); // segundo intento = fallo
  assert.strictEqual(Motor.estadoOA(p, OA1).nivel, 2);
  Motor.registrarResultado(p, OA1, { resuelto: false, intento: 3 }, datos);
  assert.strictEqual(Motor.estadoOA(p, OA1).nivel, 1);
  // dos aciertos y un fallo reinician la racha de aciertos
  Motor.registrarResultado(p, OA1, { resuelto: true, intento: 1 }, datos);
  Motor.registrarResultado(p, OA1, { resuelto: true, intento: 1 }, datos);
  Motor.registrarResultado(p, OA1, { resuelto: false, intento: 3 }, datos);
  Motor.registrarResultado(p, OA1, { resuelto: true, intento: 1 }, datos);
  assert.strictEqual(Motor.estadoOA(p, OA1).nivel, 1);
});

prueba('fallar en dificultad 1 sugiere repasar los prerequisitos', () => {
  const p = nuevo('1_basico');
  Motor.registrarResultado(p, OA4, { resuelto: false, intento: 3 }, datos);
  const ev = Motor.registrarResultado(p, OA4, { resuelto: false, intento: 3 }, datos);
  assert.deepStrictEqual(ev.repaso, [OA1]);
});

prueba('dominar un objetivo da 100 monedas una sola vez', () => {
  const p = nuevo('1_basico');
  let dominio = 0;
  for (let i = 0; i < 15; i++) dominio += Motor.registrarResultado(p, OA1, { resuelto: true, intento: 1 }, datos).dominado ? 1 : 0;
  assert.strictEqual(dominio, 1);
  assert.ok(Motor.estadoOA(p, OA1).dominado);
  assert.strictEqual(p.monedas, 15 * 10 + 100);
  for (let i = 0; i < 3; i++) Motor.registrarResultado(p, OA1, { resuelto: true, intento: 1 }, datos);
  assert.strictEqual(p.monedas, 18 * 10 + 100);
});

prueba('bono de sesión y racha creciente con tope', () => {
  const p = nuevo('1_basico');
  assert.deepStrictEqual(Motor.cerrarSesion(p, datos, '2026-10-01'), { bonoSesion: 25, bonoRacha: 10, dias: 1 });
  assert.strictEqual(Motor.cerrarSesion(p, datos, '2026-10-01').bonoRacha, 0, 'el bono de racha se paga una vez al día');
  assert.strictEqual(Motor.cerrarSesion(p, datos, '2026-10-02').bonoRacha, 20);
  for (const d of ['03', '04', '05', '06']) Motor.cerrarSesion(p, datos, '2026-10-' + d);
  assert.strictEqual(Motor.cerrarSesion(p, datos, '2026-10-07').bonoRacha, 50, 'tope de 50');
  assert.strictEqual(Motor.cerrarSesion(p, datos, '2026-10-09').dias, 1, 'saltarse un día reinicia la racha');
  assert.strictEqual(Motor.cerrarSesion(p, datos, '2026-11-01').dias, 1);
  assert.strictEqual(Motor.diaAnterior('2026-03-01'), '2026-02-28');
});

prueba('la primera mejora se alcanza con 5 aciertos', () => {
  const p = nuevo('1_basico');
  for (let i = 0; i < 5; i++) Motor.registrarResultado(p, OA1, { resuelto: true, intento: 1 }, datos);
  const r = Motor.comprarMejora(p, 'bloques', 'casco', datos);
  assert.ok(r.ok); assert.strictEqual(p.avatares.bloques.casco, 1); assert.strictEqual(p.monedas, 0);
});

prueba('la mejora final exige un tramo dominado por cada mejora final', () => {
  const p = nuevo('1_basico');
  p.monedas = 100000;
  for (const e of ['casco', 'armadura']) for (let i = 0; i < 4; i++) assert.ok(Motor.comprarMejora(p, 'bloques', e, datos).ok);
  assert.strictEqual(Motor.infoMejora(p, 'bloques', 'casco', datos).motivo, 'tramos');
  const tramo = datos.tramos.find(t => t.id === '1_basico.matematica');
  tramo.objetivos.forEach(id => { Motor.estadoOA(p, id).dominado = true; });
  assert.ok(Motor.comprarMejora(p, 'bloques', 'casco', datos).ok);
  assert.strictEqual(Motor.infoMejora(p, 'bloques', 'armadura', datos).tramosNecesarios, 2);
  assert.strictEqual(Motor.infoMejora(p, 'bloques', 'armadura', datos).motivo, 'tramos');
  assert.strictEqual(Motor.infoMejora(p, 'plataformas', 'skin', datos).siguiente, 1, 'cada mundo tiene su propio avatar');
});

prueba('árbol de prerequisitos', () => {
  const p1 = nuevo('1_basico');
  assert.ok(Motor.disponibilidad(p1, OA1, datos).ok);
  assert.deepStrictEqual(Motor.disponibilidad(p1, OA4, datos).faltan, [OA1]);
  Motor.estadoOA(p1, OA1).nivel = 3;
  assert.ok(Motor.disponibilidad(p1, OA4, datos).ok, 'disponible cuando el prerequisito va en dificultad 3');
  assert.strictEqual(Motor.disponibilidad(p1, '2_basico.matematica.OA1', datos).motivo, 'superior');
  const p3 = nuevo('3_basico');
  assert.ok(Motor.disponibilidad(p3, '3_basico.matematica.OA6', datos).ok, 'los niveles anteriores se asumen');
  assert.ok(!Motor.disponibilidad(p3, '3_basico.matematica.OA9', datos).ok, 'OA9 necesita avanzar en OA8');
  assert.strictEqual(Motor.recomendar(p3, 'matematica', datos), '3_basico.matematica.OA6');
  assert.strictEqual(Motor.recomendar(p3, 'lenguaje', datos), '3_basico.lenguaje.OA4');
  assert.strictEqual(Motor.nivelDeTrabajo(nuevo('6_basico'), datos), '6_basico');
  // una asignatura sin contenido del curso del jugador trabaja con el curso más alto que tenga, sin pasarse
  const sinMedio = ['matematica', 'lenguaje', 'ciencias', 'ingles'].find(a => !datos.orden.some(id => datos.objetivos[id].asignatura === a && datos.objetivos[id].nivel === '2_medio'));
  if (sinMedio) assert.strictEqual(Motor.nivelDeTrabajo(nuevo('2_medio'), datos, sinMedio), '8_basico', 'sin contenido de su curso, el más alto disponible');
  assert.strictEqual(Motor.nivelDeTrabajo(nuevo('2_medio'), datos, 'ingles'), '2_medio');
  assert.strictEqual(Motor.nivelDeTrabajo(nuevo('7_basico'), datos, 'ciencias'), '7_basico');
  const con5 = [...new Set(datos.orden.filter(id => datos.objetivos[id].nivel === '5_basico').map(id => datos.objetivos[id].asignatura))];
  assert.ok(con5.length >= 2, 'hay contenido de 5° básico en más de una asignatura');
  for (const asig of con5) {
    const oa = Motor.recomendar(nuevo('5_basico'), asig, datos);
    assert.ok(oa && oa.startsWith(`5_basico.${asig}.`), `recomienda ${asig} de 5° básico (${oa})`);
  }
});

prueba('elegir desafíos: solo del nivel actual y sin repetir hasta agotarlos', () => {
  const p = nuevo('1_basico'), vistos = new Set();
  const delNivel = datos.objetivos[OA1].desafios.filter(d => d.dificultad === 1).length;
  for (let i = 0; i < delNivel; i++) {
    const d = Motor.elegirDesafio(p, OA1, datos);
    assert.strictEqual(d.dificultad, 1); assert.ok(!vistos.has(d.id)); vistos.add(d.id);
  }
  assert.strictEqual(Motor.elegirDesafio(p, OA1, datos).dificultad, 1, 'al agotarlos vuelve a empezar');
});

prueba('ambientación: los tres mundos reemplazan todos los tokens del banco', () => {
  for (const m of datos.mundos) {
    const texto = JSON.stringify(Motor.ambientar(bancos, m.tokens));
    assert.ok(!/\{\w+\}/.test(texto), `quedan tokens sin reemplazar en ${m.id}`);
  }
  const d = datos.objetivos['1_basico.matematica.OA9'].desafios.find(x => x.enunciado.includes('{personaje}'));
  assert.ok(Motor.ambientar(d, datos.mundoPorId.bloques.tokens).enunciado.startsWith('Rocío'));
  assert.ok(Motor.ambientar(d, datos.mundoPorId.heroes.tokens).enunciado.startsWith('Capitana Chispa'));
});

prueba('corrección de los seis tipos de desafío', () => {
  const todos = bancos.flatMap(b => b.desafios), de = t => todos.find(d => d.tipo === t);
  const om = de('opcion_multiple'); assert.ok(Motor.corregir(om, om.correcta).ok); assert.ok(!Motor.corregir(om, (om.correcta + 1) % 4).ok);
  const co = de('completar'); assert.ok(Motor.corregir(co, co.correcta).ok);
  const or = de('ordenar_secuencia'); assert.ok(Motor.corregir(or, or.elementos.slice()).ok); assert.ok(!Motor.corregir(or, or.elementos.slice().reverse()).ok);
  const em = de('emparejar'), mapa = Object.fromEntries(em.pares);
  assert.ok(Motor.corregir(em, mapa).ok);
  const malo = { ...mapa }; const [a, b] = em.pares; malo[a[0]] = b[1]; malo[b[0]] = a[1];
  assert.deepStrictEqual(Motor.corregir(em, malo).malos.sort(), [a[0], b[0]].sort());
  const ca = de('arrastrar_categoria'); assert.ok(Motor.corregir(ca, ca.elementos.map(e => e.categoria)).ok);
  assert.strictEqual(Motor.corregir(ca, ca.elementos.map(() => 0)).ok, false);
  const nu = todos.find(d => d.tipo === 'respuesta_numerica' && d.tolerancia > 0);
  assert.ok(Motor.corregir(nu, nu.respuesta + nu.tolerancia).ok); assert.ok(!Motor.corregir(nu, nu.respuesta + nu.tolerancia + 1).ok);
  const exacta = todos.find(d => d.tipo === 'respuesta_numerica' && d.tolerancia === 0 && d.respuesta >= 1000);
  assert.ok(Motor.corregir(exacta, exacta.respuesta.toLocaleString('es-CL')).ok, 'acepta el número escrito con punto de miles');
});

console.log(`\n${n} pruebas OK`);
