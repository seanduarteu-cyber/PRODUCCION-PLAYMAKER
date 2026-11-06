-- SQL 18A · base de FICHAS (jvgifibnoigpicwklasw) · SOLO LEE: no cambia nada
-- Para el error «new row for relation "fichas_tallas" violates check constraint …» al guardar la ficha COT-2608.
-- Muestra las reglas (check) de la tabla fichas_tallas y el tamaño de la ficha COT-2608, para ver cuál regla la rechaza.
-- SQL Editor → New query → pegar todo → Run → copiar el resultado completo.

select 'Regla: ' || c.conname as que, pg_get_constraintdef(c.oid) as detalle
  from pg_constraint c
 where c.conrelid = 'public.fichas_tallas'::regclass and c.contype = 'c'
union all
select 'Columna: ' || column_name, data_type || coalesce(' (' || character_maximum_length || ')', '')
  from information_schema.columns
 where table_schema = 'public' and table_name = 'fichas_tallas' and column_name in ('items', 'specs', 'imagenes')
union all
select 'COT-2608 · items', json_array_length(items::json) || ' prendas o diseños · ' || length(items::text) || ' caracteres'
  from public.fichas_tallas where ref = 'COT-2608'
union all
select 'COT-2608 · specs', length(specs::text) || ' caracteres'
  from public.fichas_tallas where ref = 'COT-2608'
union all
select 'COT-2608 · imagenes', json_array_length(coalesce(imagenes::json, '[]'::json)) || ' montajes · ' || length(coalesce(imagenes::text, '')) || ' caracteres'
  from public.fichas_tallas where ref = 'COT-2608';
