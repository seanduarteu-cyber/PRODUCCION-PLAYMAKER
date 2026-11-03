-- =====================================================================================
-- 15A · VENTAS (Supabase de Ventas: nnisdusdujcpkrbjqnhe) · Lista liviana de pedidos
-- =====================================================================================
-- Ventas tardaba en abrir porque cada vez bajaba TODOS los pedidos con sus comprobantes
-- (imágenes y PDF guardados en base64 dentro de los abonos). Esta función entrega los
-- pedidos con todos sus datos, pero sin el archivo del comprobante: cada abono trae
-- tiene_comp (si tiene comprobante) y _i (su posición). El comprobante se trae al tocar «Ver».
--
-- No cambia ni borra ningún dato: solo agrega una función de lectura.
-- Se corre una vez en: Supabase de VENTAS → SQL Editor → pegar todo → Run.
-- (El sistema nuevo funciona igual sin esto, pero sigue lento hasta correrlo.)

create or replace function public.pedidos_livianos(p_offset integer default 0, p_cant integer default 200)
returns jsonb
language sql
stable
set search_path = public
as $$
  select coalesce(jsonb_agg(t.fila order by t.id), '[]'::jsonb)
  from (
    select p.id,
           (to_jsonb(p) - 'abonos') || jsonb_build_object('abonos', coalesce((
             select jsonb_agg(
                      case when jsonb_typeof(a.v) = 'object'
                           then (a.v - 'comp64') || jsonb_build_object(
                                  'tiene_comp', coalesce(a.v ->> 'comp64', '') <> '',
                                  '_i', a.i - 1)
                           else a.v end
                      order by a.i)
             from jsonb_array_elements(
                    case when jsonb_typeof(to_jsonb(p) -> 'abonos') = 'array'
                         then to_jsonb(p) -> 'abonos' else '[]'::jsonb end
                  ) with ordinality as a(v, i)
           ), '[]'::jsonb)) as fila
    from public.pedidos p
    order by p.id
    offset greatest(p_offset, 0)
    limit least(greatest(p_cant, 1), 500)
  ) t;
$$;

grant execute on function public.pedidos_livianos(integer, integer) to anon, authenticated;
notify pgrst, 'reload schema';

-- Prueba (debe mostrar «ok» y cuántos pedidos trae la primera página):
select 'ok' as resultado,
       jsonb_array_length(public.pedidos_livianos(0, 200)) as pedidos_primera_pagina;

-- -------------------------------------------------------------------------------------
-- OPCIONAL · Cuánto pesan hoy los comprobantes (mándame el resultado si quieres el detalle)
-- -------------------------------------------------------------------------------------
-- select count(*)                                                      as pedidos,
--        count(*) filter (where abonos::text like '%"comp64"%')         as pedidos_con_comprobante,
--        pg_size_pretty(sum(pg_column_size(abonos))::bigint)            as peso_abonos,
--        pg_size_pretty(pg_total_relation_size('public.pedidos'))       as peso_total_tabla
-- from public.pedidos;
