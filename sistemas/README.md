# Sistemas Playmaker

Código fuente de los sistemas web. Cada carpeta se publica en Netlify arrastrando un zip **plano** (los archivos en la raíz del zip, sin la carpeta).

| Carpeta | Sitio en Netlify | Base de datos (Supabase) | Qué va en el zip |
|---|---|---|---|
| `produccion/` | planificacion-playmaker | Producción `ygcsqrylpibhofvetdyh` | `index.html`, `sistemas.html`, `sw.js`, `manifest.webmanifest`, los 4 íconos `.png` y la carpeta `guias/` (95 guías de tallas) |
| `panel-fichas/` | panel-fichas-playmaker | Fichas `jvgifibnoigpicwklasw` | `index.html` |
| `ingreso-fichas/` | ingreso-fichas-playmaker (sitio del cliente) | Fichas `jvgifibnoigpicwklasw` | `index.html` |
| `ventas/` | ventas-playmaker | Ventas `nnisdusdujcpkrbjqnhe` | `index.html` |

- **Página principal:** `https://planificacion-playmaker.netlify.app/sistemas.html`. Ahí se hace el ingreso único (usuario de Planificación). Fichas y Ventas reciben la sesión desde ahí.
- **Detalle de cambios:** `HISTORIAL.txt` (lista de cambios), `LEEME_acceso_unico.txt`, `LEEME_velocidad.txt`, `LEEME_costeo.txt` y `LEEME_clasificacion_gastos.txt` (incluye cómo crear la función de Claude).

## Pendiente: respaldos y seguridad

`PENDIENTE_respaldos_y_seguridad.txt`: análisis de riesgos (llave pública con acceso total, respaldos, cuentas) y plan propuesto. En pausa hasta que se pida retomarlo.

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
| `SQL_20A_PRODUCCION_costeo_prendas.sql` | Producción | Costeo de prendas: tablas `plan_costeo` (por molde: kilos de tela y merma del corte, metros de ploteo, otros costos) y `plan_insumos_molde` (consumo de insumos por prenda, por molde y común). Detalle: `LEEME_costeo.txt`. |
| `SQL_21A_VENTAS_clasificacion_gastos.sql` | Ventas | Clasificación de gastos (Fase 1 del costeo): plan de cuentas, traducción de las categorías actuales, reglas, dato original inmutable (`gasto_raw`), clasificación (`gasto_clasif`), parámetros, auditoría y conciliación; clasifica los gastos que ya existen. Detalle: `LEEME_clasificacion_gastos.txt`. |
| `SQL_21B_VENTAS_neto_y_socios.sql` | Ventas | Requiere el 21A. Neto de cada gasto (vista `v_gastos_neto`: sin el IVA de la factura afecta, según el documento del gasto, del proveedor o el habitual de la cuenta) y pagos a socios: cuenta 5.10 «Remuneración de socios» y F.06 «Retiros de socios». Lo usa el gasto general del Costeo. |
| `SQL_21C_VENTAS_claude_sugiere_cuenta.sql` | Ventas | Requiere 21A y 21B. Claude sugiere la cuenta de un gasto: registro de consultas con su costo (`gasto_ia_consultas`), tope diario y el contexto que lee Claude; solo lo usa la función `sugerir-cuenta` de Supabase (`ventas/funciones/sugerir-cuenta/index.ts`, se crea en Edge Functions con el secreto `ANTHROPIC_API_KEY`). |
| `SQL_24C_VENTAS_cuenta_habitual_clasifica.sql` | Ventas | Requiere el 21A. La cuenta habitual del proveedor clasifica sola los gastos nuevos (regla → categoría → cuenta habitual → revisión; origen `proveedor`, no para socios) y se aplica a lo que sigue en revisión. Lo elegido por una persona no cambia. Se puede volver a correr (y después de un 21A). |
| `SQL_22A_FICHAS_revisar_ingreso_SOLO_LECTURA.sql` | Fichas | Solo lee: por qué un pedido no puede ingresar a producción (tallas por prenda, diseño aprobado, fecha, ficha confirmada y personas sin molde para su calce). Se cambia el texto a buscar en la línea marcada. |
| `SQL_23A_PRODUCCION_precios_por_proveedor.sql` | Producción | Precios por proveedor (Costeo › Precios): tablas `plan_insumo_precios` (cada producto con cada proveedor: precio sin IVA, presentación, ancho, gramaje, rendimiento, metros del rollo, cc del envase) y `plan_proveedores_estado` (proveedores desactivados para el costeo). Copia los precios actuales con su proveedor; no cambia ni borra datos. Se puede volver a correr. |
| `SQL_23C_PRODUCCION_estampado_aplicaciones.sql` | Producción | Costeo › Estampado y aplicaciones: el registro de costeo acepta ESTAMPADO y agrega `insumo_id`, `cantidad` (por prenda) y `bajadas` (de plancha por prenda) a `plan_costeo`. Si la base limita las categorías de insumos, agrega «Aplicación» (con todas las que ya están en uso). No cambia ni borra datos. Se puede volver a correr. |
| `SQL_23B_PRODUCCION_piezas_de_cada_tela.sql` | Producción | Simular costo: agrega la columna `piezas` al registro del corte (`plan_costeo`): qué piezas llevaba cada tela, para aprender qué parte de la prenda es cada pieza. No cambia ni borra datos. Se puede volver a correr. |
| `SQL_17C_FICHAS_revisar_moldes_SOLO_LECTURA.sql` | Fichas | Solo revisa: compara los 104 moldes del catálogo del 18-11-2026 con la tabla moldes (falta, desactivado, código o sección distinta). |
| `SQL_17D_FICHAS_orden_catalogo_completo.sql` | Fichas | (Reemplazado por el 25A.) Catálogo completo de noviembre: orden y sección de los 95 moldes. |
| `SQL_25A_FICHAS_catalogo_18_11_moldes_nuevos.sql` | Fichas | Catálogo del 18-11-2026 (104 moldes): agrega 85 a 93 (FUT-SH femenino e infantil, vóley 87 y 88, calza larga 89, buzo 90 y Running y atletismo 91 a 93) y pone el orden y la sección de los 104. No cambia los moldes que ya existen ni las fichas. Se puede volver a correr. |

