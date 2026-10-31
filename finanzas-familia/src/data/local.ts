// Modo demostración: mismo comportamiento que Firebase, pero los datos quedan
// solo en este dispositivo (localStorage). Sirve para probar la app sin crear
// el proyecto en la nube.
import { nuevoId } from '../lib/defaults';
import type { AppUser, ColeccionNombre, FamilyDoc, FamilyRef, Invite, Member, RawDoc, Rol } from '../lib/types';
import { DIAS_INVITACION, generarCodigo, normalizarCodigo, type Backend, type Unsub } from './backend';

interface DB {
  users: Record<string, { nombre: string; email: string | null; families: Record<string, { nombre: string; rol: Rol }> }>;
  families: Record<string, FamilyDoc>;
  members: Record<string, Record<string, Member>>;
  colls: Record<string, Partial<Record<ColeccionNombre, Record<string, RawDoc>>>>;
  invites: Record<string, Invite>;
  session: string | null;
}

const KEY = 'ff_demo_db_v1';

function vacia(): DB {
  return { users: {}, families: {}, members: {}, colls: {}, invites: {}, session: null };
}

export function crearBackendLocal(): Backend {
  let db: DB = cargar();
  const listeners = new Set<() => void>();

  function cargar(): DB {
    try {
      const s = localStorage.getItem(KEY);
      return s ? { ...vacia(), ...JSON.parse(s) } : vacia();
    } catch {
      return vacia();
    }
  }
  function guardar() {
    try {
      localStorage.setItem(KEY, JSON.stringify(db));
    } catch (e) {
      console.error('No se pudo guardar', e);
      throw new Error('No hay espacio en el dispositivo para guardar.');
    }
    queueMicrotask(() => listeners.forEach((l) => l()));
  }
  window.addEventListener('storage', (e) => {
    if (e.key === KEY) {
      db = cargar();
      listeners.forEach((l) => l());
    }
  });

  function watch(fn: () => void): Unsub {
    listeners.add(fn);
    queueMicrotask(fn);
    return () => listeners.delete(fn);
  }

  const usuarioActual = (): AppUser | null => {
    const uid = db.session;
    const u = uid ? db.users[uid] : null;
    return uid && u ? { uid, nombre: u.nombre, email: u.email } : null;
  };
  const esMiembro = (fid: string) => !!(db.session && db.members[fid]?.[db.session]);
  const exigirMiembro = (fid: string) => {
    if (!esMiembro(fid)) throw Object.assign(new Error('Sin permiso'), { code: 'permission-denied' });
  };
  const clone = <T>(x: T): T => JSON.parse(JSON.stringify(x));

  return {
    mode: 'local',
    conGoogle: false,
    onAuth(cb) {
      let last = '';
      return watch(() => {
        const u = usuarioActual();
        const k = JSON.stringify(u);
        if (k !== last) {
          last = k;
          cb(u);
        }
      });
    },
    async signIn(email) {
      const e = email.trim().toLowerCase();
      const uid = Object.keys(db.users).find((id) => db.users[id].email === e);
      if (!uid) throw Object.assign(new Error('No existe'), { code: 'auth/user-not-found' });
      db.session = uid;
      guardar();
    },
    async signUp(nombre, email) {
      const e = email.trim().toLowerCase();
      if (Object.values(db.users).some((u) => u.email === e)) {
        throw Object.assign(new Error('Ya existe'), { code: 'auth/email-already-in-use' });
      }
      const uid = nuevoId();
      db.users[uid] = { nombre: nombre.trim(), email: e, families: {} };
      db.session = uid;
      guardar();
    },
    async signInGoogle() {
      throw new Error('En modo demostración usa nombre y correo.');
    },
    async resetPassword() {
      throw new Error('En modo demostración no hay contraseñas.');
    },
    async signOut() {
      db.session = null;
      guardar();
    },

    watchMyFamilies(user, cb) {
      return watch(() => {
        const fams = db.users[user.uid]?.families || {};
        cb(Object.entries(fams).map(([id, f]): FamilyRef => ({ id, nombre: f.nombre, rol: f.rol }))
          .sort((a, b) => a.nombre.localeCompare(b.nombre)));
      });
    },
    newFamilyId: () => nuevoId(),
    async createFamily(user, familia, id) {
      db.families[id] = { ...clone(familia), id };
      db.members[id] = { [user.uid]: { uid: user.uid, nombre: user.nombre, email: user.email, rol: 'admin', unidoEn: Date.now() } };
      db.colls[id] = {};
      db.users[user.uid].families[id] = { nombre: familia.nombre, rol: 'admin' };
      guardar();
    },
    async joinFamily(user, codigoIn) {
      const inv = db.invites[normalizarCodigo(codigoIn)];
      if (!inv) throw new Error('El código no existe. Revisa que esté bien escrito.');
      if (inv.expira < Date.now()) throw new Error('El código expiró. Pide uno nuevo a tu familia.');
      db.members[inv.familyId] ||= {};
      if (!db.members[inv.familyId][user.uid]) {
        if (inv.usadoPor) throw new Error('Este código ya fue usado. Pide uno nuevo a tu familia.');
        inv.usadoPor = user.uid;
        db.members[inv.familyId][user.uid] = { uid: user.uid, nombre: user.nombre, email: user.email, rol: inv.rol, unidoEn: Date.now() };
      }
      db.users[user.uid].families[inv.familyId] = { nombre: inv.familyNombre, rol: inv.rol };
      guardar();
      return { id: inv.familyId, nombre: inv.familyNombre, rol: inv.rol };
    },
    async leaveFamily(user, fid) {
      delete db.members[fid]?.[user.uid];
      delete db.users[user.uid]?.families[fid];
      guardar();
    },
    async forgetFamily(user, fid) {
      delete db.users[user.uid]?.families[fid];
      guardar();
    },

    watchFamily(fid, cb, onError) {
      return watch(() => {
        if (!esMiembro(fid)) {
          onError(Object.assign(new Error('Sin permiso'), { code: 'permission-denied' }));
          return;
        }
        cb(db.families[fid] ? clone(db.families[fid]) : null);
      });
    },
    async updateFamily(fid, patch) {
      exigirMiembro(fid);
      Object.assign(db.families[fid], patch);
      if (patch.nombre) {
        for (const u of Object.values(db.users)) if (u.families[fid]) u.families[fid].nombre = patch.nombre;
      }
      guardar();
    },
    watchMembers(fid, cb) {
      return watch(() => cb(esMiembro(fid) ? Object.values(db.members[fid] || {}).sort((a, b) => a.unidoEn - b.unidoEn) : []));
    },
    async setMemberRole(fid, uid, rol) {
      exigirMiembro(fid);
      db.members[fid][uid].rol = rol;
      if (db.users[uid]?.families[fid]) db.users[uid].families[fid].rol = rol;
      guardar();
    },
    async removeMember(fid, uid) {
      exigirMiembro(fid);
      delete db.members[fid][uid];
      guardar();
    },
    async createInvite(user, family, rol) {
      exigirMiembro(family.id);
      const inv: Invite = {
        codigo: generarCodigo(), familyId: family.id, familyNombre: family.nombre, rol,
        creadoPor: user.uid, expira: Date.now() + DIAS_INVITACION * 86400000,
      };
      db.invites[inv.codigo] = inv;
      guardar();
      return inv;
    },

    watchCollection(fid, c, cb, rango) {
      let last = '';
      return watch(() => {
        if (!esMiembro(fid)) return cb([]);
        const docs = Object.values(db.colls[fid]?.[c] || {}).filter((d) =>
          !rango || (d.mes != null && d.mes >= rango.desde && d.mes <= rango.hasta));
        const k = JSON.stringify(docs);
        if (k !== last) {
          last = k;
          cb(clone(docs));
        }
      });
    },
    async getCollection(fid, c, rango) {
      exigirMiembro(fid);
      return clone(Object.values(db.colls[fid]?.[c] || {}).filter((d) =>
        !rango || (d.mes != null && d.mes >= rango.desde && d.mes <= rango.hasta)));
    },
    async getDoc(fid, c, id) {
      exigirMiembro(fid);
      const d = db.colls[fid]?.[c]?.[id];
      return d ? clone(d) : null;
    },
    async commit(fid, ops) {
      exigirMiembro(fid);
      db.colls[fid] ||= {};
      for (const o of ops) {
        const col = (db.colls[fid][o.coll] ||= {});
        if (o.op === 'set') col[o.id] = { ...clone(o.data), id: o.id };
        else delete col[o.id];
      }
      guardar();
    },
  };
}
