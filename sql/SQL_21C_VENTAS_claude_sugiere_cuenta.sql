-- SQL 21C · base de VENTAS (nnisdusdujcpkrbjqnhe) · SQL Editor → New query → pegar todo → Run
-- Requiere los SQL 21A y 21B. Claude sugiere la cuenta de un gasto (Fase 1b).
--
-- Crea (todo nuevo, no toca ningún dato existente):
--   gasto_ia_consultas   registro de cada consulta a Claude: modelo, cuenta sugerida, confianza, motivo, tokens,
--                        costo en dólares y, en la prueba de precisión, la cuenta que de verdad tiene el gasto
--   gasto_ia_contexto    lo que se le muestra a Claude: plan de cuentas, reglas, ejemplos ya clasificados y los
--                        últimos gastos del mismo proveedor
--   gasto_ia_reservar    anota la consulta y aplica el TOPE DIARIO (100 consultas al día; 800 para la prueba)
--   gasto_ia_completar   guarda la respuesta
--   parámetros: ia_modelo, ia_tope_diario, ia_tope_prueba
-- Las tres funciones solo las puede usar la función «sugerir-cuenta» de Supabase (con la llave de servicio); la
-- página no puede saltarse el tope. La clave de Anthropic va como secreto de la función, nunca en la base.
-- Una sola transacción: si algo falla, no queda ningún cambio. Se puede volver a correr.

begin;

do $$
begin
  if to_regclass('public.v_gastos_neto') is null then
    raise exception 'Faltan los SQL 21A y 21B en esta base (o no es la base de VENTAS). No se cambió nada.';
  end if;
  if to_regclass('public.gasto_ia_consultas') is not null and not exists (
       select 1 from information_schema.columns where table_schema = 'public' and table_name = 'gasto_ia_consultas' and column_name = 'cuenta_sugerida') then
    raise exception 'Ya existe «gasto_ia_consultas» en esta base y no es del SQL 21C. No se cambió nada: avisar antes de seguir.';
  end if;
  if exists (select 1 from pg_proc p join pg_namespace n on n.oid = p.pronamespace
              where n.nspname = 'public' and p.proname in ('gasto_ia_contexto', 'gasto_ia_reservar', 'gasto_ia_completar') and p.prosrc not like '%SQL21C%') then
    raise exception 'Ya existen funciones gasto_ia_… que no son del SQL 21C. No se cambió nada: avisar antes de seguir.';
  end if;
end $$;

create table if not exists public.gasto_ia_consultas (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  modo text not null check (modo in ('sugerir', 'prueba')),
  lote text,                         -- prueba: identifica la corrida
  grupo text,                        -- prueba: «dificil» (proveedor con varias cuentas o sin proveedor) o «facil»
  modelo text not null,              -- el modelo pedido
  modelo_respuesta text,             -- el que respondió
  gasto_id bigint,
  cuenta_real text,                  -- prueba: la cuenta que tiene el gasto
  cuenta_sugerida text,
  confianza numeric,
  motivo text,
  alternativa text,
  input_tokens integer,
  output_tokens integer,
  cache_lectura integer,
  cache_escritura integer,
  costo_usd numeric,
  duracion_ms integer,
  error text,
  usuario text
);
create index if not exists gasto_ia_consultas_fecha on public.gasto_ia_consultas (created_at);
create index if not exists gasto_ia_consultas_lote on public.gasto_ia_consultas (lote);

insert into public.gestion_parametros (clave, valor, descripcion) values
 ('ia_modelo', '"claude-opus-5-5"', 'Modelo de Claude para sugerir la cuenta (se decide con la prueba de precisión).'),
 ('ia_tope_diario', '100', 'Máximo de consultas a Claude por día al ingresar o revisar gastos (C4).'),
 ('ia_tope_prueba', '800', 'Máximo de consultas por día de la prueba de precisión.')
on conflict (clave) do nothing;