Los SQL 1A a 14A se corrieron antes y no están en este repositorio.

## Catálogo de moldes (`../catalogo/`)

- `Catalogo_ordenado_INDEXADO_18_11.pdf`: el catálogo del 18-11-2026 (104 moldes, 113 páginas) con su índice en la página 1 (un enlace por molde y el tipo de manga).
- `Indice_catalogo_ordenado_18_11.xlsx`: el mismo índice en planilla (orden, sección, N°, código, calce, manga, tallas, página, guía; los nuevos en verde).
- Guías de tallas: `produccion/guias/molde-NN.jpg`, una por molde (104), sacadas del catálogo del 18-11. Se publican con el sitio de Planificación y las usan los tres sistemas; un molde nuevo, fuera del catálogo, usa la que se sube en el panel (Storage).
- En los sistemas, el orden y la sección de cada molde vienen de la tabla `moldes` de Fichas (columnas `orden` y `deporte`, SQL 17A). Los especiales (E01…) van en la sección de su deporte, pero se siguen ofreciendo con cualquier deporte; Multideporte y Salida y entrenamiento también. Detalle: `LEEME_catalogo.txt`.

## Pruebas (`../pruebas/`)

Las pruebas usan Playwright con las bases simuladas: no tocan Supabase ni Netlify. `clasif_gastos.test.js` necesita además un Postgres local (ver el comienzo del archivo). Desde `pruebas/` se corren con `node <archivo>`; la ruta de Playwright está fija en `comun_movil.js` y en cada prueba.

