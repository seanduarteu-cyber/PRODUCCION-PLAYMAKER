# Economía de monedas

Las reglas están en `mundos/mundos.json` (`economia`), se aplican en `js/motor.js` y se simulan en
`herramientas/simular_economia.py`. Los resultados completos están en `docs/simulacion_economia.txt`.

## Cómo se ganan

| Evento | Monedas |
|---|---|
| Desafío correcto al primer intento | 10 |
| Correcto al segundo intento | 5 |
| Correcto al tercer intento | 2 |
| Sin resolver después de 3 intentos | 0 (nunca se restan monedas) |
| Completar una sesión de 10 desafíos | +25 |
| Racha de días seguidos | +10 por día de racha, tope 50 (se paga en la primera sesión completa del día) |
| Dominar un objetivo de aprendizaje | +100, una sola vez por OA |

Equivocarse nunca descuenta monedas. Las monedas solo bajan cuando el jugador compra una mejora. Si se salta un
día, la racha vuelve a 1, pero no pierde nada de lo ganado.

## Cuánto cuestan las mejoras

Cada mundo tiene 5 espacios equipables con 5 niveles. El costo depende solo del nivel:

| Nivel | Costo | Requisito extra | Ejemplo en Valle Bloque (casco) |
|---|---|---|---|
| 1 | 50 | — | Gorro de cuero |
| 2 | 150 | — | Casco de cobre |
| 3 | 400 | — | Casco de hierro |
| 4 | 800 | — | Casco de lumita |
| 5 (final) | 1.800 | Un tramo completo dominado por cada mejora final del mundo | Corona estelar |

Un espacio completo cuesta 3.200 monedas y un mundo completo 16.000 monedas más 5 tramos dominados. Las
monedas son del jugador y sirven en cualquier mundo; las mejoras compradas pertenecen al mundo donde se
compraron.

## Por qué estos valores

Ingresos simulados por sesión, con el bono de racha y los de dominio incluidos (300 jugadores simulados por perfil):

| | Le cuesta (0,55) | Promedio (0,70) | Le va muy bien (0,85) |
|---|---|---|---|
| Monedas en la primera sesión | 107 | 116 | 124 |
| Monedas por sesión, jugando a diario | 172 | 181 | 191 |
| Monedas por sesión, 4 días por semana | 147 | 157 | 166 |

Y en cuántas sesiones se alcanza cada hito (mediana, jugando a diario):

| Hito | Le cuesta | Promedio | Le va muy bien |
|---|---|---|---|
| Primera mejora (50) | 1 | 1 | 1 |
| Juntar una mejora intermedia (400) | 4 | 4 | 3 |
| Juntar un nivel 4 (800) | 6 | 6 | 5 |
| Dominar un OA | 5 | 4 | 3 |
| Dominar un tramo | 16 | 12 | 10 |
| Juntar una mejora final (1.800) | 12 | 11 | 10 |
| Avatar completo de un mundo | 94 | 89 | 85 |

Cómo cumple cada meta del diseño:

- **La primera mejora llega en la primera sesión.** Cuesta 50, lo mismo que 5 aciertos al primer intento. Un
  jugador que resuelve casi todo al segundo intento igual la alcanza: 10 desafíos × 5 monedas + 25 de bono = 75.
  La prueba de punta a punta lo confirma: tras una sesión el jugador tenía 130 monedas y compró dos mejoras.
- **Una mejora intermedia cuesta de 3 a 5 sesiones.** El nivel 3 vale 400 monedas y se junta en 3 a 4 sesiones
  en los tres perfiles. El nivel 2 (150) queda como paso intermedio de una a dos sesiones, para que entre la
  primera mejora y la intermedia siempre haya algo cerca.
- **Las mejoras finales piden dominar un tramo completo.** Juntar 1.800 monedas toma 10 a 12 sesiones, y
  dominar un tramo (en promedio 2,75 OA) toma 10 a 16. El requisito de tramo manda o empata: la mejora final llega
  cuando el jugador domina una asignatura completa de un nivel, y no solo por acumular monedas. Cada mejora final
  adicional del mismo mundo pide un tramo más.
- **El refuerzo que se ve es el avatar.** No hay ranking ni comparación con otros jugadores, y el avatar está
  siempre en pantalla, también mientras se resuelven los desafíos. Un mundo completo toma del orden de 85 a 110
  sesiones, cerca de un año escolar jugando 3 a 4 veces por semana. Con tres mundos jugables, cada uno con sus
  propias mejoras, siempre hay otro avatar que empezar. Así siempre hay una próxima mejora a
  pocas sesiones de distancia.

Por qué cada regla de ingreso tiene ese tamaño:

- **10, 5 y 2** premian acertar al primer intento sin dejar en cero a quien insiste. El tercer intento vale
  poco porque a esa altura, con la pista y alternativas descartadas, ya hay mucho de azar.
- **El bono de sesión (25)** equivale a 2,5 aciertos. Premia terminar la sesión (10 desafíos, menos de 5
  minutos) sin que valga más que jugar bien.
- **La racha tiene tope (50)** para que faltar un día no se sienta como un castigo grande: al volver, en 5
  días se recupera el máximo.
- **El bono de dominio (100)** equivale a una sesión buena y marca el hito académico más importante.

## Supuestos y riesgos

- El modelo de jugador supone que practicar un OA mejora el desempeño: +1 punto porcentual de probabilidad de
  acierto por cada desafío practicado en ese OA (`APRENDIZAJE = 0.01`). **Sin ese aprendizaje**, la regla de
  dominio (3 aciertos seguidos en dificultad 5) es exigente: un jugador promedio tardaría unas 41 sesiones en
  dominar un OA y casi nunca completaría un tramo. Conviene medirlo con datos reales de juego. Si el dominio
  resulta demasiado lento, se ajusta en `mundos/mundos.json` (por ejemplo, contar 3 aciertos en dificultad 5
  aunque no sean seguidos), sin cambiar los costos.
- Los costos están pensados para jugar seguido. Jugando 4 días por semana baja el ingreso por sesión, porque la
  racha crece menos: los primeros hitos (primera mejora, mejora intermedia, nivel 4) quedan casi iguales, juntar
  la mejora final tarda 1 a 2 sesiones más y el avatar completo, unas 12 a 15 sesiones más (97 a 109 en vez de
  85 a 94).
- Para volver a simular después de cambiar algún valor: `python3 herramientas/simular_economia.py`.
