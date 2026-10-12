# Banco de contenido

Un archivo JSON por asignatura y nivel: `contenido/<nivel>/<asignatura>.json`. Cada archivo es una lista de
objetivos de aprendizaje (OA) con el esquema pedido. `contenido/indice.json` lista los archivos, los OA de
cada uno y los **tramos** (todos los OA de una asignatura en un nivel).

Los JSON no se editan a mano: se generan desde `herramientas/` y se validan.

```bash
python3 herramientas/generar.py    # escribe contenido/**.json
python3 herramientas/validar.py    # esquema, mínimos por OA, prerequisitos y tokens (sale con 1 si hay errores)
```

## Esquema de un objetivo

```json
{
  "nivel": "3_basico",
  "asignatura": "matematica",
  "eje": "Números y operaciones",
  "objetivo_oficial": "OA 8: Demostrar que comprende las tablas de multiplicar hasta 10…",
  "dificultad": 3,
  "prerequisitos": ["2_basico.matematica.OA11"],
  "id_objetivo": "3_basico.matematica.OA8",
  "verificacion": { "codigo": "verificado", "texto": "resumen", "fuente": "https://www.curriculumnacional.cl/…" },
  "desafios": [ … ]
}
```

Campos agregados al esquema pedido:

| Campo | Para qué |
|---|---|
| `id_objetivo` | Identificador que usan los `prerequisitos` (`<nivel>.<asignatura>.OA<n>`). |
| `verificacion.codigo` | `verificado` si el código y su tema se confirmaron en una página oficial; `pendiente` si no. |
| `verificacion.texto` | Siempre `resumen`: `objetivo_oficial` es un resumen fiel, no la cita literal. |
| `verificacion.fuente` | Página de curriculumnacional.cl donde se confirmó el código. |
| `dificultad` (del OA) | Complejidad relativa del objetivo dentro del árbol (1 = de entrada). |
| `dificultad` (de cada desafío) | Nivel 1 a 5 que usa la dificultad adaptativa. |
| `texto` (opcional) | Cuento o lectura que acompaña a un desafío de comprensión. |

## Tipos de desafío

Todos tienen `id`, `tipo`, `dificultad`, `enunciado`, `pista`, `explicacion_error` y `monedas` (10, el valor al
primer intento). Cada tipo agrega sus campos:

| Tipo | Campos propios | Cómo se responde | Corrección |
|---|---|---|---|
| `opcion_multiple` | `alternativas` (4), `correcta` (índice) | Tocar una alternativa | Índice igual a `correcta` |
| `completar` | `alternativas` (4), `correcta`; el `enunciado` trae `___` | Tocar la palabra que va en el hueco | Índice igual a `correcta` |
| `ordenar_secuencia` | `elementos` en el orden correcto (el juego los desordena) | Tocar en orden | Misma secuencia; se marcan las posiciones malas |
| `emparejar` | `pares`: `[[izquierda, derecha], …]` | Tocar izquierda y luego derecha | Cada pareja correcta; las malas se deshacen |
| `arrastrar_categoria` | `categorias`, `elementos`: `[{texto, categoria}]` | Arrastrar o tocar ficha y grupo | Cada ficha en su grupo; las malas vuelven a la bandeja |
| `respuesta_numerica` | `respuesta`, `tolerancia`, `unidad` (opcional) | Teclado numérico | `|valor − respuesta| ≤ tolerancia` (acepta punto de miles) |

Todos se resuelven con pocos toques; ninguno exige escribir texto libre, para que cada desafío tome menos de 30 segundos.

## Ambientación por mundo

Los enunciados usan tokens que el motor reemplaza según el mundo elegido (`mundos/mundos.json`). El contenido
curricular es el mismo y solo cambia el envoltorio.

