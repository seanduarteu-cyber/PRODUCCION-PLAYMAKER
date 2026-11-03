# Sistemas Playmaker

Código fuente de los sistemas web. Cada carpeta se publica en Netlify arrastrando un zip **plano** (los archivos en la raíz del zip, sin la carpeta).

| Carpeta | Sitio en Netlify | Base de datos (Supabase) | Qué va en el zip |
|---|---|---|---|
| `produccion/` | planificacion-playmaker | Producción `ygcsqrylpibhofvetdyh` | `index.html`, `sistemas.html`, `sw.js`, `manifest.webmanifest` y los 4 íconos `.png` |
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

Los SQL 1A a 14A se corrieron antes y no están en este repositorio.

## Pruebas (`../pruebas/`)

Las pruebas usan Playwright con las bases simuladas: no tocan Supabase ni Netlify. Desde `pruebas/` se corren con `node <archivo>`; la ruta de Playwright está fija en `comun_movil.js` y en cada prueba.

| Prueba | Qué revisa |
|---|---|
| `acceso.test.js` | Ingreso único, permisos por perfil y cerrar sesión. |
| `ventas_rapido.test.js` | Carga liviana de Ventas; que ningún guardado pierda un comprobante. |
| `estado.test.js` | Pestaña «Estado» y pendientes que vuelven a Armado y Corte juntos. |
| `camisetas_sin_numero.test.js` | Camisetas sin nombre ni número en el sitio del cliente. |
| `ventas_movil.js`, `fichas_movil.js`, `plan_movil.js` | Revisión en tamaño celular: que nada quede cortado. |

`tiempos.js` y `tiempos_ventas.js` comparan con la versión anterior, que esperan en `pruebas/antes/`. Esa versión se saca del historial de git.
