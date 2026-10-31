// Backend con Supabase (Postgres + Auth + Realtime). Ver supabase/esquema.sql.
import { createClient, type RealtimeChannel, type User } from '@supabase/supabase-js';
import type { AppUser, ColeccionNombre, FamilyDoc, FamilyRef, Invite, Member, RawDoc, Rol } from '../lib/types';
import { DIAS_INVITACION, generarCodigo, type Backend, type RangoMeses, type Unsub, type WriteOp } from './backend';

const env = import.meta.env;

interface FilaRegistro {
  id: string;
  enc: string | null;
  mes: string | null;
  creado_por: string | null;
  creado_en: number;
  borrado?: boolean;
  coleccion?: string;
  familia_id?: string;
}

interface Observador {
  fid: string;
  coll: ColeccionNombre;
  rango?: RangoMeses;
  docs: Map<string, RawDoc>;
  cb: (docs: RawDoc[]) => void;
  onError?: (e: Error) => void;
  recargar: () => void;
}

const aRaw = (f: FilaRegistro): RawDoc => ({
  id: f.id,
  enc: f.enc ?? '',
  mes: f.mes ?? undefined,
  creadoPor: f.creado_por ?? '',
  creadoEn: Number(f.creado_en),
});

function errorSupabase(e: { message?: string; code?: string; status?: number } | null): Error {
  const err = new Error(e?.message || 'Error desconocido');
  (err as Error & { code?: string }).code = e?.code;
  return err;
}