| Token | Valle Bloque (bloques) | Isla Brinco (plataformas) | Ciudad Voltia (héroes) |
|---|---|---|---|
| `{personaje}` | Rocío | Pipo | Capitana Chispa |
| `{objetos}` | bloques de piedra | cascabeles | cristales de energía |
| `{los_objetos}` | los bloques de piedra | los cascabeles | los cristales de energía |
| `{lugar}` | la mina | la isla | la ciudad |
| `{el_contenedor}` / `{contenedores}` | el cofre / cofres | el baúl / baúles | el maletín / maletines |
| `{la_construccion}` | la torre | la plataforma | la base secreta |
| `{junto}` | picó | recogió | cargó |

Reglas para que el español concuerde en los tres mundos: los objetos y contenedores son siempre masculinos, y
las construcciones siempre femeninas. Ejemplo: «{personaje} {junto} 8 {objetos} y después 5 más» se lee
«Rocío picó 8 bloques de piedra…» en Valle Bloque y «Capitana Chispa cargó 8 cristales de energía…» en Ciudad Voltia.

## Cobertura actual

26 objetivos y 465 desafíos: Matemática y Lenguaje de 1° a 4° básico. Matemática tiene 20 desafíos por OA
(4 por nivel) y Lenguaje 15 (3 por nivel). Están los seis tipos de desafío.

