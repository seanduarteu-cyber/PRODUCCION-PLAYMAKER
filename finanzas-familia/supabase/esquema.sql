-- =====================================================================
-- Finanzas Familia · esquema para Supabase
--
-- Cómo usarlo: Supabase › SQL Editor › New query › pega TODO este archivo
-- › Run. Se puede volver a ejecutar sin perder datos.
--
-- Seguridad:
--  * Cada familia (centro de costos) solo es visible para sus miembros
--    (Row Level Security). Nadie puede listar familias ni invitaciones.
--  * Los datos financieros llegan cifrados desde el teléfono (columna `enc`):
--    el servidor, y quien administra el proyecto, nunca ven montos,
--    descripciones ni categorías.
--  * Las escrituras pasan por funciones que validan la membresía.
-- =====================================================================

-- ---------- Tablas ----------
create table if not exists public.familias (
  id uuid primary key,
  nombre text not null check (char_length(nombre) between 1 and 80),
  creado_por uuid references auth.users (id) on delete set null,
  creado_en bigint not null,
  cifrado jsonb not null,
  settings_enc text not null check (char_length(settings_enc) < 1000000)
);

create table if not exists public.miembros (
  familia_id uuid not null references public.familias (id) on delete cascade,
  uid uuid not null references auth.users (id) on delete cascade,
  nombre text not null default '',
  email text,
  rol text not null check (rol in ('admin', 'miembro')),
  unido_en bigint not null,
  primary key (familia_id, uid)
);
create index if not exists miembros_uid on public.miembros (uid);

create table if not exists public.invitaciones (
  codigo text primary key check (codigo ~ '^[A-Z2-9]{8}$'),
  familia_id uuid not null references public.familias (id) on delete cascade,
  familia_nombre text not null,
  rol text not null check (rol in ('admin', 'miembro')),
  creado_por uuid not null,
  expira timestamptz not null,
  usado_por uuid
);

-- Gastos, ingresos, boletas y deudas (cifrados).
create table if not exists public.registros (
  familia_id uuid not null references public.familias (id) on delete cascade,
  coleccion text not null check (coleccion in ('gastos', 'ingresos', 'boletas', 'deudas')),
  id text not null check (char_length(id) <= 64),
  enc text check (char_length(enc) < 1000000),
  mes text check (mes ~ '^[0-9]{4}-[0-9]{2}$'),
  creado_por uuid,
  creado_en bigint not null,
  borrado boolean not null default false,
  actualizado timestamptz not null default now(),
  primary key (familia_id, coleccion, id)
);
create index if not exists registros_mes on public.registros (familia_id, coleccion, mes);

-- Fotos de boletas (cifradas). Tabla aparte para no enviarlas por tiempo real.
create table if not exists public.adjuntos (
  familia_id uuid not null references public.familias (id) on delete cascade,
  id text not null check (char_length(id) <= 64),
  enc text not null check (char_length(enc) < 1500000),
  creado_por uuid,
  creado_en bigint not null,
  primary key (familia_id, id)
);

-- ---------- Funciones de ayuda ----------
create or replace function public.es_miembro(fid uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.miembros where familia_id = fid and uid = auth.uid());
$$;

create or replace function public.es_admin(fid uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.miembros where familia_id = fid and uid = auth.uid() and rol = 'admin');
$$;

-- ---------- Permisos: solo lectura directa; las escrituras van por funciones ----------
alter table public.familias enable row level security;
alter table public.miembros enable row level security;
alter table public.invitaciones enable row level security;
alter table public.registros enable row level security;
alter table public.adjuntos enable row level security;

revoke all on public.familias, public.miembros, public.invitaciones, public.registros, public.adjuntos from anon, authenticated;
grant select on public.familias, public.miembros, public.invitaciones, public.registros, public.adjuntos to authenticated;
grant update (settings_enc) on public.familias to authenticated;
grant update (rol) on public.miembros to authenticated;
grant delete on public.miembros to authenticated;
grant insert, delete on public.invitaciones to authenticated;

