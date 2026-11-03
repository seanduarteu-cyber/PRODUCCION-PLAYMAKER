-- =====================================================================================
-- 16A · FICHAS (Supabase de Fichas: jvgifibnoigpicwklasw) · Prendas sin nombre ni número
-- =====================================================================================
-- Permite guardar personas que llevan solo talla (camisetas sin nombre ni número).
-- Quita ÚNICAMENTE la regla que exigía nombre, número o nombre estampado en cada persona.
-- Las demás reglas de la tabla quedan igual. No cambia ni borra datos.
-- Se corre una vez en: Supabase de FICHAS → SQL Editor → pegar todo → Run.

do $$
declare r record;
begin
  for r in
    select conname
    from pg_constraint
    where conrelid = 'public.fichas_detalle'::regclass
      and contype = 'c'
      and pg_get_constraintdef(oid) ~* 'nombre'
      and pg_get_constraintdef(oid) ~* 'numero'
  loop
    execute format('alter table public.fichas_detalle drop constraint %I', r.conname);
  end loop;
end $$;

notify pgrst, 'reload schema';

-- Resultado: debe decir «ok» (y abajo, las reglas que siguen vigentes)
select case when exists (
         select 1 from pg_constraint
         where conrelid = 'public.fichas_detalle'::regclass and contype = 'c'
           and pg_get_constraintdef(oid) ~* 'nombre' and pg_get_constraintdef(oid) ~* 'numero')
       then 'revisar: sigue la regla' else 'ok' end as resultado,
       (select string_agg(conname || ': ' || pg_get_constraintdef(oid), E'\n')
        from pg_constraint where conrelid = 'public.fichas_detalle'::regclass and contype = 'c') as reglas_que_siguen;
