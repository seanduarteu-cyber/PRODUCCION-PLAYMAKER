import { initializeApp } from 'firebase/app';
import {
  browserLocalPersistence, browserPopupRedirectResolver, connectAuthEmulator, createUserWithEmailAndPassword,
  getRedirectResult, GoogleAuthProvider, indexedDBLocalPersistence, initializeAuth,
  onAuthStateChanged, sendPasswordResetEmail, signInWithEmailAndPassword, signInWithPopup,
  signInWithRedirect, signOut, updateProfile, type User,
} from 'firebase/auth';
import {
  collection, connectFirestoreEmulator, deleteDoc, deleteField, doc, getDoc, getDocs, initializeFirestore, onSnapshot,
  orderBy, persistentLocalCache, persistentMultipleTabManager, query, setDoc, Timestamp,
  updateDoc, where, writeBatch, type DocumentData, type Query,
} from 'firebase/firestore';
import type { AppUser, ColeccionNombre, FamilyDoc, Invite, Member, RawDoc, Rol } from '../lib/types';
import {
  DIAS_INVITACION, generarCodigo, normalizarCodigo,
  type Backend, type RangoMeses, type Unsub, type WriteOp,
} from './backend';

const env = import.meta.env;

function authDomain(): string {
  // En Firebase Hosting conviene usar el mismo dominio de la app (evita problemas
  // de inicio de sesión con Google en iPhone / Safari).
  const h = location.hostname;
  if (h.endsWith('.web.app') || h.endsWith('.firebaseapp.com')) return h;
  return env.VITE_FIREBASE_AUTH_DOMAIN || `${env.VITE_FIREBASE_PROJECT_ID}.firebaseapp.com`;
}

