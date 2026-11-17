-- SQL 23C · base de PRODUCCIÓN (ygcsqrylpibhofvetdyh) · SQL Editor → New query → pegar todo → Run
-- Costeo › Estampado y aplicaciones: qué aplicaciones lleva cada molde de un pedido (escudo vinilo, texturizado, pro…),
-- cuántas por prenda y cuántas bajadas de plancha. Se registra al terminar Estampado (o desde Costeo).
-- 1) plan_costeo: acepta registros de ESTAMPADO y agrega tres columnas (insumo_id, cantidad por prenda, bajadas por
--    prenda). No cambia ni borra ningún dato.
-- 2) Insumos: la categoría «Aplicación». Solo si la base limita las categorías, la regla se amplía (con todas las que ya
--    están en uso); si no las limita, no se toca nada.
-- Todo o nada. Se puede volver a correr.

begin;

do $$
begin
  if to_regclass('public.plan_costeo') is null or to_regclass('public.plan_insumos') is null then
    raise exception 'Faltan las tablas plan_costeo o plan_insumos (SQL 20A y 5A) o no es la base de PRODUCCIÓN. No se cambió nada.';
  end if;
end $$;

alter table public.plan_costeo add column if not exists insumo_id bigint;
alter table public.plan_costeo add column if not exists cantidad numeric check (cantidad is null or cantidad >= 0);
alter table public.plan_costeo add column if not exists bajadas numeric check (bajadas is null or bajadas >= 0);

-- etapas del registro de costeo: se agrega ESTAMP
do $$
declare c record;
begin
  for c in select conname from pg_constraint
            where conrelid = 'public.plan_costeo'::regclass and contype = 'c' and pg_get_constraintdef(oid) ilike '%etapa%' loop
    execute format('alter table public.plan_costeo drop constraint %I', c.conname);
  end loop;
end $$;
alter table public.plan_costeo add constraint plan_costeo_etapa_check check (etapa in ('CORTE', 'PLOTEO', 'SUBL', 'OTRO', 'ESTAMP'));

-- categoría «Aplicación» de los insumos (solo si hay una regla que limita las categorías)
do $$
declare c record; hubo boolean := false; lista text;
begin
  for c in select conname from pg_constraint
            where conrelid = 'public.plan_insumos'::regclass and contype = 'c' and pg_get_constraintdef(oid) ilike '%categoria%' loop
    execute format('alter table public.plan_insumos drop constraint %I', c.conname);
    hubo := true;
  end loop;
  if hubo then
    select string_agg(quote_literal(x), ', ') into lista from (
      select unnest(array['Tela', 'Elástico', 'Hilo', 'Cierre', 'Etiqueta', 'Embalaje', 'Papel', 'Tinta', 'Aplicación', 'Servicio', 'Otro']) as x
      union select distinct categoria from public.plan_insumos where categoria is not null) t;
    execute format('alter table public.plan_insumos add constraint plan_insumos_categoria_check check (categoria is null or categoria in (%s))', lista);
  end if;
end $$;

notify pgrst, 'reload schema';
commit;

-- Revisión: debe decir «SQL 23C listo»
select 'SQL 23C listo' as estado,
       (select count(*) from public.plan_costeo where etapa = 'ESTAMP') as registros_de_estampado;