| Nivel | Asignatura | OA | Eje | Desafíos | Código | Prerequisitos |
|---|---|---|---|---|---|---|
| 1° básico | Matemática | [OA 1](https://www.curriculumnacional.cl/614/w3-article-17473.html) | Números y operaciones | 20 | verificado | — |
| 1° básico | Matemática | [OA 4](https://curriculumnacional.mineduc.cl/614/w3-propertyvalue-53688.html) | Números y operaciones | 20 | verificado | 1° Mat OA 1 |
| 1° básico | Matemática | [OA 9](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17481:MA01-OA-09) | Números y operaciones | 20 | verificado | 1° Mat OA 1 |
| 2° básico | Matemática | [OA 1](https://www.curriculumnacional.cl/614/w3-article-17509.html) | Números y operaciones | 20 | verificado | 1° Mat OA 1 |
| 2° básico | Matemática | [OA 3](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17511:MA02-OA-03) | Números y operaciones | 20 | verificado | 1° Mat OA 4 |
| 2° básico | Matemática | [OA 9](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/matematica/2-basico/ma02-oa-09) | Números y operaciones | 20 | verificado | 1° Mat OA 9 |
| 2° básico | Matemática | [OA 11](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17519:MA02-OA-11) | Números y operaciones | 20 | verificado | 2° Mat OA 1, 2° Mat OA 9 |
| 3° básico | Matemática | [OA 6](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17551:MA03-OA-06) | Números y operaciones | 20 | verificado | 2° Mat OA 9 |
| 3° básico | Matemática | [OA 8](https://www.curriculumnacional.cl/docente/629/w3-article-17553.html) | Números y operaciones | 20 | verificado | 2° Mat OA 11 |
| 3° básico | Matemática | [OA 9](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17554:MA03-OA-09) | Números y operaciones | 20 | verificado | 3° Mat OA 8 |
| 3° básico | Matemática | [OA 11](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17556:MA03-OA-11) | Números y operaciones | 20 | verificado | 3° Mat OA 9 |
| 4° básico | Matemática | [OA 3](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17594:MA04-OA-03) | Números y operaciones | 20 | verificado | 3° Mat OA 6 |
| 4° básico | Matemática | [OA 5](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17596:MA04-OA-05) | Números y operaciones | 20 | verificado | 3° Mat OA 8 |
| 4° básico | Matemática | [OA 6](https://www.curriculumnacional.cl/614/w3-article-17597.html) | Números y operaciones | 20 | verificado | 3° Mat OA 9 |
| 4° básico | Matemática | [OA 8](https://www.curriculumnacional.cl/docentes/Educacion-General/Matematica-4-basico/MA04-OA-08/17599:MA04-OA-08) | Números y operaciones | 20 | verificado | 3° Mat OA 11 |
| 1° básico | Lenguaje | [OA 3](https://www.curriculumnacional.cl/614/w3-article-17116.html) | Lectura | 15 | verificado | — |
| 1° básico | Lenguaje | [OA 4](https://www.curriculumnacional.cl/recursos/leo-1-basico-texto-estudiante-tomo-1) | Lectura | 15 | **pendiente** | 1° Len OA 3 |
| 1° básico | Lenguaje | [OA 8](https://www.curriculumnacional.cl/recursos/leo-1-basico-texto-estudiante-tomo-1) | Lectura | 15 | **pendiente** | 1° Len OA 4 |
| 2° básico | Lenguaje | [OA 5](https://www.curriculumnacional.cl/portal/Ejes/Lenguaje-y-Comunicacion/Lectura-Comprension/17151:LE02-OA-05) | Lectura | 15 | verificado | 1° Len OA 8 |
| 2° básico | Lenguaje | [OA 21](https://www.curriculumnacional.cl/portal/Educacion-General/Lenguaje-y-comunicacion-2-basico/LE02-OA-01/131696:Programa-de-apoyo-compartido-Lenguaje-y-Comunicacion-2-basico-Periodo-2) | Escritura | 15 | **pendiente** | 1° Len OA 4 |
| 3° básico | Lenguaje | [OA 4](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/lenguaje-comunicacion/3-basico) | Lectura | 15 | verificado | 2° Len OA 5 |
| 3° básico | Lenguaje | [OA 20](https://www.curriculumnacional.cl/614/w3-article-17203.html) | Escritura | 15 | verificado | 1° Len OA 4 |
| 3° básico | Lenguaje | [OA 22](https://www.curriculumnacional.cl/portal/Ejes/Lenguaje-y-Comunicacion/Escritura-Produccion/17205:LE03-OA-22) | Escritura | 15 | verificado | 2° Len OA 21 |
| 4° básico | Lenguaje | [OA 4](https://www.curriculumnacional.cl/portal/Ejes/Lenguaje-y-Comunicacion/Lectura-Comprension/17225:LE04-OA-04) | Lectura | 15 | verificado | 3° Len OA 4 |
| 4° básico | Lenguaje | [OA 10](https://www.curriculumnacional.cl/portal/Ejes/Lectura/Vocabulario/17231:LE04-OA-10) | Lectura | 15 | verificado | 3° Len OA 4 |
| 4° básico | Lenguaje | [OA 21](https://www.curriculumnacional.cl/614/w3-article-17242.html) | Escritura | 15 | verificado | 3° Len OA 22 |

### Pendientes de verificación

- **LE01 OA 04** (leer palabras aisladas y en contexto) y **LE01 OA 08** (comprensión de narraciones): ambos
  códigos aparecen en el eje Lectura de 1° básico (texto «Leo Primero»), pero no se pudo confirmar su redacción.
- **LE02 OA 21** (ortografía de 2° básico): la lista de contenidos ortográficos apareció junto a otro código en
  la fuente; falta confirmar que el número sea 21. En 3° básico, por ejemplo, la ortografía es el OA 22 y no el 21.

Mientras estén pendientes, el juego los muestra con la etiqueta «Código por verificar» en el árbol.

### Qué falta para cubrir los cursos completos

Este primer banco cubre los objetivos centrales del eje Números y operaciones (Matemática) y de Lectura y
Escritura (Lenguaje). Faltan, por ejemplo, Geometría, Medición, Patrones y Datos en Matemática, y Comunicación
oral y los OA de escritura de textos en Lenguaje. Para agregar un OA: registrarlo en `herramientas/objetivos.py`
con su código oficial y fuente, escribir su generador (mínimo 15 desafíos, al menos 3 por nivel) y volver a
correr `generar.py` y `validar.py`.