export function crearBackendSupabase(): Backend {
  const sb = createClient(env.VITE_SUPABASE_URL!, (env.VITE_SUPABASE_ANON_KEY || env.VITE_SUPABASE_PUBLISHABLE_KEY)!, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: 'pkce' },
  });

  // ---- pequeño bus interno para recargar listas después de un cambio propio ----
  const bus = new Map<string, Set<() => void>>();
  const escuchar = (k: string, fn: () => void): Unsub => {
    if (!bus.has(k)) bus.set(k, new Set());
    bus.get(k)!.add(fn);
    return () => bus.get(k)?.delete(fn);
  };
  const avisar = (k: string) => bus.get(k)?.forEach((fn) => fn());
  // Al volver a la app o recuperar internet, recargar todo lo visible.
  const alVolver = () => avisar('*');
  window.addEventListener('online', alVolver);
  document.addEventListener('visibilitychange', () => document.visibilityState === 'visible' && alVolver());

  const toAppUser = (u: User | null | undefined): AppUser | null =>
    u ? { uid: u.id, nombre: (u.user_metadata?.nombre as string) || (u.user_metadata?.full_name as string) || (u.email ? u.email.split('@')[0] : 'Usuario'), email: u.email ?? null } : null;

  // ---- Registros: lectura paginada + tiempo real compartido por familia ----
  const observadores = new Set<Observador>();
  const canales = new Map<string, { canal: RealtimeChannel; usos: number }>();

  const enRango = (o: Observador, mes: string | null | undefined) =>
    !o.rango || (mes != null && mes >= o.rango.desde && mes <= o.rango.hasta);

  async function leerTodo(fid: string, coll: ColeccionNombre, rango?: RangoMeses): Promise<RawDoc[]> {
    const out: RawDoc[] = [];
    const PAG = 1000;
    for (let desde = 0; ; desde += PAG) {
      let q = sb.from('registros').select('id, enc, mes, creado_por, creado_en')
        .eq('familia_id', fid).eq('coleccion', coll).eq('borrado', false);
      if (rango) q = q.gte('mes', rango.desde).lte('mes', rango.hasta);
      const { data, error } = await q.order('id').range(desde, desde + PAG - 1);
      if (error) throw errorSupabase(error);
      out.push(...(data as FilaRegistro[]).map(aRaw));
      if (!data || data.length < PAG) break;
    }
    return out;
  }

  function emitir(o: Observador) {
    o.cb([...o.docs.values()]);
  }

  function canalFamilia(fid: string): Unsub {
    let c = canales.get(fid);
    if (!c) {
      const canal = sb.channel(`registros-${fid}`)
        .on('postgres_changes', { event: '*', schema: 'public', table: 'registros', filter: `familia_id=eq.${fid}` }, (p) => {
          const f = p.new as FilaRegistro;
          if (!f || !f.id || f.familia_id !== fid) return;
          for (const o of observadores) {
            if (o.fid !== fid || o.coll !== f.coleccion) continue;
            if (f.borrado || !enRango(o, f.mes)) {
              if (o.docs.delete(f.id)) emitir(o);
            } else {
              o.docs.set(f.id, aRaw(f));
              emitir(o);
            }
          }
        })
        .subscribe((estado) => {
          // Al reconectar, recargar por si se perdió algún cambio.
          if (estado === 'SUBSCRIBED') for (const o of observadores) if (o.fid === fid) o.recargar();
        });
      c = { canal, usos: 0 };
      canales.set(fid, c);
    }
    c.usos++;
    return () => {
      const x = canales.get(fid);
      if (!x) return;
      x.usos--;
      if (x.usos <= 0) {
        sb.removeChannel(x.canal);
        canales.delete(fid);
      }
    };
  }

  /** Aplica los cambios en pantalla al instante (antes de que responda el servidor). */
  function aplicarLocal(fid: string, ops: WriteOp[]) {
    const tocados = new Set<Observador>();
    for (const op of ops) {
      for (const o of observadores) {
        if (o.fid !== fid || o.coll !== op.coll) continue;
        if (op.op === 'delete' || !enRango(o, op.data.mes)) {
          if (o.docs.delete(op.id)) tocados.add(o);
        } else {
          o.docs.set(op.id, { ...op.data, id: op.id });
          tocados.add(o);
        }
      }
    }
    tocados.forEach(emitir);
  }

  // ---- Familias ----
  async function leerFamilia(fid: string): Promise<FamilyDoc | null> {
    const { data, error } = await sb.from('familias').select('*').eq('id', fid).maybeSingle();
    if (error) throw errorSupabase(error);
    if (!data) return null;
    return {
      id: data.id, nombre: data.nombre, creadoPor: data.creado_por ?? '', creadoEn: Number(data.creado_en),
      cifrado: data.cifrado, settingsEnc: data.settings_enc,
    };
  }

  const authListeners = new Set<(u: AppUser | null) => void>();
  const recuperacion = new Set<() => void>();
  let ultimo = '';
  sb.auth.onAuthStateChange((evento, sesion) => {
    if (evento === 'PASSWORD_RECOVERY') recuperacion.forEach((fn) => fn());
    const u = toAppUser(sesion?.user);
    const k = JSON.stringify(u);
    if (k === ultimo) return;
    ultimo = k;
    authListeners.forEach((cb) => cb(u));
  });

  const urlApp = () => location.origin + location.pathname;

  return {
    mode: 'supabase',
    conGoogle: env.VITE_SUPABASE_GOOGLE === '1',

    onAuth(cb) {
      authListeners.add(cb);
      sb.auth.getSession().then(({ data }) => {
        const u = toAppUser(data.session?.user);
        ultimo = JSON.stringify(u);
        cb(u);
      });
      return () => authListeners.delete(cb);
    },
    async signIn(email, password) {
      const { error } = await sb.auth.signInWithPassword({ email: email.trim(), password });
      if (error) throw errorSupabase(error);
    },
    async signUp(nombre, email, password) {
      const { data, error } = await sb.auth.signUp({
        email: email.trim(), password, options: { data: { nombre: nombre.trim() }, emailRedirectTo: urlApp() },
      });
      if (error) throw errorSupabase(error);
      if (!data.session) {
        // El proyecto pide confirmar el correo antes de entrar.
        throw Object.assign(new Error('Te enviamos un correo para confirmar tu cuenta. Ábrelo y luego entra con tu correo y contraseña.'), { code: 'confirmar_correo' });
      }
    },
    async signInGoogle() {
      const { error } = await sb.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: urlApp() } });
      if (error) throw errorSupabase(error);
    },
    async resetPassword(email) {
      const { error } = await sb.auth.resetPasswordForEmail(email.trim(), { redirectTo: urlApp() });
      if (error) throw errorSupabase(error);
    },
    onRecuperacion(cb) {
      recuperacion.add(cb);
      return () => recuperacion.delete(cb);
    },
    async cambiarContrasena(password) {
      const { error } = await sb.auth.updateUser({ password });
      if (error) throw errorSupabase(error);
    },
    async signOut() {
      for (const { canal } of canales.values()) sb.removeChannel(canal);
      canales.clear();
      await sb.auth.signOut();
    },

    watchMyFamilies(user, cb) {
      let vivo = true;
      const cargar = async () => {
        const { data, error } = await sb.from('miembros').select('familia_id, rol, familias(nombre)').eq('uid', user.uid);
        if (!vivo) return;
        if (error) return console.warn(error.message);
        const filas = (data || []) as unknown as { familia_id: string; rol: Rol; familias: { nombre: string } | null }[];
        cb(filas.filter((f) => f.familias).map((f): FamilyRef => ({ id: f.familia_id, nombre: f.familias!.nombre, rol: f.rol }))
          .sort((a, b) => a.nombre.localeCompare(b.nombre)));
      };
      cargar();
      const off1 = escuchar('familias', cargar);
      const off2 = escuchar('*', cargar);
      return () => {
        vivo = false;
        off1();
        off2();
      };
    },
    newFamilyId: () => crypto.randomUUID(),
    async createFamily(user, familia, id) {
      const { error } = await sb.rpc('crear_familia', {
        p_id: id, p_nombre: familia.nombre, p_cifrado: familia.cifrado, p_settings_enc: familia.settingsEnc,
        p_creado_en: familia.creadoEn, p_mi_nombre: user.nombre,
      });
      if (error) throw errorSupabase(error);
      avisar('familias');
    },
    async joinFamily(user, codigo) {
      const { data, error } = await sb.rpc('unirse_familia', { p_codigo: codigo, p_mi_nombre: user.nombre });
      if (error) throw errorSupabase(error);
      const r = data as { familia_id: string; familia_nombre: string; rol: Rol };
      avisar('familias');
      return { id: r.familia_id, nombre: r.familia_nombre, rol: r.rol };
    },
    async leaveFamily(user, fid) {
      const { error } = await sb.from('miembros').delete().eq('familia_id', fid).eq('uid', user.uid);
      if (error) throw errorSupabase(error);
      avisar('familias');
    },
    async forgetFamily() {
      avisar('familias');
    },

    watchFamily(fid, cb, onError) {
      let vivo = true;
      const cargar = async () => {
        try {
          const f = await leerFamilia(fid);
          if (!vivo) return;
          if (f) cb(f);
          else onError(Object.assign(new Error('Sin acceso'), { code: 'permission-denied' }));
        } catch (e) {
          if (vivo) onError(e as Error);
        }
      };
      cargar();
      const canal = sb.channel(`familia-${fid}`)
        .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'familias', filter: `id=eq.${fid}` }, () => cargar())
        .subscribe();
      const off1 = escuchar(`familia:${fid}`, cargar);
      const off2 = escuchar('*', cargar);
      return () => {
        vivo = false;
        sb.removeChannel(canal);
        off1();
        off2();
      };
    },
    async updateFamily(fid, patch) {
      if (patch.settingsEnc != null) {
        const { error } = await sb.from('familias').update({ settings_enc: patch.settingsEnc }).eq('id', fid);
        if (error) throw errorSupabase(error);
      }
      if (patch.nombre != null) {
        const { error } = await sb.rpc('renombrar_familia', { p_familia: fid, p_nombre: patch.nombre });
        if (error) throw errorSupabase(error);
        avisar('familias');
      }
      avisar(`familia:${fid}`);
    },
    watchMembers(fid, cb) {
      let vivo = true;
      const cargar = async () => {
        const { data, error } = await sb.from('miembros').select('*').eq('familia_id', fid).order('unido_en');
        if (!vivo || error) return;
        cb((data || []).map((m): Member => ({ uid: m.uid, nombre: m.nombre, email: m.email, rol: m.rol, unidoEn: Number(m.unido_en) })));
      };
      cargar();
      const off1 = escuchar(`miembros:${fid}`, cargar);
      const off2 = escuchar('*', cargar);
      return () => {
        vivo = false;
        off1();
        off2();
      };
    },
    async setMemberRole(fid, uid, rol) {
      const { error } = await sb.from('miembros').update({ rol }).eq('familia_id', fid).eq('uid', uid);
      if (error) throw errorSupabase(error);
      avisar(`miembros:${fid}`);
    },
    async removeMember(fid, uid) {
      const { error } = await sb.from('miembros').delete().eq('familia_id', fid).eq('uid', uid);
      if (error) throw errorSupabase(error);
      avisar(`miembros:${fid}`);
    },
    async createInvite(user, family, rol) {
      const codigo = generarCodigo();
      const expira = Date.now() + DIAS_INVITACION * 86400000;
      const { error } = await sb.from('invitaciones').insert({
        codigo, familia_id: family.id, familia_nombre: family.nombre, rol, creado_por: user.uid, expira: new Date(expira).toISOString(),
      });
      if (error) throw errorSupabase(error);
      const inv: Invite = { codigo, familyId: family.id, familyNombre: family.nombre, rol, creadoPor: user.uid, expira };
      return inv;
    },

    watchCollection(fid, coll, cb, rango, onError) {
      if (coll === 'adjuntos') {
        cb([]);
        return () => undefined;
      }
      let vivo = true;
      let turno = 0;
      const o: Observador = {
        fid, coll, rango, docs: new Map(), cb, onError,
        recargar: async () => {
          const t = ++turno;
          try {
            const docs = await leerTodo(fid, coll, rango);
            if (!vivo || t !== turno) return;
            o.docs = new Map(docs.map((d) => [d.id, d]));
            emitir(o);
          } catch (e) {
            if (!vivo) return;
            if (onError) onError(e as Error);
            else cb([]);
          }
        },
      };
      observadores.add(o);
      o.recargar();
      const offCanal = canalFamilia(fid);
      const offBus = escuchar('*', o.recargar);
      return () => {
        vivo = false;
        observadores.delete(o);
        offCanal();
        offBus();
      };
    },
    getCollection: (fid, coll, rango) => leerTodo(fid, coll, rango),
    async getDoc(fid, coll, id) {
      if (coll === 'adjuntos') {
        const { data, error } = await sb.from('adjuntos').select('id, enc, creado_por, creado_en').eq('familia_id', fid).eq('id', id).maybeSingle();
        if (error) throw errorSupabase(error);
        return data ? aRaw(data as FilaRegistro) : null;
      }
      const { data, error } = await sb.from('registros').select('id, enc, mes, creado_por, creado_en, borrado')
        .eq('familia_id', fid).eq('coleccion', coll).eq('id', id).maybeSingle();
      if (error) throw errorSupabase(error);
      return data && !data.borrado ? aRaw(data as FilaRegistro) : null;
    },
    async commit(fid, ops) {
      aplicarLocal(fid, ops);
      try {
        for (let i = 0; i < ops.length; i += 200) {
          const lote = ops.slice(i, i + 200).map((o) => o.op === 'set'
            ? { op: 'set', coll: o.coll, id: o.id, enc: o.data.enc, mes: o.data.mes ?? '', creado_en: o.data.creadoEn }
            : { op: 'delete', coll: o.coll, id: o.id });
          const { error } = await sb.rpc('aplicar_cambios', { p_familia: fid, p_ops: lote });
          if (error) throw errorSupabase(error);
        }
      } catch (e) {
        // Deshacer lo mostrado: recargar desde el servidor.
        for (const o of observadores) if (o.fid === fid) o.recargar();
        throw e;
      }
    },
  };
}
