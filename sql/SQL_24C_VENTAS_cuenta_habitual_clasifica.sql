-- SQL 24C · base de VENTAS (nnisdusdujcpkrbjqnhe) · SQL Editor → New query → pegar todo → Run
-- Requiere el SQL 21A. La cuenta habitual del proveedor clasifica sola los gastos nuevos.
--
-- Hasta ahora la base clasificaba sola un gasto nuevo (los que entran por el formulario o por «Sincronizar Sheets»)
-- con las reglas y con la traducción de su categoría; la cuenta habitual del proveedor solo se usaba en el
-- formulario. Desde este SQL, el orden es:
--   1. Reglas (las de palabra, las de proveedor y las de proveedor + palabra, también las aprendidas de los gastos).
--   2. La traducción de su categoría, cuando es clara.
--   3. NUEVO: la cuenta habitual del proveedor (Gastos › Proveedores) → el gasto queda CLASIFICADO, con origen
--      «Cuenta habitual del proveedor». No se usa con los socios (siguen pidiendo qué es el pago).
--   4. Si nada de lo anterior: a Revisión.
-- Las compras de inversión bajo el umbral siguen yendo a Revisión, como antes.
-- La cuenta se puede cambiar después: una cuenta elegida por una persona nunca se pisa.
--
-- Al final aplica esto a los gastos que siguen en revisión y muestra cuántos quedaron clasificados.
-- No cambia los gastos ya clasificados por una persona ni los que se clasificaron por su categoría.
-- Todo o nada. Se puede volver a correr. Si algún día se vuelve a correr el SQL 21A, correr después este de nuevo.

begin;

do $$
begin
  if to_regclass('public.gasto_clasif') is null or to_regprocedure('public.gasto_clasificar_auto(jsonb)') is null
     or not exists (select 1 from information_schema.columns
                     where table_schema = 'public' and table_name = 'proveedores' and column_name = 'cuenta_codigo') then
    raise exception 'Falta el SQL 21A (clasificación de gastos) o no es la base de VENTAS. No se cambió nada.';
  end if;
end $$;

-- ── 1. Origen nuevo: «proveedor» (cuenta habitual del proveedor) ───────────────────────────────────────
do $$
declare c record;
begin
  for c in select conname from pg_constraint
            where conrelid = 'public.gasto_clasif'::regclass and contype = 'c'
              and pg_get_constraintdef(oid) like '%origen%' and pg_get_constraintdef(oid) like '%alias%' loop
    execute format('alter table public.gasto_clasif drop constraint %I', c.conname);
  end loop;
end $$;
alter table public.gasto_clasif add constraint gasto_clasif_origen
  check (origen is null or origen in ('alias', 'regla', 'historial', 'manual', 'ia', 'proveedor'));

-- ── 2. Clasificación automática: regla → categoría → cuenta habitual del proveedor → revisión ───────────
create or replace function public.gasto_clasificar_auto(j jsonb)
returns table (cuenta text, origen text, regla bigint, estado text, motivo text, sugerencia text)
language plpgsql stable set search_path = public as $$ -- SQL21A · SQL24C
declare
  d text := gasto_norm(j ->> 'descripcion');
  p text := gasto_norm(j ->> 'proveedor');
  c text := gasto_norm(j ->> 'categoria');
  m numeric := gasto_num(j ->> 'monto');
  r record; a record; umbral numeric; hab text;
