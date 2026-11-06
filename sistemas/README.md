# Sistemas Playmaker

Código fuente de los sistemas web. Cada carpeta se publica en Netlify arrastrando un zip **plano** (los archivos en la raíz del zip, sin la carpeta).

| Carpeta | Sitio en Netlify | Base de datos (Supabase) | Qué va en el zip |
|---|---|---|---|
| `produccion/` | planificacion-playmaker | Producción `ygcsqrylpibhofvetdyh` | `index.html`, `sistemas.html`, `sw.js`, `manifest.webmanifest`, los 4 íconos `.png` y la carpeta `guias/` (95 guías de tallas) |
| `panel-fichas/` | panel-fichas-playmaker | Fichas `jvgifibnoigpicwklasw` | `index.html` |
| `ingreso-fichas/` | ingreso-fichas-playmaker (sitio del cliente) | Fichas `jvgifibnoigpicwklasw` | `index.html` |
| `ventas/` | ventas-playmaker | Ventas `nnisdusdujcpkrbjqnhe` | `index.html` |

- **Página principal:** `https://planificacion-playmaker.netlify.app/sistemas.html`. Ahí se hace el ingreso único (usuario de Planificación). Fichas y Ventas reciben la sesión desde ahí.
- **Detalle de cambios:** `HISTORIAL.txt` (lista de cambios), `LEEME_acceso_unico.txt` y `LEEME_velocidad.txt`.

## SQL (`../sql/`)

Se corren una vez en el SQL Editor de la base indicada en cada archivo.

| Archivo | Base | Qué hace |
|---|---|---|
| `SQL_15A_VENTAS_pedidos_livianos.sql` | Ventas | Función `pedidos_livianos`: la lista de pedidos sin los comprobantes en base64 (Ventas abre rápido). |
| `SQL_16A_FICHAS_prendas_sin_nombre_ni_numero.sql` | Fichas | Quita reglas que exigían nombre y número a la vez. |
| `SQL_16B_FICHAS_quitar_chk_det_nombre.sql` | Fichas | Quita `chk_det_nombre`, que exigía nombre en cada persona. |
| `SQL_16C_FICHAS_nombre_hasta_80.sql` | Fichas | Vuelve a poner el tope de 80 caracteres al nombre, que ahora puede ir vacío. |
| `SQL_17A_FICHAS_moldes_orden_del_catalogo.sql` | Fichas | Catálogo ordenado: columna `orden`, deporte = sección del catálogo y moldes nuevos 83 y 84. |
| `SQL_18A_FICHAS_reglas_fichas_tallas_SOLO_LECTURA.sql` | Fichas | Solo lee: reglas (check) de fichas_tallas y tamaño de una ficha. |
| `SQL_18B_FICHAS_ampliar_topes_ficha.sql` | Fichas | Amplía los topes de tamaño de la ficha (specs e imagenes a 200.000 caracteres, items a 20.000): fichas con muchos diseños y montajes. |
| `SQL_19A_FICHAS_descripcion_mangas.sql` | Fichas | Descripción de la manga de cada camiseta según su código: …01 manga clásica, …02 manga raglán, …03 sin mangas. |
| `SQL_19B_FICHAS_E02_codigo_sin_mangas.sql` | Fichas | La E02 (rugby sin mangas) pasa de RB-HOMUCC02 a RB-HOMUCC03 en la tabla de moldes y en las fichas ya guardadas. Se puede correr más de una vez. |
| `SQL_17C_FICHAS_revisar_moldes_SOLO_LECTURA.sql` | Fichas | Solo revisa: compara los 95 moldes del catálogo completo con la tabla moldes (falta, desactivado, código o sección distinta). |
| `SQL_17D_FICHAS_orden_catalogo_completo.sql` | Fichas | Catálogo completo: orden y sección de los 95 moldes (los 01 al 10 al inicio de Fútbol). |

Los SQL 1A a 14A se corrieron antes y no están en este repositorio.

## Catálogo de moldes (`../catalogo/`)

- `Catalogo_ordenado_COMPLETO_INDEXADO.pdf`: el catálogo completo (95 moldes, 105 páginas) con su índice en la página 1 (un enlace por página) y marcadores.
- `Indice_catalogo_ordenado_COMPLETO.xlsx`: el mismo índice en planilla (orden, sección, N°, código, calce, tallas, página, guía).
- Guías de tallas: `produccion/guias/molde-NN.jpg`, una por molde, sacadas del catálogo completo. Se publican con el sitio de Planificación y las usan los tres sistemas; un molde nuevo, fuera del catálogo, usa la que se sube en el panel (Storage).
- En los sistemas, el orden y la sección de cada molde vienen de la tabla `moldes` de Fichas (columnas `orden` y `deporte`, SQL 17A). Los especiales (E01…) van en la sección de su deporte, pero se siguen ofreciendo con cualquier deporte; Multideporte y Salida y entrenamiento también. Detalle: `LEEME_catalogo.txt`.

## Pruebas (`../pruebas/`)

Las pruebas usan Playwright con las bases simuladas: no tocan Supabase ni Netlify. Desde `pruebas/` se corren con `node <archivo>`; la ruta de Playwright está fija en `comun_movil.js` y en cada prueba.

| Prueba | Qué revisa |
|---|---|
| `acceso.test.js` | Ingreso único, permisos por perfil y cerrar sesión. |
| `ventas_rapido.test.js` | Carga liviana de Ventas; que ningún guardado pierda un comprobante. |
| `estado.test.js` | Pestaña «Estado» y pendientes que vuelven a Armado y Corte juntos. |
| `pedido_cliente.test.js` | Sitio del cliente: basta con la talla, lista pegada desde Excel (columnas), cada prenda con su lista, sin arquero, medias por pares. |
| `pedido_panel.test.js` | Panel y Planificación: medias por diseño con pares por talla y hoja propia, sin arquero ni número obligatorio. |
| `catalogo.test.js` | Catálogo ordenado en el panel y en Planificación: orden, secciones, 83 y 84, moldes ya elegidos; con y sin el SQL 17A, y sin conexión. |
| `ventas_movil.js`, `fichas_movil.js`, `plan_movil.js` | Revisión en tamaño celular: que nada quede cortado. |

`tiempos.js` y `tiempos_ventas.js` comparan con la versión anterior, que esperan en `pruebas/antes/`. Esa versión se saca del historial de git.
