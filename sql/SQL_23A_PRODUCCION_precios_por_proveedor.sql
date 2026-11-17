-- SQL 23A · base de PRODUCCIÓN (ygcsqrylpibhofvetdyh) · SQL Editor → New query → pegar todo → Run
-- Precios por proveedor (Planificación › Costeo › Precios). Crea dos tablas nuevas y copia en ellas los precios que
-- ya existen; no cambia ni borra ningún dato existente.
--
-- 1) plan_insumo_precios: cada producto (tela, papel, tinta u otro insumo de Inventario) con cada proveedor que lo
--    vende: su precio sin IVA y cómo viene.
--      presentacion: kg · m · unid · rollo · envase · paquete · litro      contenido: metros del rollo, cc del envase,
--      unidades del paquete · ancho_m y gramaje (g/m²): telas y papel · rendimiento: telas, metros por kg
--    proveedor_id = el proveedor de Ventas (misma lista que los gastos); vacío = escrito a mano, aún sin cruzar.
-- 2) plan_proveedores_estado: proveedores desactivados para el costeo (sus precios dejan de contar).
--
-- El costeo usa, de cada producto, el precio MÁS CARO entre sus proveedores activos. Planificación lo calcula y lo
-- deja en el precio del insumo (plan_insumos.precio), así el resto del sistema sigue igual.
-- Primera vez: cada insumo con precio pasa a tener una línea con su proveedor actual (o «Sin proveedor»). Al papel
-- que se lleva por rollo y a las tintas les faltan los metros del rollo y los cc del envase: se completan en Precios.
-- Todo o nada: si algo falla no queda ningún cambio. Se puede volver a correr.

begin;

do $$
begin
  if to_regclass('public.plan_insumos') is null then
    raise exception 'Falta la tabla plan_insumos (SQL 5A de insumos) o no es la base de PRODUCCIÓN. No se cambió nada.';
  end if;
  if to_regclass('public.plan_insumo_precios') is not null and not exists (
       select 1 from information_schema.columns where table_schema = 'public' and table_name = 'plan_insumo_precios' and column_name = 'presentacion') then
    raise exception 'Ya existe una tabla plan_insumo_precios distinta a la de este SQL. No se cambió nada.';
  end if;
end $$;

create table if not exists public.plan_insumo_precios (
  id bigserial primary key,
  insumo_id bigint not null,                -- plan_insumos.id
  proveedor_id bigint,                      -- proveedores.id de Ventas (vacío: aún sin cruzar)
  proveedor text not null default '',
  nombre_proveedor text,                    -- cómo lo llama el proveedor (opcional)
  presentacion text not null default 'unid' check (presentacion in ('kg', 'm', 'unid', 'rollo', 'envase', 'paquete', 'litro')),
  contenido numeric check (contenido is null or contenido > 0),
  precio numeric check (precio is null or precio >= 0),           -- sin IVA, por presentación
  ancho_m numeric check (ancho_m is null or ancho_m > 0),
  gramaje numeric check (gramaje is null or gramaje > 0),
  rendimiento numeric check (rendimiento is null or rendimiento > 0),
  activo boolean not null default true,
  usuario text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists plan_insumo_precios_insumo on public.plan_insumo_precios (insumo_id);

create table if not exists public.plan_proveedores_estado (
  clave text primary key,                   -- nombre del proveedor en minúsculas, sin tildes ni espacios de más
  nombre text not null,
  proveedor_id bigint,
  activo boolean not null default true,
  usuario text,
  updated_at timestamptz not null default now()
);

-- precios que ya existen: una línea por insumo con precio, con su proveedor (las columnas de precio pueden faltar
-- si el SQL 5A es antiguo: entonces no hay nada que copiar)
do $$
declare
  tiene_precio boolean; tiene_prov boolean; tiene_rend boolean;
begin
  select bool_or(column_name = 'precio'), bool_or(column_name = 'proveedor'), bool_or(column_name = 'rendimiento')
    into tiene_precio, tiene_prov, tiene_rend
    from information_schema.columns where table_schema = 'public' and table_name = 'plan_insumos';
  if coalesce(tiene_precio, false) then
    execute format($q$
      insert into public.plan_insumo_precios (insumo_id, proveedor, presentacion, contenido, precio, rendimiento, usuario)
      select i.id, %s,
             case when i.categoria = 'Tela' then case when i.unidad = 'kg' then 'kg' else 'm' end
                  when i.categoria = 'Tinta' then case when i.unidad = 'litro' then 'litro' else 'envase' end
                  when i.categoria = 'Papel' then case when i.unidad = 'rollo' then 'rollo' else 'm' end
                  when i.unidad in ('kg', 'm', 'unid', 'rollo', 'litro') then i.unidad else 'unid' end,
             -- papel por rollo y tinta por envase: los metros del rollo y los cc se completan en Precios
             case when i.categoria = 'Tinta' or (i.categoria = 'Papel' and i.unidad = 'rollo') then null else 1 end,
             i.precio, %s, 'SQL 23A'
        from public.plan_insumos i
       where i.precio > 0
         and not exists (select 1 from public.plan_insumo_precios p where p.insumo_id = i.id)$q$,
      case when coalesce(tiene_prov, false) then $e$coalesce(nullif(btrim(i.proveedor), ''), 'Sin proveedor')$e$ else $e$'Sin proveedor'$e$ end,
      case when coalesce(tiene_rend, false) then $e$case when i.categoria = 'Tela' and i.rendimiento > 0 then i.rendimiento end$e$ else 'null' end);
  end if;
end $$;

-- mismo acceso que las demás tablas de Planificación (la app entra con la llave pública)
alter table public.plan_insumo_precios enable row level security;
drop policy if exists plan_insumo_precios_todo on public.plan_insumo_precios;
create policy plan_insumo_precios_todo on public.plan_insumo_precios for all to anon, authenticated using (true) with check (true);
grant select, insert, update, delete on public.plan_insumo_precios to anon, authenticated;
grant usage, select on sequence public.plan_insumo_precios_id_seq to anon, authenticated;

alter table public.plan_proveedores_estado enable row level security;
drop policy if exists plan_proveedores_estado_todo on public.plan_proveedores_estado;
create policy plan_proveedores_estado_todo on public.plan_proveedores_estado for all to anon, authenticated using (true) with check (true);
grant select, insert, update, delete on public.plan_proveedores_estado to anon, authenticated;

notify pgrst, 'reload schema';
commit;

-- Revisión: debe decir «SQL 23A listo»
select 'SQL 23A listo' as estado,
       (select count(*) from public.plan_insumo_precios) as precios_por_proveedor,
       (select count(distinct insumo_id) from public.plan_insumo_precios) as productos_con_precio,
       (select count(*) from public.plan_insumo_precios where proveedor = 'Sin proveedor') as sin_proveedor;