export function crearBackendFirebase(): Backend {
  const app = initializeApp({
    apiKey: env.VITE_FIREBASE_API_KEY,
    authDomain: authDomain(),
    projectId: env.VITE_FIREBASE_PROJECT_ID,
    storageBucket: env.VITE_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: env.VITE_FIREBASE_MESSAGING_SENDER_ID,
    appId: env.VITE_FIREBASE_APP_ID,
  });
  const auth = initializeAuth(app, {
    persistence: [indexedDBLocalPersistence, browserLocalPersistence],
    popupRedirectResolver: browserPopupRedirectResolver,
  });
  auth.languageCode = 'es';
  const db = initializeFirestore(app, {
    ignoreUndefinedProperties: true,
    localCache: persistentLocalCache({ tabManager: persistentMultipleTabManager() }),
  });

  if (env.VITE_FIREBASE_EMULADOR) {
    // Solo para pruebas locales con `firebase emulators:start`.
    connectAuthEmulator(auth, `http://${location.hostname}:9099`, { disableWarnings: true });
    connectFirestoreEmulator(db, location.hostname, 8080);
  }

  const authListeners = new Set<(u: AppUser | null) => void>();
  let nombrePendiente = ''; // nombre recién escrito al registrarse (antes de que Firebase lo guarde)
  const toAppUser = (u: User | null, nombre?: string): AppUser | null =>
    u ? { uid: u.uid, nombre: nombre || u.displayName || nombrePendiente || (u.email ? u.email.split('@')[0] : 'Usuario'), email: u.email } : null;
  const emit = (u: AppUser | null) => authListeners.forEach((cb) => cb(u));

  getRedirectResult(auth).catch(() => undefined);

  const fam = (fid: string) => doc(db, 'families', fid);
  const userRef = (uid: string) => doc(db, 'users', uid);
  const coll = (fid: string, c: ColeccionNombre) => collection(db, 'families', fid, c);

  async function asegurarPerfil(u: AppUser) {
    await setDoc(userRef(u.uid), { nombre: u.nombre, email: u.email }, { merge: true });
  }

  const conId = <T>(d: { id: string; data(): DocumentData }) => ({ ...(d.data() as object), id: d.id }) as T;

  function construirQuery(fid: string, c: ColeccionNombre, rango?: RangoMeses): Query {
    if (!rango) return query(coll(fid, c));
    if (rango.desde === rango.hasta) return query(coll(fid, c), where('mes', '==', rango.desde));
    return query(coll(fid, c), where('mes', '>=', rango.desde), where('mes', '<=', rango.hasta), orderBy('mes'));
  }

  const esStandaloneIOS = () =>
    /iphone|ipad|ipod/i.test(navigator.userAgent) &&
    ((navigator as unknown as { standalone?: boolean }).standalone || matchMedia('(display-mode: standalone)').matches);

  return {
    mode: 'firebase',
    conGoogle: true,

    onAuth(cb) {
      authListeners.add(cb);
      const off = onAuthStateChanged(auth, (u) => {
        const au = toAppUser(u);
        cb(au);
        if (au) asegurarPerfil(au).catch(() => undefined);
      });
      return () => {
        authListeners.delete(cb);
        off();
      };
    },
    async signIn(email, password) {
      await signInWithEmailAndPassword(auth, email.trim(), password);
    },
    async signUp(nombre, email, password) {
      nombrePendiente = nombre.trim();
      const cred = await createUserWithEmailAndPassword(auth, email.trim(), password);
      await updateProfile(cred.user, { displayName: nombre.trim() });
      const au = toAppUser(cred.user, nombre.trim())!;
      await asegurarPerfil(au);
      emit(au);
    },
    async signInGoogle() {
      const provider = new GoogleAuthProvider();
      provider.setCustomParameters({ prompt: 'select_account' });
      if (esStandaloneIOS()) {
        await signInWithRedirect(auth, provider);
        return;
      }
      try {
        await signInWithPopup(auth, provider);
      } catch (e) {
        const code = (e as { code?: string }).code;
        if (code === 'auth/popup-blocked' || code === 'auth/operation-not-supported-in-this-environment') {
          await signInWithRedirect(auth, provider);
        } else throw e;
      }
    },
    async resetPassword(email) {
      await sendPasswordResetEmail(auth, email.trim());
    },
    async signOut() {
      await signOut(auth);
    },

    watchMyFamilies(user, cb) {
      return onSnapshot(userRef(user.uid), (snap) => {
        const fams = (snap.data()?.families || {}) as Record<string, { nombre: string; rol: Rol }>;
        cb(Object.entries(fams).map(([id, f]) => ({ id, nombre: f.nombre, rol: f.rol }))
          .sort((a, b) => a.nombre.localeCompare(b.nombre)));
      }, () => cb([]));
    },
    newFamilyId() {
      return doc(collection(db, 'families')).id;
    },
    async createFamily(user, familia, id) {
      const ref = fam(id);
      const nombre = familia.nombre;
      const b = writeBatch(db);
      b.set(ref, familia);
      const member: Member = { uid: user.uid, nombre: user.nombre, email: user.email, rol: 'admin', unidoEn: Date.now() };
      b.set(doc(db, 'families', ref.id, 'members', user.uid), member);
      b.set(userRef(user.uid), { nombre: user.nombre, email: user.email, families: { [ref.id]: { nombre, rol: 'admin' } } }, { merge: true });
      await b.commit();
    },
    async joinFamily(user, codigoIn) {
      const codigo = normalizarCodigo(codigoIn);
      const snap = await getDoc(doc(db, 'invites', codigo)).catch(() => null);
      if (!snap || !snap.exists()) throw new Error('El código no existe. Revisa que esté bien escrito.');
      const inv = snap.data() as { familyId: string; familyNombre: string; rol: Rol; expira: Timestamp };
      if (inv.expira.toMillis() < Date.now()) throw new Error('El código expiró. Pide uno nuevo a tu familia.');
      const memberRef = doc(db, 'families', inv.familyId, 'members', user.uid);
      const ya = await getDoc(memberRef).then((s) => s.exists()).catch(() => false);
      const b = writeBatch(db);
      if (!ya) {
        if ((snap.data() as { usadoPor?: string }).usadoPor) throw new Error('Este código ya fue usado. Pide uno nuevo a tu familia.');
        b.update(doc(db, 'invites', codigo), { usadoPor: user.uid });
        b.set(memberRef, { uid: user.uid, nombre: user.nombre, email: user.email, rol: inv.rol, unidoEn: Date.now(), codigo });
      }
      b.set(userRef(user.uid), { families: { [inv.familyId]: { nombre: inv.familyNombre, rol: inv.rol } } }, { merge: true });
      await b.commit();
      return { id: inv.familyId, nombre: inv.familyNombre, rol: inv.rol };
    },
    async leaveFamily(user, fid) {
      const b = writeBatch(db);
      b.delete(doc(db, 'families', fid, 'members', user.uid));
      b.update(userRef(user.uid), { [`families.${fid}`]: deleteField() });
      await b.commit();
    },
    async forgetFamily(user, fid) {
      await updateDoc(userRef(user.uid), { [`families.${fid}`]: deleteField() }).catch(() => undefined);
    },

    watchFamily(fid, cb, onError) {
      return onSnapshot(fam(fid), (s) => cb(s.exists() ? conId<FamilyDoc>(s) : null), (e) => onError(e));
    },
    async updateFamily(fid, patch) {
      await updateDoc(fam(fid), patch as DocumentData);
      if (patch.nombre && auth.currentUser) {
        await updateDoc(userRef(auth.currentUser.uid), { [`families.${fid}.nombre`]: patch.nombre }).catch(() => undefined);
      }
    },
    watchMembers(fid, cb) {
      return onSnapshot(collection(db, 'families', fid, 'members'), (s) =>
        cb(s.docs.map((d) => d.data() as Member).sort((a, b) => a.unidoEn - b.unidoEn)), () => cb([]));
    },
    async setMemberRole(fid, uid, rol) {
      await updateDoc(doc(db, 'families', fid, 'members', uid), { rol });
    },
    async removeMember(fid, uid) {
      await deleteDoc(doc(db, 'families', fid, 'members', uid));
    },
    async createInvite(user, family, rol) {
      const codigo = generarCodigo();
      const expira = Date.now() + DIAS_INVITACION * 86400000;
      await setDoc(doc(db, 'invites', codigo), {
        familyId: family.id, familyNombre: family.nombre, rol, creadoPor: user.uid, expira: Timestamp.fromMillis(expira),
      });
      const inv: Invite = { codigo, familyId: family.id, familyNombre: family.nombre, rol, creadoPor: user.uid, expira };
      return inv;
    },

    watchCollection(fid: string, c: ColeccionNombre, cb: (docs: RawDoc[]) => void, rango?: RangoMeses, onError?: (e: Error) => void): Unsub {
      return onSnapshot(construirQuery(fid, c, rango), (s) => cb(s.docs.map((d) => conId<RawDoc>(d))), (e) => {
        console.warn(c, e.code);
        if (onError) onError(e);
        else cb([]);
      });
    },
    async getCollection(fid: string, c: ColeccionNombre, rango?: RangoMeses) {
      const s = await getDocs(construirQuery(fid, c, rango));
      return s.docs.map((d) => conId<RawDoc>(d));
    },
    async getDoc(fid: string, c: ColeccionNombre, id: string) {
      const s = await getDoc(doc(coll(fid, c), id));
      return s.exists() ? conId<RawDoc>(s) : null;
    },
    async commit(fid: string, ops: WriteOp[]) {
      for (let i = 0; i < ops.length; i += 400) {
        const b = writeBatch(db);
        for (const o of ops.slice(i, i + 400)) {
          const ref = doc(coll(fid, o.coll), o.id);
          if (o.op === 'set') b.set(ref, o.data);
          else b.delete(ref);
        }
        await b.commit();
      }
    },
  };
}
