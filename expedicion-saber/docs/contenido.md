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
| `audio` (opcional) | `{texto, idioma}`: lo que el juego lee en voz alta, sobre todo en Inglés (`idioma: "en"`). En los desafíos de comprensión oral el texto no se muestra: se escucha con 🔊, se repite más lento con 🐢 y, si el equipo no tiene voz, se puede ver. |

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
| `respuesta_numerica` | `respuesta`, `tolerancia`, `unidad` (opcional) | Teclado numérico; si algún desafío del OA tiene respuesta negativa, aparece la tecla «−» en todos los de ese OA | `|valor − respuesta| ≤ tolerancia` (acepta punto de miles) |

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

<!-- inicio:cobertura -->
124 objetivos y 2.074 desafíos (115 con audio en inglés). Resumen por asignatura:

| Asignatura | Cursos | OA | Desafíos |
|---|---|---|---|
| Matemática | 1° básico a 4° medio | 37 | 680 |
| Lenguaje y Comunicación | 1° básico a 8° básico | 21 | 332 |
| Ciencias Naturales | 1° básico a 4° medio | 38 | 599 |
| Inglés | 1° básico a 4° medio | 28 | 463 |

Registrados en `herramientas/objetivos.py` y aún sin desafíos (12): 1°M Len OA 3, 1°M Len OA 4, 1°M Len OA 9, 2°M Len OA 3, 2°M Len OA 9, 2°M Len OA 18, 3°M Len LELI OAC 01, 3°M Len LELI OAC 03, 3°M Len LELI OAC 05, 4°M Len LELI OAC 01, 4°M Len LELI OAC 03, 4°M Len LELI OAC 04.

### Matemática

