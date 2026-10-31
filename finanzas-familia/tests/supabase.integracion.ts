// Pruebas de seguridad del esquema de Supabase (supabase/esquema.sql).
// Requiere Supabase local con el esquema aplicado:
//   npx supabase start   →   psql ... -f supabase/esquema.sql
//   SUPABASE_URL=http://127.0.0.1:54321 SUPABASE_ANON_KEY=... npm run test:supabase
import { createClient, type SupabaseClient } from '@supabase/supabase-js';
import { randomUUID } from 'node:crypto';
import { beforeAll, describe, expect, it } from 'vitest';

const URL = process.env.SUPABASE_URL || 'http://127.0.0.1:54321';
const KEY = process.env.SUPABASE_ANON_KEY || '';
const run = Date.now().toString(36);

async function usuario(nombre: string): Promise<{ sb: SupabaseClient; uid: string }> {
  const sb = createClient(URL, KEY, { auth: { persistSession: false, autoRefreshToken: false } });
  const { data, error } = await sb.auth.signUp({ email: `${nombre}-${run}@ejemplo.cl`, password: 'clave-segura-123', options: { data: { nombre } } });
  if (error) throw error;
  if (!data.session) throw new Error('El Supabase de pruebas debe tener desactivada la confirmación de correo');
  return { sb, uid: data.user!.id };
}

async function crearFamilia(sb: SupabaseClient, nombre: string) {
  const id = randomUUID();
  const { error } = await sb.rpc('crear_familia', {
    p_id: id, p_nombre: nombre, p_cifrado: { v: 1, sal: 's', verificador: 'v' }, p_settings_enc: 'CIFRADO', p_creado_en: Date.now(), p_mi_nombre: nombre,
  });
  if (error) throw error;
  return id;
}

const gasto = (id: string, mes = '2026-10') => ({ op: 'set', coll: 'gastos', id, enc: 'CIFRADO==', mes, creado_en: Date.now() });