-- Lo que lee Claude. Los ejemplos son los 3 gastos clasificados más recientes de cada cuenta (siempre los mismos
-- para todas las consultas, así se reutilizan y cuestan menos); nunca el gasto que se consulta.
create or replace function public.gasto_ia_contexto(p_gasto jsonb) returns jsonb
language sql stable security definer set search_path = public as $$ -- SQL21C
  with gid as (select gasto_num(p_gasto ->> 'id')::bigint as id),
  g as (
    select gasto_num(to_jsonb(x) ->> 'id')::bigint as id, gasto_fecha(to_jsonb(x) ->> 'fecha') as fecha,
           gasto_num(to_jsonb(x) ->> 'monto') as monto, to_jsonb(x) ->> 'descripcion' as descripcion, to_jsonb(x) ->> 'proveedor' as proveedor
      from gastos x),
  cl as (
    select g.*, c.cuenta_codigo from g join gasto_clasif c on c.gasto_id = g.id
     where c.estado = 'clasificado' and c.cuenta_codigo is not null and g.id is distinct from (select id from gid)),
  ej as (
    select cl.*, row_number() over (partition by cl.cuenta_codigo order by cl.fecha desc nulls last, cl.id desc) as n from cl),
  hist as (
    select cl.* from cl where gasto_norm(cl.proveedor) <> '' and gasto_norm(cl.proveedor) = gasto_norm(p_gasto ->> 'proveedor')
     order by cl.fecha desc nulls last, cl.id desc limit 10)
  select jsonb_build_object(
    'cuentas', (select jsonb_agg(jsonb_build_object('codigo', codigo, 'nombre', nombre, 'nivel', nivel, 'que_entra', que_entra) order by orden, codigo)
                  from plan_cuentas where activa),
    'reglas', (select jsonb_agg(jsonb_build_object('tipo', tipo, 'proveedor', proveedor, 'palabra', palabra, 'accion', accion, 'cuenta', cuenta_codigo, 'motivo', motivo) order by prioridad, id)
                 from gasto_reglas where activa),
    'ejemplos', (select jsonb_agg(jsonb_build_object('descripcion', ej.descripcion, 'proveedor', ej.proveedor, 'monto', ej.monto, 'cuenta', ej.cuenta_codigo)
                   order by pc.orden, ej.cuenta_codigo, ej.n)
                   from ej join plan_cuentas pc on pc.codigo = ej.cuenta_codigo where ej.n <= 3 and pc.activa),
    'historial', (select jsonb_agg(jsonb_build_object('fecha', fecha, 'descripcion', descripcion, 'monto', monto, 'cuenta', cuenta_codigo)) from hist),
    'modelo', (select valor #>> '{}' from gestion_parametros where clave = 'ia_modelo'))
$$;

-- Anota la consulta antes de llamar a Claude y aplica el tope del día (hora de Chile)
create or replace function public.gasto_ia_reservar(p_modo text, p_modelo text, p_gasto_id bigint, p_usuario text,
                                                   p_lote text default null, p_grupo text default null, p_cuenta_real text default null)
returns bigint language plpgsql security definer set search_path = public as $$ -- SQL21C
declare tope integer; usados integer; nuevo bigint;
begin
  tope := coalesce(gasto_num((select valor #>> '{}' from gestion_parametros
                               where clave = case when p_modo = 'prueba' then 'ia_tope_prueba' else 'ia_tope_diario' end))::integer,
                   case when p_modo = 'prueba' then 800 else 100 end);
  select count(*) into usados from gasto_ia_consultas
   where modo = p_modo and created_at >= (date_trunc('day', now() at time zone 'America/Santiago') at time zone 'America/Santiago');
  if usados >= tope then
    raise exception 'TOPE_DIARIO: hoy ya se hicieron % consultas (tope %).', usados, tope;
  end if;
  insert into gasto_ia_consultas (modo, modelo, gasto_id, usuario, lote, grupo, cuenta_real)
  values (p_modo, p_modelo, p_gasto_id, p_usuario, p_lote, p_grupo, p_cuenta_real) returning id into nuevo;
  return nuevo;
end $$;

-- Guarda la respuesta (o el error) de una consulta
create or replace function public.gasto_ia_completar(p_id bigint, p_datos jsonb) returns void
language plpgsql security definer set search_path = public as $$ -- SQL21C
begin
  update gasto_ia_consultas set
    modelo_respuesta = p_datos ->> 'modelo_respuesta', cuenta_sugerida = p_datos ->> 'cuenta_sugerida',
    confianza = gasto_num(p_datos ->> 'confianza'), motivo = p_datos ->> 'motivo', alternativa = p_datos ->> 'alternativa',
    input_tokens = gasto_num(p_datos ->> 'input_tokens')::integer, output_tokens = gasto_num(p_datos ->> 'output_tokens')::integer,
    cache_lectura = gasto_num(p_datos ->> 'cache_lectura')::integer, cache_escritura = gasto_num(p_datos ->> 'cache_escritura')::integer,
    costo_usd = gasto_num(p_datos ->> 'costo_usd'), duracion_ms = gasto_num(p_datos ->> 'duracion_ms')::integer, error = p_datos ->> 'error'
  where id = p_id;
end $$;

alter table public.gasto_ia_consultas enable row level security;
drop policy if exists gasto_ia_consultas_leer on public.gasto_ia_consultas;
create policy gasto_ia_consultas_leer on public.gasto_ia_consultas for select to anon, authenticated using (true);
grant select on public.gasto_ia_consultas to anon, authenticated;
revoke all on function public.gasto_ia_contexto(jsonb) from public, anon, authenticated;
revoke all on function public.gasto_ia_reservar(text, text, bigint, text, text, text, text) from public, anon, authenticated;
revoke all on function public.gasto_ia_completar(bigint, jsonb) from public, anon, authenticated;
grant execute on function public.gasto_ia_contexto(jsonb) to service_role;
grant execute on function public.gasto_ia_reservar(text, text, bigint, text, text, text, text) to service_role;
grant execute on function public.gasto_ia_completar(bigint, jsonb) to service_role;
grant select, insert, update on public.gasto_ia_consultas to service_role;
grant usage, select on sequence public.gasto_ia_consultas_id_seq to service_role;

notify pgrst, 'reload schema';

commit;

-- Revisión: debe decir «SQL 21C listo»
select 'SQL 21C listo' as estado,
       (select valor #>> '{}' from public.gestion_parametros where clave = 'ia_modelo') as modelo,
       (select valor #>> '{}' from public.gestion_parametros where clave = 'ia_tope_diario') as tope_diario,
       jsonb_array_length(public.gasto_ia_contexto('{}'::jsonb) -> 'cuentas') as cuentas_que_ve_claude,
       jsonb_array_length(public.gasto_ia_contexto('{}'::jsonb) -> 'ejemplos') as ejemplos_que_ve_claude;
