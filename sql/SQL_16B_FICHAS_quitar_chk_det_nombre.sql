-- =====================================================================================
-- 16B · FICHAS (Supabase de Fichas: jvgifibnoigpicwklasw) · Quitar la regla chk_det_nombre
-- =====================================================================================
-- La base rechaza personas sin nombre por la regla «chk_det_nombre». Este SQL la quita
-- (y también cualquier regla que exija nombre o número), muestra cómo era y las reglas que
-- quedan. No cambia ni borra datos. Supabase de FICHAS → SQL Editor → pegar todo → Run.

create temp table _reglas_quitadas as
  select conname as regla, pg_get_constraintdef(oid) as condicion
  from pg_constraint
  where conrelid = 'public.fichas_detalle'::regclass and contype = 'c'
    and (conname = 'chk_det_nombre'
         or (pg_get_constraintdef(oid) ~* 'nombre' and pg_get_constraintdef(oid) ~* 'numero'));

do $$
declare r record;
begin
  for r in select regla from _reglas_quitadas loop
    execute format('alter table public.fichas_detalle drop constraint %I', r.regla);
  end loop;
end $$;

notify pgrst, 'reload schema';

-- Resultado: «ok», qué se quitó y qué reglas siguen (mándame una captura de esto)
select 'ok' as resultado,
       (select string_agg(regla || ': ' || condicion, E'\n') from _reglas_quitadas) as reglas_quitadas,
       (select string_agg(conname || ': ' || pg_get_constraintdef(oid), E'\n')
          from pg_constraint where conrelid = 'public.fichas_detalle'::regclass and contype = 'c') as reglas_que_siguen;