| Prueba | Qué revisa |
|---|---|
| `acceso.test.js` | Ingreso único, permisos por perfil y cerrar sesión. |
| `ventas_rapido.test.js` | Carga liviana de Ventas; que ningún guardado pierda un comprobante. |
| `estado.test.js` | Pestaña «Estado» y pendientes que vuelven a Armado y Corte juntos. |
| `estampado.test.js` | Costeo: aplicaciones del estampado al terminar Estampado (precargadas desde la ficha), «No lleva aplicaciones», costeo del pedido con aplicaciones y bajadas de plancha, aviso si falta, edición y stock, y en Simular costo. Usa `base_simulada.js` (base con estado). |
| `precios_proveedor.test.js` | Costeo: precios por proveedor (el más caro de los activos, desactivar proveedor y producto, proveedor nuevo creado en Ventas, tela por ancho y gramaje, papel por rollo, compras), las 4 tintas en Ploteo y margen y Simular costo (tela por pieza, gramaje, confección, ploteo, gasto general y precio sugerido). |
| `reingreso.test.js` | Planificación: devolver un pedido terminado o en curso a una etapa anterior (qué se rehace, validaciones, fecha también en la ficha, detalle ya borrado, marca de reingreso y cumplimiento en Gerencia), con una base simulada que guarda los cambios. |
| `pedido_cliente.test.js` | Sitio del cliente: basta con la talla, lista pegada desde Excel (columnas), cada prenda con su lista, sin arquero, medias por pares. |
| `pedido_panel.test.js` | Panel y Planificación: medias por diseño con pares por talla y hoja propia, sin arquero ni número obligatorio. |
| `catalogo.test.js` | Catálogo ordenado en el panel y en Planificación: orden, secciones, 83 y 84, moldes ya elegidos; con y sin el SQL 17A, y sin conexión. |
| `moldes_despiece.test.js` | Despiece de moldes: botón en el inicio del panel, resumen del despiece en Planificación › Moldes y botón que abre el panel en el molde, lo guarda y vuelve a Planificación. |
| `cambiar_molde.test.js` | Panel: cambiar el molde de un diseño sin perder personas, montajes ni ficha técnica. |
| `calces_diseno.test.js` | Un diseño con varios calces, unir diseños, aviso de calce sin molde (Planificación) y copiar la configuración de telas. |
| `costeo.test.js` | Costeo en Planificación, por molde: kilos de cada molde y tela en el corte, metros de cada molde en el ploteo, costo total y por prenda de cada molde, gasto general desde la clasificación de Ventas (neto, cada mes y 3 meses anteriores), consumo por molde. |
| `clasif_gastos.test.js` | Clasificación de gastos de punta a punta **contra un Postgres local** (corre los SQL 21A, 21B y 21C y atiende la página con psql): reglas, dato original inmutable, sugerencias, Revisión, Plan, Reglas, Proveedores, Conciliación, neto y socios, Claude (formulario, Revisión y prueba de precisión, con la función simulada) y Ventas sin los SQL. |
| `proveedores_aprenden.test.js` | Gastos › Proveedores **contra un Postgres local** (SQL 21A, 21B y 24C): «Según sus gastos», «Completar con lo que dicen los gastos» (cuenta habitual, reglas por palabra, tipo de documento; solo lo marcado), lo que sale de Revisión, gastos nuevos clasificados por la cuenta habitual, formulario y celular. |
| `sugerir_cuenta.test.mjs` | La función `sugerir-cuenta` en Node con el SDK oficial de Anthropic (Anthropic simulado, Supabase atendido por Postgres local): qué se envía, respuesta obligada a una cuenta del plan, registro y costo, tope diario y errores. Requiere `SDK` (carpeta de `@anthropic-ai/sdk` 1.8.0) y `PGBASE` (base con los SQL 21A–21C). |
| `ventas_movil.js`, `fichas_movil.js`, `plan_movil.js` | Revisión en tamaño celular: que nada quede cortado. |

`tiempos.js` y `tiempos_ventas.js` comparan con la versión anterior, que esperan en `pruebas/antes/`. Esa versión se saca del historial de git.
