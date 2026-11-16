-- SQL 22A · base de FICHAS (jvgifibnoigpicwklasw) · SOLO LEE: no cambia nada
-- ¿Por qué un pedido no puede ingresar a producción? Repite, para las fichas que calzan con el texto buscado, los
-- mismos controles que hace Planificación antes de ingresar un pedido:
--   tallas completas (personas con talla por cada prenda vendida) · diseño aprobado · fecha de entrega · ficha
--   confirmada · cada persona con molde para su calce.
-- Para buscar otro pedido, cambiar 'torque' en la línea marcada (puede ser parte del nombre o el N° de pedido).
-- SQL Editor → New query → pegar todo → Run → copiar el resultado completo.

with buscar as (select '%torque%'::text as t),          -- ← texto a buscar
f as (
  select ft.ref, ft.proyecto, ft.cliente, ft.estado, ft.montaje_aprobado, ft.entrega_cliente,
         coalesce(nullif(ft.items::text, '')::jsonb, '[]'::jsonb) as items, coalesce(nullif(ft.specs::text, '')::jsonb, '{}'::jsonb) as specs
    from public.fichas_tallas ft, buscar
   where ft.ref ilike buscar.t or ft.proyecto ilike buscar.t or ft.cliente ilike buscar.t),
d as (
  select fd.ref, coalesce(fd.calce, '') as calce, coalesce(nullif(fd.tallas::text, '')::jsonb, '{}'::jsonb) as tallas
    from public.fichas_detalle fd where fd.ref in (select ref from f)),
it as (
  select f.ref, i ->> 'prenda' as prenda, coalesce((i ->> 'cant')::numeric, 0) as cant
    from f, jsonb_array_elements(case when jsonb_typeof(f.items) = 'array' then f.items else '[]'::jsonb end) i),
asig as (
  select it.ref, it.prenda, it.cant,
         (select count(*) from d where d.ref = it.ref and coalesce(d.tallas ->> it.prenda, '') not in ('', 'false', 'null')) as con_talla
    from it),
sm as (   -- personas con talla en una prenda cuyo diseño no tiene molde para su calce (las medias no llevan molde)
  select d.ref, k.key as prenda, coalesce(nullif(d.calce, ''), 'sin calce') as calce, count(*) as personas,
         bool_or(it.prenda is null) as prenda_fuera
    from d cross join lateral jsonb_each(d.tallas) k
    join f on f.ref = d.ref
    left join it on it.ref = d.ref and it.prenda = k.key
   where coalesce(k.value #>> '{}', '') not in ('', 'false', 'null')
     and regexp_replace(k.key, '_\d+$', '') <> 'medias'
     and (coalesce(f.specs -> k.key -> 'moldes' ->> d.calce, '') = ''
          or (f.specs -> k.key -> 'moldes' ->> d.calce ~ '\|manual$' and btrim(split_part(f.specs -> k.key -> 'moldes' ->> d.calce, '|', 1)) = ''))
   group by 1, 2, 3)
select f.ref as pedido, f.proyecto, f.cliente,
       f.estado as estado_ficha, f.montaje_aprobado as diseno_aprobado, f.entrega_cliente,
       (select sum(cant) from asig a where a.ref = f.ref) as vendidas,
       (select sum(least(con_talla, cant)) from asig a where a.ref = f.ref) as con_talla,
       (select string_agg(prenda || ': ' || least(con_talla, cant) || ' de ' || cant, ' · ' order by prenda) from asig a where a.ref = f.ref) as tallas_por_prenda,
       coalesce((select string_agg(prenda || ' ' || lower(calce) || ': ' || personas || case when prenda_fuera then ' (prenda que ya no está en la ficha)' else '' end, ' · ')
                   from sm where sm.ref = f.ref), '—') as personas_sin_molde,
       concat_ws(' · ',
         case when coalesce((select sum(cant) from asig a where a.ref = f.ref), 0) = 0 then 'la ficha no tiene prendas vendidas'
              when (select sum(least(con_talla, cant)) from asig a where a.ref = f.ref) < (select sum(cant) from asig a where a.ref = f.ref) then 'faltan tallas' end,
         case when f.montaje_aprobado is not true then 'falta aprobar el diseño' end,
         case when f.entrega_cliente is null then 'falta la fecha de entrega' end,
         case when f.estado is distinct from 'confirmado' then 'falta confirmar la ficha (estado: ' || coalesce(f.estado, 'vacío') || ')' end,
         case when exists (select 1 from sm where sm.ref = f.ref) then 'hay personas sin molde para su calce' end) as que_falta
  from f
 order by f.ref;
