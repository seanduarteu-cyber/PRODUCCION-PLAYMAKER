-- SQL 17B · base de FICHAS (jvgifibnoigpicwklasw) · OPCIONAL · correr solo si los moldes 01 al 10 ya no se usan
-- Los moldes 01 al 10 (FUTMUJU01, FUTHOMU01, FUTINMUJU01, FUTINHOMU01, FUTMUJV01, FUTHOMV01, FUTINMUJV01, FUTINHOMV01,
-- FUTMUJCC01, FUTHOMCC01) no aparecen en el catálogo ordenado. Esto los desactiva: dejan de ofrecerse en fichas y pedidos nuevos.
-- No borra nada: las fichas y pedidos que ya los tienen los siguen mostrando.
-- Para volver atrás: el mismo update con activo = true (o «Activar» en Planificación › Configuración › Catálogo).

update public.moldes set activo = false, updated_at = now() where numero between 1 and 10;

select numero, codigo, descripcion, activo from public.moldes where numero between 1 and 10 order by numero;
