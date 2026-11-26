-- SQL 26A · base de PRODUCCIÓN (ygcsqrylpibhofvetdyh) · SQL Editor → New query → pegar todo → Run
-- Telas de cada pedido. Al ingresar a producción se confirman las telas de cada molde (las que indica la ficha) y su
-- proveedor, con el estimado en kg por prenda sacado de los cortes ya pesados del mismo molde con la misma tela.
-- Lo usan: el corte (las telas sin estimado se pesan obligatoriamente), el stock de telas (se descuenta el estimado y
-- al pesar se reemplaza por lo pesado) y el costeo (precio del proveedor elegido).
-- LO ÚNICO QUE TOCA: agrega la columna «telas» (jsonb) a la tabla planificacion. No cambia datos. Se puede volver a correr.

begin;

do $$
begin
  if to_regclass('public.planificacion') is null then
    raise exception 'No es la base de PRODUCCIÓN (falta la tabla planificacion). No se cambió nada.';
  end if;
end $$;

alter table public.planificacion add column if not exists telas jsonb;
comment on column public.planificacion.telas is
  'Telas confirmadas al ingresar a producción: [{molde, tela, insumo_id, proveedor, prendas, kg_prenda (estimado o null), cortes}]';

notify pgrst, 'reload schema';

commit;

-- Revisión: debe decir «SQL 26A listo»
select case when exists (select 1 from information_schema.columns
                          where table_schema = 'public' and table_name = 'planificacion' and column_name = 'telas')
            then 'SQL 26A listo' else 'NO se aplicó: revisa el error de arriba (¿es la base de Producción?)' end as estado;
