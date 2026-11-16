-- SQL 20A · base de PRODUCCIÓN (ygcsqrylpibhofvetdyh) · SQL Editor → New query → pegar todo → Run
-- Costeo de prendas (pestaña «Costeo» de Planificación). Crea dos tablas nuevas; no toca ninguna existente.
--
-- 1) plan_costeo: lo que registra cada área de un pedido
--      CORTE  → una fila por tela del despiece: kg de tela cortada, kg de merma y prendas cortadas
--      PLOTEO → metros ploteados (papel y tinta; el papel de protección de sublimación sale de estos metros)
--      SUBL   → metros de papel de protección, solo si se quieren distintos a los del ploteo
--      OTRO   → otro costo del pedido (concepto y monto: bordado de escudos, medias compradas, despacho…)
-- 2) plan_insumos_molde: lo que lleva UNA prenda de cada insumo (elástico, hilo, cierre, etiqueta, bolsa…)
--      molde = N° del molde (ej: '18', '102' para la E02) o '*' = común a todas las prendas con molde
--
-- Precios: los de Inventario → Insumos. Los demás valores (insumos de papel, tinta y protección, margen y la
-- clasificación de los gastos de Ventas para el gasto general) se guardan en plan_config desde la pestaña Costeo.
-- Se puede volver a correr sin problema.

create table if not exists public.plan_costeo (
  id bigserial primary key,
  planificacion_id bigint not null,
  cot text,
  etapa text not null check (etapa in ('CORTE', 'PLOTEO', 'SUBL', 'OTRO')),
  tela text not null default '',            -- CORTE: la tela · OTRO: el concepto
  kg_cortado numeric check (kg_cortado is null or kg_cortado >= 0),
  kg_merma numeric check (kg_merma is null or kg_merma >= 0),
  prendas integer check (prendas is null or prendas >= 0),
  metros numeric check (metros is null or metros >= 0),
  monto numeric check (monto is null or monto >= 0),
  usuario text,
  nota text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint plan_costeo_unico unique (planificacion_id, etapa, tela)
);
create index if not exists plan_costeo_planificacion on public.plan_costeo (planificacion_id);

create table if not exists public.plan_insumos_molde (
  id bigserial primary key,
  molde text not null,                      -- N° del molde o '*' (común a todas las prendas)
  insumo_id bigint not null,                -- plan_insumos.id
  cantidad numeric not null check (cantidad > 0),   -- por prenda, en la unidad del insumo
  updated_at timestamptz not null default now(),
  constraint plan_insumos_molde_unico unique (molde, insumo_id)
);

-- mismo acceso que las demás tablas de Planificación (la app entra con la llave pública)
alter table public.plan_costeo enable row level security;
drop policy if exists plan_costeo_todo on public.plan_costeo;
create policy plan_costeo_todo on public.plan_costeo for all to anon, authenticated using (true) with check (true);
grant select, insert, update, delete on public.plan_costeo to anon, authenticated;
grant usage, select on sequence public.plan_costeo_id_seq to anon, authenticated;

alter table public.plan_insumos_molde enable row level security;
drop policy if exists plan_insumos_molde_todo on public.plan_insumos_molde;
create policy plan_insumos_molde_todo on public.plan_insumos_molde for all to anon, authenticated using (true) with check (true);
grant select, insert, update, delete on public.plan_insumos_molde to anon, authenticated;
grant usage, select on sequence public.plan_insumos_molde_id_seq to anon, authenticated;

notify pgrst, 'reload schema';

-- Revisión: debe decir «costeo listo»
select 'costeo listo' as estado,
       (select count(*) from public.plan_costeo) as registros_de_costeo,
       (select count(*) from public.plan_insumos_molde) as consumos_por_molde;
