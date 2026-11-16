-- SQL 21B · base de VENTAS (nnisdusdujcpkrbjqnhe) · SQL Editor → New query → pegar todo → Run
-- Requiere el SQL 21A. Gastos en NETO y pagos a socios como remuneración.
--
-- 1) Neto de cada gasto. Los gastos se ingresan con impuestos; el neto es el monto sin el IVA que se recupera:
--      con FACTURA AFECTA → neto = monto ÷ 1,19 (el IVA es crédito fiscal)
--      con boleta, factura exenta, honorarios o sin documento → neto = monto (no hay IVA que recuperar)
--    Qué documento tiene cada gasto se toma, en este orden: lo que se marcó en el gasto → el tipo de documento
--    del proveedor (Gastos › Proveedores) → el IVA habitual de la cuenta (SUPUESTO, hasta cruzarlo con el libro
--    de compras en la Fase 3). Vista nueva v_gastos_neto; la usan Ventas y el Costeo de Planificación.
-- 2) Pagos a socios: cuenta nueva 5.10 «Remuneración de socios» (gasto general de administración). La cuenta
--    F.06 pasa a llamarse «Retiros de socios» (fuera del resultado). Los gastos de la categoría REMUNERACIÓN DE
--    SOCIOS que estaban en F.06 pasan a 5.10 (queda en la auditoría). Al ingresar un pago a un socio, Ventas
--    pregunta qué es: remuneración, reembolso con respaldo, gasto personal o retiro.
--
-- LO ÚNICO QUE TOCA DE LO QUE YA EXISTE: tablas del SQL 21A (plan_cuentas: columna iva_recuperable, cuenta 5.10 y
-- nombre de F.06; gasto_clasif: columna documento y los gastos de remuneración de socios; gasto_cuenta_alias y
-- el motivo de la regla de pagos a Sean Duarte). No toca gastos, proveedores, pedidos ni nada más de Ventas.
-- Una sola transacción: si algo falla, no queda ningún cambio. Se puede volver a correr.

begin;

do $$
begin
  if to_regclass('public.plan_cuentas') is null or to_regclass('public.gasto_clasif') is null
     or not exists (select 1 from information_schema.columns where table_schema = 'public' and table_name = 'plan_cuentas' and column_name = 'devengo_servicio') then
    raise exception 'Falta el SQL 21A en esta base (o no es la base de VENTAS). No se cambió nada.';
  end if;
  if to_regclass('public.v_gastos_neto') is not null and not exists (
       select 1 from information_schema.columns where table_schema = 'public' and table_name = 'v_gastos_neto' and column_name = 'iva_recuperable') then
    raise exception 'Ya existe «v_gastos_neto» en esta base y no es del SQL 21B. No se cambió nada: avisar antes de seguir.';
  end if;
end $$;

-- ── 1. IVA habitual de cada cuenta (supuesto) y documento de cada gasto ─────────────────────────────────
alter table public.plan_cuentas add column if not exists iva_recuperable boolean;   -- habitualmente con factura afecta
alter table public.gasto_clasif add column if not exists documento text;            -- lo marcado en el gasto (manda)
alter table public.gasto_clasif drop constraint if exists gasto_clasif_documento;
alter table public.gasto_clasif add constraint gasto_clasif_documento
  check (documento is null or documento in ('afecta', 'exenta', 'boleta', 'honorarios', 'sin_documento'));

-- solo las cuentas que todavía no lo tienen definido (no pisa lo que se cambie desde Ventas)
update public.plan_cuentas set iva_recuperable = codigo in (
    '1.02', '2.01', '2.03', '2.04', '2.05', '2.06', '2.07', '2.08', '2.10', '3.06', '3.08', '3.10', '4.04', '5.05', 'F.02', 'F.03')
 where iva_recuperable is null;

-- ── 2. Pagos a socios ──────────────────────────────────────────────────────────────────────────────────
insert into public.plan_cuentas (codigo, nombre, nivel, tipo, prorrateo, devengo_servicio, es_activo, activa, orden, supuesto, que_entra, iva_recuperable)
values ('5.10', 'Remuneración de socios', '5', 'fijo', null, true, false, true, 510, null,
        'Abonos a Sean Duarte y Silvia Urbina como remuneración por su trabajo en la empresa. Reembolsos con respaldo van a la cuenta del gasto; gastos personales y retiros, fuera del resultado.', false)
on conflict (codigo) do nothing;
update public.plan_cuentas
   set nombre = 'Retiros de socios', actualizado_por = 'SQL 21B', updated_at = now(),
       que_entra = 'Retiro de utilidades u otro dinero entregado a un socio que no es remuneración, reembolso ni gasto personal. Fuera del resultado.'
 where codigo = 'F.06' and nombre = 'Pagos a socios';
update public.gasto_cuenta_alias set cuenta_codigo = '5.10', actualizado_por = 'SQL 21B', updated_at = now()
 where public.gasto_norm(categoria) = 'REMUNERACION DE SOCIOS' and cuenta_codigo = 'F.06';