begin
  select g.* into r from gasto_reglas g
   where g.activa and (
     (g.tipo = 'palabra' and gasto_palabra(d, g.palabra)) or
     (g.tipo = 'proveedor' and gasto_prov_calza(p, g.proveedor)) or
     (g.tipo = 'proveedor_palabra' and gasto_prov_calza(p, g.proveedor) and gasto_palabra(d, g.palabra)))
   order by g.prioridad, g.id limit 1;
  select al.cuenta_codigo, al.revisar, al.nota into a from gasto_cuenta_alias al where gasto_norm(al.categoria) = c limit 1;
  -- cuenta habitual del proveedor (no socios)
  if p <> '' then
    select pv.cuenta_codigo into hab
      from proveedores pv join plan_cuentas pc on pc.codigo = pv.cuenta_codigo and pc.activa
     where gasto_norm(pv.nombre) = p and not coalesce(pv.es_socio, false)
     order by pv.id desc limit 1;
  end if;
  if r.id is not null and r.accion = 'clasificar' then
    cuenta := r.cuenta_codigo; origen := 'regla'; regla := r.id; estado := 'clasificado'; motivo := r.motivo; sugerencia := null;
  elsif r.id is not null then
    cuenta := null; origen := 'regla'; regla := r.id; estado := 'revision'; motivo := r.motivo;
    sugerencia := coalesce(r.cuenta_codigo, hab, a.cuenta_codigo);
  elsif a.cuenta_codigo is not null and not a.revisar then
    cuenta := a.cuenta_codigo; origen := 'alias'; regla := null; estado := 'clasificado'; motivo := null; sugerencia := null;
  elsif hab is not null then
    cuenta := hab; origen := 'proveedor'; regla := null; estado := 'clasificado'; motivo := 'Cuenta habitual del proveedor'; sugerencia := null;
  else
    cuenta := null; origen := 'alias'; regla := null; estado := 'revision'; sugerencia := a.cuenta_codigo;
    motivo := coalesce(a.nota, case when c = '' then 'Gasto sin categoría.' else 'Categoría sin traducción: ' || (j ->> 'categoria') || '.' end);
  end if;
  -- inversión bajo el umbral: puede ser gasto (mantención, oficina) o parte de una obra mayor
  if cuenta is not null and exists (select 1 from plan_cuentas pc where pc.codigo = cuenta and pc.es_activo) then
    umbral := coalesce((select gasto_num(gp.valor #>> '{}') from gestion_parametros gp where gp.clave = 'umbral_inversion'), 300000);
    if coalesce(m, 0) < umbral then
      sugerencia := cuenta; cuenta := null; estado := 'revision';
      motivo := 'Bajo el umbral de inversión ($' || replace(to_char(umbral, 'FM999,999,999'), ',', '.') || '): ¿es gasto o parte de una obra mayor?';
    end if;
  end if;
  return next;
end $$;

-- ── 3. Al editar un gasto y al reclasificar: lo automático (también la cuenta habitual) se recalcula ─────
create or replace function public.gasto_registrar() returns trigger
language plpgsql security definer set search_path = public as $$ -- SQL21A · SQL24C
declare j jsonb; gid bigint; rid bigint; op text; x record; ya record;
begin
  begin
    if tg_op = 'DELETE' then j := to_jsonb(old); op := 'baja';
    else j := to_jsonb(new); op := case when tg_op = 'INSERT' then 'alta' else 'edicion' end; end if;
    if tg_op = 'UPDATE' and to_jsonb(old) = to_jsonb(new) then return null; end if;   -- se guardó igual: nada cambió
    gid := gasto_num(j ->> 'id')::bigint;
    rid := gasto_raw_agregar(j, op, null, null);
    if tg_op = 'DELETE' then
      delete from gasto_clasif where gasto_id = gid;
      return null;
    end if;
    select * into ya from gasto_clasif where gasto_id = gid;
    select * into x from gasto_clasificar_auto(j);
    if ya.gasto_id is null then
      insert into gasto_clasif (gasto_id, raw_id, cuenta_codigo, periodo_devengo, origen, regla_id, estado, motivo, sugerencia_codigo, actualizado_por)
      values (gid, rid, x.cuenta, date_trunc('month', gasto_fecha(j ->> 'fecha'))::date, x.origen, x.regla, x.estado, x.motivo, x.sugerencia, 'automático');
    elsif ya.origen in ('alias', 'regla', 'proveedor') then
      -- clasificación automática: se recalcula con el gasto editado
      update gasto_clasif set raw_id = rid, cuenta_codigo = x.cuenta, origen = x.origen, regla_id = x.regla, estado = x.estado,
             motivo = x.motivo, sugerencia_codigo = x.sugerencia, actualizado_por = 'automático', updated_at = now(),
             periodo_devengo = case when date_trunc('month', gasto_fecha(to_jsonb(old) ->> 'fecha'))::date = periodo_devengo
                                    then date_trunc('month', gasto_fecha(j ->> 'fecha'))::date else periodo_devengo end
       where gasto_id = gid;
    else
      update gasto_clasif set raw_id = rid where gasto_id = gid;   -- elegida por una persona: se respeta
    end if;
  exception when others then
    raise warning 'gasto_registrar: %', sqlerrm;
  end;
  return null;
end $$;

create or replace function public.gasto_reclasificar(p_usuario text default null)
returns jsonb language plpgsql security definer set search_path = public as $$ -- SQL21A · SQL24C
declare n_rev integer; n_cambio integer;
begin
  select count(*) into n_rev from gasto_clasif where origen in ('alias', 'regla', 'proveedor');
  with s as (
    select gasto_num(to_jsonb(g) ->> 'id')::bigint as gid, x.*
      from gastos g cross join lateral gasto_clasificar_auto(to_jsonb(g)) x
  )
  update gasto_clasif c
     set cuenta_codigo = s.cuenta, origen = s.origen, regla_id = s.regla, estado = s.estado, motivo = s.motivo,
         sugerencia_codigo = s.sugerencia, actualizado_por = coalesce(p_usuario, 'automático'), updated_at = now()
    from s
   where c.gasto_id = s.gid and c.origen in ('alias', 'regla', 'proveedor')
     and (c.cuenta_codigo, c.origen, c.regla_id, c.estado, c.motivo, c.sugerencia_codigo)
         is distinct from (s.cuenta, s.origen, s.regla, s.estado, s.motivo, s.sugerencia);
  get diagnostics n_cambio = row_count;
  return jsonb_build_object('revisados', n_rev, 'cambiados', n_cambio);
end $$;

revoke all on function public.gasto_reclasificar(text) from public;
grant execute on function public.gasto_reclasificar(text) to anon, authenticated;

-- Ventas sabe que la base ya clasifica con la cuenta habitual
insert into public.gestion_parametros (clave, valor, descripcion, actualizado_por)
values ('clasif_por_proveedor', 'true'::jsonb, 'SQL 24C: la cuenta habitual del proveedor clasifica sola los gastos nuevos', 'SQL 24C')
on conflict (clave) do update set valor = excluded.valor, descripcion = excluded.descripcion, updated_at = now();

notify pgrst, 'reload schema';

-- ── 4. Aplicar a lo que sigue en revisión (no toca lo elegido por una persona) ────────────────────────
select public.gasto_reclasificar('SQL 24C');

select 'SQL 24C listo' as estado,
       (select count(*) from public.proveedores where cuenta_codigo is not null and not coalesce(es_socio, false)) as proveedores_con_cuenta_habitual,
       (select count(*) from public.gasto_clasif where origen = 'proveedor' and estado = 'clasificado') as gastos_por_cuenta_habitual,
       (select count(*) from public.gasto_clasif where estado = 'revision') as siguen_en_revision;

commit;
