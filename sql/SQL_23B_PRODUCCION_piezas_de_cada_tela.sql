-- SQL 23B · base de PRODUCCIÓN (ygcsqrylpibhofvetdyh) · SQL Editor → New query → pegar todo → Run
-- Costeo › Simular costo: qué piezas llevaba cada tela en cada corte registrado.
-- Agrega UNA columna al registro del corte (plan_costeo.piezas: lista de piezas de esa tela, ej. ["Espalda"]); no cambia
-- ni borra ningún dato. Planificación la llena sola desde la ficha del pedido al registrar el corte, y completa los cortes
-- anteriores mientras su ficha exista. Con eso aprende qué parte de cada prenda es la espalda, el cuello, la entrepierna…
-- Todo o nada. Se puede volver a correr.

begin;

do $$
begin
  if to_regclass('public.plan_costeo') is null then
    raise exception 'Falta la tabla plan_costeo (SQL 20A de costeo) o no es la base de PRODUCCIÓN. No se cambió nada.';
  end if;
end $$;

alter table public.plan_costeo add column if not exists piezas jsonb;

notify pgrst, 'reload schema';
commit;

-- Revisión: debe decir «SQL 23B listo»
select 'SQL 23B listo' as estado,
       (select count(*) from public.plan_costeo where etapa = 'CORTE') as cortes_registrados,
       (select count(*) from public.plan_costeo where etapa = 'CORTE' and piezas is not null) as con_piezas;