insert into public.gasto_cuenta_alias (categoria, cuenta_codigo, revisar)
select pc.nombre, pc.codigo, false from public.plan_cuentas pc
 where pc.codigo in ('5.10', 'F.06')
   and not exists (select 1 from public.gasto_cuenta_alias a where public.gasto_norm(a.categoria) = public.gasto_norm(pc.nombre));
update public.gasto_reglas
   set motivo = 'Pago a socio: ¿remuneración, reembolso con respaldo, gasto personal o retiro?', updated_at = now()
 where tipo = 'proveedor' and proveedor = 'SEAN DUARTE' and creada_por = 'sistema'
   and motivo = 'Pago a socio: ¿gasto de la empresa, reembolso con respaldo o retiro?';

-- los gastos de la categoría REMUNERACIÓN DE SOCIOS que ya estaban en «Pagos a socios» (F.06) pasan a 5.10
create temporary table sql21b_movidos on commit drop as
select c.gasto_id from public.gasto_clasif c join public.gastos g on public.gasto_num(to_jsonb(g) ->> 'id')::bigint = c.gasto_id
 where c.cuenta_codigo = 'F.06' and c.estado = 'clasificado' and public.gasto_norm(to_jsonb(g) ->> 'categoria') = 'REMUNERACION DE SOCIOS';
update public.gasto_clasif c
   set cuenta_codigo = '5.10', actualizado_por = 'SQL 21B', updated_at = now(),
       motivo = 'Remuneración de socios (SQL 21B: antes «Pagos a socios»)'
 where c.gasto_id in (select gasto_id from sql21b_movidos) and c.origen not in ('alias', 'regla');
-- los automáticos y las sugerencias de los que siguen en revisión se recalculan con la traducción nueva
select public.gasto_reclasificar('SQL 21B');

-- ── 3. Neto de cada gasto ──────────────────────────────────────────────────────────────────────────────
create or replace view public.v_gastos_neto as
with g as (
  select public.gasto_num(to_jsonb(x) ->> 'id')::bigint as gasto_id, public.gasto_fecha(to_jsonb(x) ->> 'fecha') as fecha,
         coalesce(public.gasto_num(to_jsonb(x) ->> 'monto'), 0) as monto, to_jsonb(x) ->> 'proveedor' as proveedor
    from public.gastos x),
pv as (
  select distinct on (public.gasto_norm(p.nombre)) public.gasto_norm(p.nombre) as n, p.tipo_documento
    from public.proveedores p where coalesce(p.tipo_documento, '') <> ''
   order by public.gasto_norm(p.nombre), public.gasto_num(to_jsonb(p) ->> 'id') desc),
iva as (select coalesce((select public.gasto_num(valor #>> '{}') from public.gestion_parametros where clave = 'tasa_iva'), 0.19) as t),
d as (
  select g.*, c.cuenta_codigo, c.estado, pc.nivel,
         coalesce(c.periodo_devengo, date_trunc('month', g.fecha)::date) as periodo,
         coalesce(c.documento, pv.tipo_documento) as documento,
         case when c.documento is not null then 'gasto' when pv.tipo_documento is not null then 'proveedor' else 'cuenta' end as origen_iva,
         case when coalesce(c.documento, pv.tipo_documento) is not null then coalesce(c.documento, pv.tipo_documento) = 'afecta'
              else coalesce(pc.iva_recuperable, false) end as iva_recuperable
    from g left join public.gasto_clasif c on c.gasto_id = g.gasto_id
           left join public.plan_cuentas pc on pc.codigo = c.cuenta_codigo
           left join pv on pv.n = public.gasto_norm(g.proveedor))
select d.gasto_id, d.fecha, d.periodo, d.cuenta_codigo, d.nivel, d.estado, d.documento, d.origen_iva, d.iva_recuperable,
       d.monto as monto_bruto,
       case when d.iva_recuperable then round(d.monto / (1 + iva.t)) else d.monto end as monto_neto,
       case when d.iva_recuperable then d.monto - round(d.monto / (1 + iva.t)) else 0 end as iva_credito
  from d, iva;

grant select on public.v_gastos_neto to anon, authenticated;

notify pgrst, 'reload schema';

commit;

-- Revisión: debe decir «SQL 21B listo»
select 'SQL 21B listo' as estado,
       (select count(*) from public.gasto_clasif where cuenta_codigo = '5.10') as en_remuneracion_de_socios,
       (select count(*) from public.gasto_clasif where cuenta_codigo = 'F.06') as en_retiros_de_socios,
       (select count(*) from public.plan_cuentas where iva_recuperable) as cuentas_con_iva_recuperable,
       (select sum(monto_bruto) from public.v_gastos_neto) as total_bruto,
       (select sum(monto_neto) from public.v_gastos_neto) as total_neto,
       (select sum(iva_credito) from public.v_gastos_neto) as iva_credito,
       (select diferencia from public.v_gastos_conciliacion) as diferencia_conciliacion;