drop policy if exists familias_leer on public.familias;
create policy familias_leer on public.familias for select to authenticated using (public.es_miembro(id));
drop policy if exists familias_presupuesto on public.familias;
create policy familias_presupuesto on public.familias for update to authenticated
  using (public.es_miembro(id)) with check (public.es_miembro(id));

drop policy if exists miembros_leer on public.miembros;
create policy miembros_leer on public.miembros for select to authenticated using (public.es_miembro(familia_id));
drop policy if exists miembros_rol on public.miembros;
create policy miembros_rol on public.miembros for update to authenticated
  using (public.es_admin(familia_id)) with check (public.es_admin(familia_id));
drop policy if exists miembros_quitar on public.miembros;
create policy miembros_quitar on public.miembros for delete to authenticated
  using (public.es_admin(familia_id) or uid = auth.uid());

drop policy if exists invitaciones_leer on public.invitaciones;
create policy invitaciones_leer on public.invitaciones for select to authenticated using (public.es_admin(familia_id));
drop policy if exists invitaciones_crear on public.invitaciones;
create policy invitaciones_crear on public.invitaciones for insert to authenticated
  with check (
    public.es_admin(familia_id) and creado_por = auth.uid() and usado_por is null
    and expira <= now() + interval '8 days'
  );
drop policy if exists invitaciones_borrar on public.invitaciones;
create policy invitaciones_borrar on public.invitaciones for delete to authenticated using (public.es_admin(familia_id));

drop policy if exists registros_leer on public.registros;
create policy registros_leer on public.registros for select to authenticated using (public.es_miembro(familia_id));
drop policy if exists adjuntos_leer on public.adjuntos;
create policy adjuntos_leer on public.adjuntos for select to authenticated using (public.es_miembro(familia_id));

-- ---------- Operaciones ----------

-- Crea la familia y deja a quien la crea como administrador.
create or replace function public.crear_familia(
  p_id uuid, p_nombre text, p_cifrado jsonb, p_settings_enc text, p_creado_en bigint, p_mi_nombre text
) returns void
language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'Debes iniciar sesión.' using errcode = '42501'; end if;
  insert into familias (id, nombre, creado_por, creado_en, cifrado, settings_enc)
    values (p_id, trim(p_nombre), auth.uid(), p_creado_en, p_cifrado, p_settings_enc);
  insert into miembros (familia_id, uid, nombre, email, rol, unido_en)
    values (p_id, auth.uid(), coalesce(p_mi_nombre, ''), auth.email(), 'admin', p_creado_en);
end;
$$;

-- Une al usuario a una familia con un código de invitación (un solo uso, vence).
create or replace function public.unirse_familia(p_codigo text, p_mi_nombre text) returns json
language plpgsql security definer set search_path = public as $$
declare
  inv invitaciones%rowtype;
begin
  if auth.uid() is null then raise exception 'Debes iniciar sesión.' using errcode = '42501'; end if;
  select * into inv from invitaciones where codigo = upper(regexp_replace(p_codigo, '[^A-Za-z0-9]', '', 'g')) for update;
  if not found then raise exception 'El código no existe. Revisa que esté bien escrito.'; end if;
  if exists (select 1 from miembros where familia_id = inv.familia_id and uid = auth.uid()) then
    return json_build_object('familia_id', inv.familia_id, 'familia_nombre', inv.familia_nombre,
      'rol', (select rol from miembros where familia_id = inv.familia_id and uid = auth.uid()));
  end if;
  if inv.usado_por is not null then raise exception 'Este código ya fue usado. Pide uno nuevo a tu familia.'; end if;
  if inv.expira < now() then raise exception 'El código expiró. Pide uno nuevo a tu familia.'; end if;
  insert into miembros (familia_id, uid, nombre, email, rol, unido_en)
    values (inv.familia_id, auth.uid(), coalesce(p_mi_nombre, ''), auth.email(), inv.rol,
            (extract(epoch from now()) * 1000)::bigint);
  update invitaciones set usado_por = auth.uid() where codigo = inv.codigo;
  return json_build_object('familia_id', inv.familia_id, 'familia_nombre', inv.familia_nombre, 'rol', inv.rol);