| Nivel | OA | Eje | Desafíos | Código | Prerequisitos |
|---|---|---|---|---|---|
| 1° básico | [OA 1](https://www.curriculumnacional.cl/614/w3-article-17473.html) | Números y operaciones | 20 | verificado | — |
| 1° básico | [OA 4](https://curriculumnacional.mineduc.cl/614/w3-propertyvalue-53688.html) | Números y operaciones | 20 | verificado | 1° Mat OA 1 |
| 1° básico | [OA 9](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17481:MA01-OA-09) | Números y operaciones | 20 | verificado | 1° Mat OA 1 |
| 2° básico | [OA 1](https://www.curriculumnacional.cl/614/w3-article-17509.html) | Números y operaciones | 20 | verificado | 1° Mat OA 1 |
| 2° básico | [OA 3](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17511:MA02-OA-03) | Números y operaciones | 20 | verificado | 1° Mat OA 4 |
| 2° básico | [OA 9](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/matematica/2-basico/ma02-oa-09) | Números y operaciones | 20 | verificado | 1° Mat OA 9 |
| 2° básico | [OA 11](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17519:MA02-OA-11) | Números y operaciones | 20 | verificado | 2° Mat OA 1, 2° Mat OA 9 |
| 3° básico | [OA 6](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17551:MA03-OA-06) | Números y operaciones | 20 | verificado | 2° Mat OA 9 |
| 3° básico | [OA 8](https://www.curriculumnacional.cl/docente/629/w3-article-17553.html) | Números y operaciones | 20 | verificado | 2° Mat OA 11 |
| 3° básico | [OA 9](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17554:MA03-OA-09) | Números y operaciones | 20 | verificado | 3° Mat OA 8 |
| 3° básico | [OA 11](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17556:MA03-OA-11) | Números y operaciones | 20 | verificado | 3° Mat OA 9 |
| 4° básico | [OA 3](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17594:MA04-OA-03) | Números y operaciones | 20 | verificado | 3° Mat OA 6 |
| 4° básico | [OA 5](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17596:MA04-OA-05) | Números y operaciones | 20 | verificado | 3° Mat OA 8 |
| 4° básico | [OA 6](https://www.curriculumnacional.cl/614/w3-article-17597.html) | Números y operaciones | 20 | verificado | 3° Mat OA 9 |
| 4° básico | [OA 8](https://www.curriculumnacional.cl/docentes/Educacion-General/Matematica-4-basico/MA04-OA-08/17599:MA04-OA-08) | Números y operaciones | 20 | verificado | 3° Mat OA 11 |
| 5° básico | [OA 3](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17641:MA05-OA-03) | Números y operaciones | 20 | verificado | 4° Mat OA 5 |
| 5° básico | [OA 4](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17642:MA05-OA-04) | Números y operaciones | 20 | verificado | 4° Mat OA 6 |
| 5° básico | [OA 7](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/matematica/5-basico) | Números y operaciones | 20 | verificado | 4° Mat OA 8 |
| 6° básico | [OA 1](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17686:MA06-OA-01) | Números y operaciones | 20 | verificado | 5° Mat OA 3, 5° Mat OA 4 |
| 6° básico | [OA 4](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros-y-operaciones/17689:MA06-OA-04) | Números y operaciones | 20 | verificado | 5° Mat OA 7 |
| 7° básico | [OA 1](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros/70512:MA07-OA-01) | Números | 20 | verificado | 4° Mat OA 3 |
| 7° básico | [OA 4](https://www.curriculumnacional.cl/614/w3-article-70515.html) | Números | 20 | verificado | 6° Mat OA 4 |
| 8° básico | [OA 1](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/matematica/8-basico) | Números | 20 | verificado | 7° Mat OA 1 |
| 8° básico | [OA 3](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/matematica/8-basico) | Números | 20 | verificado | 5° Mat OA 3 |
| 8° básico | [OA 7](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/matematica/8-basico) | Álgebra y funciones | 20 | verificado | 8° Mat OA 1 |
| 1° medio | [OA 1](https://www.curriculumnacional.cl/614/w3-article-81005.html) | Números | 15 | verificado | 8° Mat OA 1 |
| 1° medio | [OA 4](https://www.curriculumnacional.cl/614/w3-article-81008.html) | Álgebra y funciones | 15 | verificado | 8° Mat OA 7 |
| 1° medio | [OA 14](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Probabilidad-y-estadistica/81018:MA1M-OA-14) | Probabilidad y estadística | 15 | verificado | — |
| 2° medio | [OA 2](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Numeros/81042:MA2M-OA-02) | Números | 15 | verificado | 1°M Mat OA 1, 8° Mat OA 3 |
| 2° medio | [OA 4](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Algebra-y-funciones/81044:MA2M-OA-04) | Álgebra y funciones | 15 | verificado | 1°M Mat OA 4 |
| 2° medio | [OA 11](https://www.curriculumnacional.cl/portal/Ejes/Matematica/Probabilidad-y-estadistica/81051:MA2M-OA-11) | Probabilidad y estadística | 15 | verificado | 1°M Mat OA 14 |
| 3° medio | [FG-MATE-3M-OAC-01](https://www.curriculumnacional.cl/curriculum/3o-4o-medio/matematica-3o-medio/3-medio-fg) | Números | 15 | verificado | 2°M Mat OA 2 |
| 3° medio | [FG-MATE-3M-OAC-02](https://www.curriculumnacional.cl/portal/Ejes/Matematica/91154:FG-MATE-3M-OAC-02) | Probabilidad y estadística | 15 | verificado | 2°M Mat OA 11 |
| 3° medio | [FG-MATE-3M-OAC-03](https://www.curriculumnacional.cl/docentes/Formacion-General/Matematica-3-medio/FG-MATE-3M-OAC-03/91155:FG-MATE-3M-OAC-03) | Álgebra y funciones | 15 | verificado | 2°M Mat OA 2 |
| 4° medio | [FG-MATE-4M-OAC-01](https://www.curriculumnacional.cl/portal/Ejes/Matematica/91169:FG-MATE-4M-OAC-01) | Números | 15 | verificado | 3°M Mat MATE OAC 03 |
| 4° medio | [FG-MATE-4M-OAC-02](https://www.curriculumnacional.cl/portal/Ejes/Matematica/91170:FG-MATE-4M-OAC-02) | Probabilidad y estadística | 15 | verificado | 3°M Mat MATE OAC 02 |
| 4° medio | [FG-MATE-4M-OAC-03](https://www.curriculumnacional.cl/portal/Formacion-General/Matematica/Matematica-4-medio/145083:Unidad-3-Funciones-potencias-y-trigonometricas) | Álgebra y funciones | 15 | verificado | 3°M Mat MATE OAC 03 |

### Lenguaje y Comunicación

| Nivel | OA | Eje | Desafíos | Código | Prerequisitos |
|---|---|---|---|---|---|
| 1° básico | [OA 3](https://www.curriculumnacional.cl/614/w3-article-17116.html) | Lectura | 15 | verificado | — |
| 1° básico | [OA 4](https://www.curriculumnacional.cl/recursos/leo-1-basico-texto-estudiante-tomo-1) | Lectura | 15 | **pendiente** | 1° Len OA 3 |
| 1° básico | [OA 8](https://www.curriculumnacional.cl/recursos/leo-1-basico-texto-estudiante-tomo-1) | Lectura | 15 | **pendiente** | 1° Len OA 4 |
| 2° básico | [OA 5](https://www.curriculumnacional.cl/portal/Ejes/Lenguaje-y-Comunicacion/Lectura-Comprension/17151:LE02-OA-05) | Lectura | 15 | verificado | 1° Len OA 8 |
| 2° básico | [OA 21](https://www.curriculumnacional.cl/portal/Educacion-General/Lenguaje-y-comunicacion-2-basico/LE02-OA-01/131696:Programa-de-apoyo-compartido-Lenguaje-y-Comunicacion-2-basico-Periodo-2) | Escritura | 15 | **pendiente** | 1° Len OA 4 |
| 3° básico | [OA 4](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/lenguaje-comunicacion/3-basico) | Lectura | 15 | verificado | 2° Len OA 5 |
| 3° básico | [OA 20](https://www.curriculumnacional.cl/614/w3-article-17203.html) | Escritura | 15 | verificado | 1° Len OA 4 |
| 3° básico | [OA 22](https://www.curriculumnacional.cl/portal/Ejes/Lenguaje-y-Comunicacion/Escritura-Produccion/17205:LE03-OA-22) | Escritura | 15 | verificado | 2° Len OA 21 |
| 4° básico | [OA 4](https://www.curriculumnacional.cl/portal/Ejes/Lenguaje-y-Comunicacion/Lectura-Comprension/17225:LE04-OA-04) | Lectura | 15 | verificado | 3° Len OA 4 |
| 4° básico | [OA 10](https://www.curriculumnacional.cl/portal/Ejes/Lectura/Vocabulario/17231:LE04-OA-10) | Lectura | 15 | verificado | 3° Len OA 4 |
| 4° básico | [OA 21](https://www.curriculumnacional.cl/614/w3-article-17242.html) | Escritura | 15 | verificado | 3° Len OA 22 |
| 5° básico | [OA 4](https://www.curriculumnacional.cl/614/w3-article-17262.html) | Lectura | 17 | verificado | 4° Len OA 4 |
| 5° básico | [OA 12](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/lenguaje-comunicacion/5-basico) | Lectura | 16 | verificado | 4° Len OA 10 |
| 5° básico | [OA 21](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/lenguaje-comunicacion/5-basico) | Escritura | 17 | verificado | 3° Len OA 20 |
| 5° básico | [OA 22](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/lenguaje-comunicacion/5-basico) | Escritura | 17 | verificado | 4° Len OA 21 |
| 6° básico | [OA 4](https://www.curriculumnacional.cl/docentes/Educacion-General/Lenguaje-y-comunicacion-6-basico/LE06-OA-04/17299:LE06-OA-04) | Lectura | 16 | verificado | 5° Len OA 4 |
| 6° básico | [OA 21](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/lenguaje-comunicacion/6-basico) | Escritura | 17 | **pendiente** | 5° Len OA 21 |
| 7° básico | [OA 3](https://www.curriculumnacional.cl/portal/Ejes/Lenguaje-y-Comunicacion/Lectura-Comprension/70382:LE07-OA-03) | Lectura | 17 | verificado | 6° Len OA 4 |
| 7° básico | [OA 4](https://www.curriculumnacional.cl/portal/Ejes/Lenguaje-y-Comunicacion/Lectura-Comprension/70383:LE07-OA-04) | Lectura | 16 | verificado | 5° Len OA 4 |
| 8° básico | [OA 3](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/lengua-literatura/8-basico) | Lectura | 17 | verificado | 7° Len OA 3 |
| 8° básico | [OA 4](https://www.curriculumnacional.cl/614/w3-article-70416.html) | Lectura | 17 | verificado | 7° Len OA 4 |

### Ciencias Naturales

| Nivel | OA | Eje | Desafíos | Código | Prerequisitos |
|---|---|---|---|---|---|
| 1° básico | [OA 1](https://www.curriculumnacional.cl/docentes/Educacion-General/Ciencias-Naturales-1-basico/CN01-OA-01/18361:CN01-OA-01) | Ciencias de la vida | 16 | verificado | — |
| 1° básico | [OA 4](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-Naturales/Ciencias-de-la-Vida/18364:CN01-OA-04) | Ciencias de la vida | 17 | verificado | 1° Cie OA 1 |
| 1° básico | [OA 12](https://www.curriculumnacional.cl/614/w3-article-18372.html) | Ciencias de la Tierra y el Universo | 16 | verificado | — |
| 2° básico | [OA 1](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-Naturales/Ciencias-de-la-Vida/18383:CN02-OA-01) | Ciencias de la vida | 16 | verificado | 1° Cie OA 1 |
| 2° básico | [OA 7](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/ciencias-naturales/2-basico) | Ciencias de la vida | 16 | verificado | 1° Cie OA 1 |
| 2° básico | [OA 9](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/ciencias-naturales/2-basico/cn02-oa-09) | Ciencias físicas y químicas | 16 | verificado | — |
| 3° básico | [OA 1](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/ciencias-naturales/3-basico) | Ciencias de la vida | 16 | verificado | 1° Cie OA 4 |
| 3° básico | [OA 9](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/ciencias-naturales/3-basico) | Ciencias físicas y químicas | 16 | verificado | — |
| 3° básico | [OA 11](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-Naturales/Ciencias-de-la-Tierra-y-el-Universo/18418:CN03-OA-11) | Ciencias de la Tierra y el Universo | 16 | verificado | 1° Cie OA 12 |
| 3° básico | [OA 12](https://www.curriculumnacional.cl/portal/Educacion-General/Ciencias-Naturales-3-basico/CN03-OA-12/182826:Ficha-Pedagogica-para-la-priorizacion-curricular-Ciencias-naturales-3-basico-OA-12) | Ciencias de la Tierra y el Universo | 16 | verificado | 3° Cie OA 11 |
| 4° básico | [OA 1](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-Naturales/Ciencias-de-la-Vida/18433:CN04-OA-01) | Ciencias de la vida | 16 | verificado | 2° Cie OA 1 |
| 4° básico | [OA 3](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-Naturales/Ciencias-de-la-Vida/18435:CN04-OA-03) | Ciencias de la vida | 16 | verificado | 4° Cie OA 1, 3° Cie OA 1 |
| 4° básico | [OA 5](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/ciencias-naturales/4-basico) | Ciencias de la vida | 16 | verificado | 2° Cie OA 7 |
| 4° básico | [OA 16](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-Naturales/Ciencias-de-la-Tierra-y-el-Universo/18448:CN04-OA-16) | Ciencias de la Tierra y el Universo | 17 | verificado | — |
| 5° básico | [OA 1](https://www.curriculumnacional.cl/614/w3-article-18462.html) | Ciencias de la vida | 16 | verificado | 2° Cie OA 7 |
| 5° básico | [OA 8](https://www.curriculumnacional.cl/docentes/Educacion-General/Ciencias-Naturales-5-basico/CN05-OA-08/18469:CN05-OA-08) | Ciencias físicas y químicas | 16 | verificado | — |
| 5° básico | [OA 10](https://www.curriculumnacional.cl/docentes/Educacion-General/Ciencias-Naturales-5-basico/CN05-OA-10/18471:CN05-OA-10) | Ciencias físicas y químicas | 15 | verificado | 5° Cie OA 8 |
| 6° básico | [OA 1](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/ciencias-naturales/6-basico) | Ciencias de la vida | 16 | verificado | 4° Cie OA 3, 3° Cie OA 1 |
| 6° básico | [OA 8](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/ciencias-naturales/6-basico) | Ciencias físicas y químicas | 16 | verificado | 5° Cie OA 8 |
| 6° básico | [OA 13](https://www.curriculumnacional.cl/curriculum/1o-6o-basico/ciencias-naturales/6-basico) | Ciencias físicas y químicas | 16 | verificado | 2° Cie OA 9 |
| 7° básico | [OA 8](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/ciencias-naturales/7-basico) | Física | 16 | verificado | — |
| 7° básico | [OA 13](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/ciencias-naturales/7-basico) | Química | 16 | verificado | 6° Cie OA 13 |
| 7° básico | [OA 14](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/ciencias-naturales/7-basico) | Química | 16 | verificado | 6° Cie OA 13 |
| 8° básico | [OA 10](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-Naturales/Fisica/70202:CN08-OA-10) | Física | 17 | verificado | 5° Cie OA 10 |
| 8° básico | [OA 11](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/ciencias-naturales/8-basico) | Física | 16 | verificado | 6° Cie OA 8, 6° Cie OA 13 |
| 8° básico | [OA 12](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/ciencias-naturales/8-basico) | Química | 17 | verificado | 7° Cie OA 14 |
| 1° medio | [OA 2](https://www.curriculumnacional.cl/614/w3-article-80700.html) | Biología | 15 | verificado | — |
| 1° medio | [OA 9](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-Naturales/Fisica/80707:CN1M-OA-09) | Física | 15 | verificado | — |
| 1° medio | [OA 18](https://www.curriculumnacional.cl/portal/Ejes/Quimica/Reacciones-quimicas/80716:CN1M-OA-18) | Química | 15 | verificado | 8° Cie OA 12 |
| 2° medio | [OA 7](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-Naturales/Biologia/80746:CN2M-OA-07) | Biología | 15 | verificado | 1°M Cie OA 2 |
| 2° medio | [OA 9](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-Naturales/Fisica/80748:CN2M-OA-09) | Física | 15 | verificado | — |
| 2° medio | [OA 15](https://www.curriculumnacional.cl/614/w3-article-80754.html) | Química | 15 | verificado | 1°M Cie OA 18 |
| 3° medio | [FG-CIBS-3y4-OAC-01](https://www.curriculumnacional.cl/614/w3-article-91029.html) | Bienestar y salud | 15 | verificado | — |
| 3° medio | [FG-CITS-3y4-OAC-02](https://www.curriculumnacional.cl/docentes/Formacion-General/Tecnologia-y-sociedad/FG-CITS-3y4-OAC-02/91045:FG-CITS-3y4-OAC-02) | Tecnología y sociedad | 15 | verificado | 1°M Cie OA 9 |
| 3° medio | [FG-CIBS-3y4-OAC-03](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-para-la-ciudadania/Bienestar-y-salud/91031:FG-CIBS-3y4-OAC-03) | Bienestar y salud | 15 | verificado | 3°M Cie CIBS OAC 01 |
| 4° medio | [FG-CISA-3y4-OAC-01](https://www.curriculumnacional.cl/docentes/Formacion-General/Seguridad-prevencion-y-autocuidado/FG-CISA-3y4-OAC-01/91041:FG-CISA-3y4-OAC-01) | Seguridad, prevención y autocuidado | 15 | verificado | 2°M Cie OA 15, 1°M Cie OA 18 |
| 4° medio | [FG-CISA-3y4-OAC-02](https://www.curriculumnacional.cl/portal/Curso/Educacion-General/3-Medio-FG/144973:Unidad-2-Modulo-Seguridad-prevencion-y-autocuidado-Amenazas-y-riesgos-cerca-de-nosotros-Estoy-actuando-responsablemente) | Seguridad, prevención y autocuidado | 15 | verificado | 8° Cie OA 10, 8° Cie OA 11 |
| 4° medio | [FG-CIAS-3y4-OAC-03](https://www.curriculumnacional.cl/portal/Ejes/Ciencias-para-la-ciudadania/Ambiente-y-sostenibilidad/91028:FG-CIAS-3y4-OAC-03) | Ambiente y sostenibilidad | 15 | verificado | 8° Cie OA 11 |

### Inglés

| Nivel | OA | Eje | Desafíos | Código | Prerequisitos |
|---|---|---|---|---|---|
| 1° básico | [OA 1](https://www.curriculumnacional.cl/614/w3-article-20874.html) | Comprensión oral | 18 | verificado | — |
| 1° básico | [OA 13](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Expresion-escrita/20886:EN01-OA-13) | Expresión escrita | 19 | **pendiente** | 1° Ing OA 1 |
| 2° básico | [OA 1](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Comprension-oral/20893:EN02-OA-01) | Comprensión oral | 19 | verificado | 1° Ing OA 1 |
| 2° básico | [OA 13](https://www.curriculumnacional.cl/portal/Educacion-General/Ingles-Propuesta-curricular-/Ingles-Propuesta-2-basico/) | Expresión escrita | 18 | **pendiente** | 1° Ing OA 13 |
| 3° básico | [OA 1](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Comprension-oral/20913:EN03-OA-01) | Comprensión oral | 19 | verificado | 2° Ing OA 1 |
| 3° básico | [OA 13](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Expresion-escrita/20924:EN03-OA-13) | Expresión escrita | 19 | verificado | 2° Ing OA 13 |
| 4° básico | [OA 1](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Comprension-oral/20930:EN04-OA-01) | Comprensión oral | 18 | verificado | 3° Ing OA 1 |
| 4° básico | [OA 13](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Expresion-escrita/20942:EN04-OA-13) | Expresión escrita | 18 | verificado | 3° Ing OA 13 |
| 5° básico | [OA 5](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Comprension-de-lectura/18708:IN05-OA-05) | Comprensión de lectura | 17 | verificado | 4° Ing OA 1 |
| 5° básico | [OA 14](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Expresion-escrita/18717:IN05-OA-14) | Expresión escrita | 17 | verificado | 4° Ing OA 13 |
| 6° básico | [OA 5](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Comprension-de-lectura/18728:IN06-OA-05) | Comprensión de lectura | 16 | verificado | 5° Ing OA 5 |
| 6° básico | [OA 15](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Expresion-escrita/18738:IN06-OA-15) | Expresión escrita | 17 | verificado | 5° Ing OA 14 |
| 7° básico | [OA 9](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/ingles/7-basico/in07-oa-09) | Comprensión de lectura | 17 | verificado | 6° Ing OA 5 |
| 7° básico | [OA 16](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Expresion-escrita/70353:IN07-OA-16) | Expresión escrita | 17 | verificado | 6° Ing OA 15 |
| 8° básico | [OA 9](https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/ingles/8-basico) | Comprensión de lectura | 17 | verificado | 7° Ing OA 9 |
| 8° básico | [OA 16](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Expresion-escrita/70374:IN08-OA-16) | Expresión escrita | 17 | verificado | 7° Ing OA 16 |
| 1° medio | [OA 9](https://www.curriculumnacional.cl/docentes/Educacion-General/Ingles-1-medio/IN1M-OA-09/80907:IN1M-OA-09) | Comprensión de lectura | 15 | verificado | 8° Ing OA 9 |
| 1° medio | [OA 10](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Comprension-de-lectura/) | Comprensión de lectura | 15 | verificado | 8° Ing OA 9 |
| 1° medio | [OA 16](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Expresion-escrita/80914:IN1M-OA-16) | Expresión escrita | 15 | verificado | 8° Ing OA 16 |
| 2° medio | [OA 10](https://www.curriculumnacional.cl/portal/Innovacion/Lineas-de-Innovacion/Modernizacion-de-Textos-escolares-2020/140095:Textos-Escolares-Reimpresos-Ingles-2-medio) | Comprensión de lectura | 15 | verificado | 1°M Ing OA 10 |
| 2° medio | [OA 11](https://www.curriculumnacional.cl/portal/Innovacion/Lineas-de-Innovacion/Modernizacion-de-Textos-escolares-2020/140095:Textos-Escolares-Reimpresos-Ingles-2-medio) | Comprensión de lectura | 15 | verificado | 1°M Ing OA 9 |
| 2° medio | [OA 16](https://www.curriculumnacional.cl/portal/Ejes/Ingles/Expresion-escrita/80935:IN2M-OA-16) | Expresión escrita | 15 | verificado | 1°M Ing OA 16 |
| 3° medio | [FG-INGL-3M-OAC-01](https://www.curriculumnacional.cl/portal/Ejes/Ingles/91128:FG-INGL-3M-OAC-01) | Comprensión | 15 | verificado | 2°M Ing OA 10, 2°M Ing OA 11 |
| 3° medio | [FG-INGL-3M-OAC-02](https://www.curriculumnacional.cl/docentes/Formacion-General/Ingles-3-medio/FG-INGL-3M-OAC-02/91129:FG-INGL-3M-OAC-02) | Producción | 15 | verificado | 2°M Ing OA 16 |
| 3° medio | [FG-INGL-3M-OAC-03](https://www.curriculumnacional.cl/portal/Formacion-General/Ingles/Ingles-3-medio/145038:Unidad-2-My-Reflections-on-Global-Issues) | Comprensión y producción | 15 | verificado | 3°M Ing INGL OAC 01, 3°M Ing INGL OAC 02 |
| 4° medio | [FG-INGL-4M-OAC-01](https://www.curriculumnacional.cl/curriculum/3o-4o-medio/ingles-4o-medio/4-medio-fg) | Comprensión | 15 | verificado | 3°M Ing INGL OAC 01 |
| 4° medio | [FG-INGL-4M-OAC-02](https://www.curriculumnacional.cl/curriculum/3o-4o-medio/ingles-4o-medio/4-medio-fg/fg-ingl-4m-oac-02) | Producción | 15 | verificado | 3°M Ing INGL OAC 02 |
| 4° medio | [FG-INGL-4M-OAC-03](https://www.curriculumnacional.cl/portal/Formacion-General/Ingles/Ingles-4-medio/145048:Unidad-3-It-s-business-time) | Comprensión y producción | 15 | verificado | 3°M Ing INGL OAC 03 |
<!-- fin:cobertura -->

### Pendientes de verificación

<!-- inicio:pendientes -->
- **LE01 OA 04** (leer palabras aisladas y en contexto, aplicando la correspondencia letra-sonido …): aparece en el eje Lectura de 1° básico (texto «Leo Primero»), pero no se pudo confirmar su redacción.
- **LE01 OA 08** (demostrar comprensión de narraciones: información explícita, secuencia de accion…): aparece en el eje Lectura de 1° básico (texto «Leo Primero»), pero no se pudo confirmar su redacción.
- **LE02 OA 21** (escribir correctamente para facilitar la comprensión del lector: ce-ci, que-qui,…): la lista de contenidos ortográficos apareció junto a otro código en la fuente; falta confirmar que el número sea 21.
- **LE06 OA 21** (utilizar correctamente los participios irregulares (roto, abierto, dicho, escrit…): el número y el tema (participios irregulares) salen de un documento secundario; falta confirmarlos en una página oficial.
- **EN01 OA 13** (escribir (copiar o completar) palabras y oraciones simples de acuerdo a un model…): las páginas del Mineduc sobre la propuesta curricular de Inglés de 1° básico se contradicen en qué eje corresponde a cada número; conviene revisar el PDF oficial.
- **EN02 OA 13** (escribir (copiar o completar) palabras y oraciones simples de acuerdo a un model…): no se pudo confirmar su redacción en una página oficial; se supuso igual al OA 13 de 3° y 4° básico, que sí está verificado.
<!-- fin:pendientes -->

Mientras estén pendientes, el juego los muestra con la etiqueta «Código por verificar» en el árbol.

### Qué falta para cubrir los cursos completos

El banco cubre objetivos centrales de cada asignatura de 1° a 8° básico: Números (Matemática), Lectura y
Escritura (Lenguaje), los tres ejes de Ciencias Naturales y Comprensión oral, Comprensión de lectura y Expresión
escrita (Inglés). Faltan, por ejemplo, Geometría, Medición y Datos en Matemática, Comunicación oral en Lenguaje,
más OA por curso en Ciencias e Inglés, e Historia. Para agregar un OA: registrarlo en `herramientas/objetivos.py`
con su código oficial y fuente, escribir su generador (mínimo 15 desafíos, al menos 3 por nivel; `herramientas/autor.py`
ayuda a escribirlos a mano) y volver a correr `generar.py`, `validar.py` y `documentar.py`.