async function invitar(sb: SupabaseClient, uid: string, familia: string, rol = 'admin', dias = 7) {
  const codigo = Array.from({ length: 8 }, () => 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'[Math.floor(Math.random() * 32)]).join('');
  const { error } = await sb.from('invitaciones').insert({
    codigo, familia_id: familia, familia_nombre: 'Casa', rol, creado_por: uid, expira: new Date(Date.now() + dias * 86400000).toISOString(),
  });
  return { codigo, error };
}

let sean: { sb: SupabaseClient; uid: string };
let dani: { sb: SupabaseClient; uid: string };
let rosa: { sb: SupabaseClient; uid: string };
let casa: string;
let perez: string;

beforeAll(async () => {
  if (!KEY) throw new Error('Falta SUPABASE_ANON_KEY');
  [sean, dani, rosa] = await Promise.all([usuario('sean'), usuario('dani'), usuario('rosa')]);
  casa = await crearFamilia(sean.sb, 'Casa DY');
  perez = await crearFamilia(rosa.sb, 'Familia Pérez');
  const { error } = await sean.sb.rpc('aplicar_cambios', { p_familia: casa, p_ops: [gasto('g1')] });
  if (error) throw error;
});

describe('aislamiento entre familias', () => {
  it('el miembro lee su familia y sus registros', async () => {
    const f = await sean.sb.from('familias').select('nombre').eq('id', casa);
    expect(f.data).toEqual([{ nombre: 'Casa DY' }]);
    const r = await sean.sb.from('registros').select('id').eq('familia_id', casa);
    expect(r.data?.map((x) => x.id)).toEqual(['g1']);
  });
  it('otra familia no ve ni lista nada', async () => {
    expect((await rosa.sb.from('familias').select('*').eq('id', casa)).data).toEqual([]);
    expect((await rosa.sb.from('registros').select('*').eq('familia_id', casa)).data).toEqual([]);
    expect((await rosa.sb.from('miembros').select('*').eq('familia_id', casa)).data).toEqual([]);
    const todas = await rosa.sb.from('familias').select('id');
    expect(todas.data?.map((x) => x.id)).toEqual([perez]);
  });
  it('otra familia no puede escribir ni borrar', async () => {
    const r = await rosa.sb.rpc('aplicar_cambios', { p_familia: casa, p_ops: [gasto('intruso')] });
    expect(r.error?.code).toBe('42501');
    const d = await rosa.sb.rpc('aplicar_cambios', { p_familia: casa, p_ops: [{ op: 'delete', coll: 'gastos', id: 'g1' }] });
    expect(d.error?.code).toBe('42501');
    await rosa.sb.from('familias').update({ settings_enc: 'robado' }).eq('id', casa);
    const f = await sean.sb.from('familias').select('settings_enc').eq('id', casa).single();
    expect(f.data?.settings_enc).toBe('CIFRADO');
  });
  it('no se puede escribir directo en las tablas (solo por funciones)', async () => {
    const r = await sean.sb.from('registros').insert({ familia_id: casa, coleccion: 'gastos', id: 'x', enc: 'a', creado_por: sean.uid, creado_en: 1 });
    expect(r.error).toBeTruthy();
    const m = await rosa.sb.from('miembros').insert({ familia_id: casa, uid: rosa.uid, rol: 'admin', unido_en: 1 });
    expect(m.error).toBeTruthy();
  });
  it('sin sesión no se ve nada', async () => {
    const anon = createClient(URL, KEY, { auth: { persistSession: false } });
    expect((await anon.from('familias').select('*')).data ?? []).toEqual([]);
    expect((await anon.rpc('aplicar_cambios', { p_familia: casa, p_ops: [gasto('a')] })).error).toBeTruthy();
  });
});

describe('invitaciones', () => {
  it('la pareja se une con el código y queda usado', async () => {
    const { codigo, error } = await invitar(sean.sb, sean.uid, casa);
    expect(error).toBeNull();
    const r = await dani.sb.rpc('unirse_familia', { p_codigo: codigo.slice(0, 4) + '-' + codigo.slice(4).toLowerCase(), p_mi_nombre: 'Daniela' });
    expect(r.error).toBeNull();
    expect(r.data).toMatchObject({ familia_id: casa, rol: 'admin' });
    expect((await dani.sb.from('registros').select('id').eq('familia_id', casa)).data?.length).toBe(1);
    const otro = await rosa.sb.rpc('unirse_familia', { p_codigo: codigo, p_mi_nombre: 'Rosa' });
    expect(otro.error?.message).toMatch(/ya fue usado/);
  });
  it('códigos inexistentes o vencidos no sirven', async () => {
    expect((await rosa.sb.rpc('unirse_familia', { p_codigo: 'ZZZZ9999', p_mi_nombre: 'x' })).error?.message).toMatch(/no existe/);
    const { codigo } = await invitar(sean.sb, sean.uid, casa, 'admin', -1);
    expect((await rosa.sb.rpc('unirse_familia', { p_codigo: codigo, p_mi_nombre: 'x' })).error?.message).toMatch(/expiró/);
  });
  it('no se pueden crear invitaciones largas, ni para otra familia, ni listarlas', async () => {
    expect((await invitar(sean.sb, sean.uid, casa, 'admin', 30)).error).toBeTruthy();
    expect((await invitar(rosa.sb, rosa.uid, casa)).error).toBeTruthy();
    expect((await rosa.sb.from('invitaciones').select('*')).data).toEqual([]);
  });
});

describe('roles', () => {
  let hijo: { sb: SupabaseClient; uid: string };
  beforeAll(async () => {
    hijo = await usuario('hijo');
    const { codigo } = await invitar(sean.sb, sean.uid, casa, 'miembro');
    const r = await hijo.sb.rpc('unirse_familia', { p_codigo: codigo, p_mi_nombre: 'Hijo' });
    if (r.error) throw r.error;
  });
  it('un miembro registra y edita el presupuesto, pero no invita, ni renombra, ni cambia roles', async () => {
    expect((await hijo.sb.rpc('aplicar_cambios', { p_familia: casa, p_ops: [gasto('gh')] })).error).toBeNull();
    expect((await hijo.sb.from('familias').update({ settings_enc: 'NUEVO' }).eq('id', casa)).error).toBeNull();
    expect((await invitar(hijo.sb, hijo.uid, casa)).error).toBeTruthy();
    expect((await hijo.sb.rpc('renombrar_familia', { p_familia: casa, p_nombre: 'X' })).error).toBeTruthy();
    await hijo.sb.from('miembros').update({ rol: 'admin' }).eq('familia_id', casa).eq('uid', hijo.uid);
    await hijo.sb.from('miembros').delete().eq('familia_id', casa).eq('uid', sean.uid);
    const m = await sean.sb.from('miembros').select('uid, rol').eq('familia_id', casa);
    expect(m.data?.find((x) => x.uid === hijo.uid)?.rol).toBe('miembro');
    expect(m.data?.some((x) => x.uid === sean.uid)).toBe(true);
  });
  it('un admin quita a un miembro y este deja de ver los datos', async () => {
    expect((await sean.sb.from('miembros').delete().eq('familia_id', casa).eq('uid', hijo.uid)).error).toBeNull();
    expect((await hijo.sb.from('registros').select('id').eq('familia_id', casa)).data).toEqual([]);
    expect((await hijo.sb.rpc('aplicar_cambios', { p_familia: casa, p_ops: [gasto('gh2')] })).error?.code).toBe('42501');
  });
});

describe('tiempo real', () => {
  it('los cambios llegan solo a los miembros de la familia', async () => {
    const recibido: Record<string, unknown[]> = { dani: [], rosa: [] };
    const suscribir = (quien: 'dani' | 'rosa', sb: SupabaseClient) => new Promise<() => void>((res) => {
      const canal = sb.channel(`prueba-${quien}-${run}`)
        .on('postgres_changes', { event: '*', schema: 'public', table: 'registros', filter: `familia_id=eq.${casa}` }, (p) => recibido[quien].push(p.new))
        .subscribe((estado) => estado === 'SUBSCRIBED' && res(() => sb.removeChannel(canal)));
    });
    await dani.sb.realtime.setAuth((await dani.sb.auth.getSession()).data.session!.access_token);
    await rosa.sb.realtime.setAuth((await rosa.sb.auth.getSession()).data.session!.access_token);
    const [offD, offR] = await Promise.all([suscribir('dani', dani.sb), suscribir('rosa', rosa.sb)]);
    await new Promise((r) => setTimeout(r, 1500));
    await sean.sb.rpc('aplicar_cambios', { p_familia: casa, p_ops: [gasto('rt1')] });
    await sean.sb.rpc('aplicar_cambios', { p_familia: casa, p_ops: [{ op: 'delete', coll: 'gastos', id: 'rt1' }] });
    for (let i = 0; i < 40 && recibido.dani.length < 2; i++) await new Promise((r) => setTimeout(r, 250));
    await new Promise((r) => setTimeout(r, 1000));
    offD();
    offR();
    expect(recibido.dani).toHaveLength(2);
    expect(recibido.dani[1]).toMatchObject({ id: 'rt1', borrado: true, enc: null });
    expect(recibido.rosa).toHaveLength(0);
  }, 30000);
});