end;
$$;

-- Cambiar el nombre de la familia (solo administradores).
create or replace function public.renombrar_familia(p_familia uuid, p_nombre text) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not public.es_admin(p_familia) then raise exception 'Solo un administrador puede renombrar la familia.' using errcode = '42501'; end if;
  update familias set nombre = trim(p_nombre) where id = p_familia;
end;
$$;

-- Guarda o borra registros cifrados en un solo paso (todo o nada).
-- p_ops: [{op:'set', coll, id, enc, mes, creado_en} | {op:'delete', coll, id}]
create or replace function public.aplicar_cambios(p_familia uuid, p_ops jsonb) returns void
language plpgsql security definer set search_path = public as $$
declare
  o jsonb;
  c text;
begin
  if not public.es_miembro(p_familia) then
    raise exception 'No tienes permiso en esta familia.' using errcode = '42501';
  end if;
  if jsonb_array_length(p_ops) > 500 then raise exception 'Demasiados cambios en una sola operación.'; end if;
  for o in select * from jsonb_array_elements(p_ops) loop
    c := o->>'coll';
    if c = 'adjuntos' then
      if o->>'op' = 'set' then
        insert into adjuntos (familia_id, id, enc, creado_por, creado_en)
          values (p_familia, o->>'id', o->>'enc', auth.uid(), coalesce((o->>'creado_en')::bigint, 0))
          on conflict (familia_id, id) do update set enc = excluded.enc;
      else
        delete from adjuntos where familia_id = p_familia and id = o->>'id';
      end if;
    elsif o->>'op' = 'set' then
      insert into registros (familia_id, coleccion, id, enc, mes, creado_por, creado_en, borrado, actualizado)
        values (p_familia, c, o->>'id', o->>'enc', nullif(o->>'mes', ''), auth.uid(),
                coalesce((o->>'creado_en')::bigint, 0), false, now())
        on conflict (familia_id, coleccion, id)
        do update set enc = excluded.enc, mes = excluded.mes, borrado = false, actualizado = now();
    elsif o->>'op' = 'delete' then
      -- Se marca como borrado (y se vacía) para avisar en tiempo real a los demás miembros.
      update registros set enc = null, borrado = true, actualizado = now()
        where familia_id = p_familia and coleccion = c and id = o->>'id';
    else
      raise exception 'Operación desconocida';
    end if;
  end loop;
end;
$$;

revoke all on function public.crear_familia(uuid, text, jsonb, text, bigint, text) from public, anon;
revoke all on function public.unirse_familia(text, text) from public, anon;
revoke all on function public.renombrar_familia(uuid, text) from public, anon;
revoke all on function public.aplicar_cambios(uuid, jsonb) from public, anon;
revoke all on function public.es_miembro(uuid) from public, anon;
revoke all on function public.es_admin(uuid) from public, anon;
grant execute on function public.crear_familia(uuid, text, jsonb, text, bigint, text) to authenticated;
grant execute on function public.unirse_familia(text, text) to authenticated;
grant execute on function public.renombrar_familia(uuid, text) to authenticated;
grant execute on function public.aplicar_cambios(uuid, jsonb) to authenticated;
grant execute on function public.es_miembro(uuid) to authenticated;
grant execute on function public.es_admin(uuid) to authenticated;

-- ---------- Tiempo real (los gastos de uno aparecen al instante en el teléfono del otro) ----------
do $$
begin
  if not exists (select 1 from pg_publication_tables where pubname = 'supabase_realtime' and tablename = 'registros') then
    alter publication supabase_realtime add table public.registros;
  end if;
  if not exists (select 1 from pg_publication_tables where pubname = 'supabase_realtime' and tablename = 'familias') then
    alter publication supabase_realtime add table public.familias;
  end if;
end $$;
