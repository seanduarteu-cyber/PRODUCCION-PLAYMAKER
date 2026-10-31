import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { claveGuardada, derivarLlave, descifrar, guardarClave, olvidarClave, verificarLlave } from '../lib/crypto';
import { mesActual } from '../lib/format';
import type {
  AppUser, Boleta, ColeccionNombre, Deuda, Family, FamilyDoc, FamilyRef, Gasto, Ingreso, Member, MesKey, Rol, Settings,
} from '../lib/types';
import { crearAcciones, deRaws, type Acciones } from './acciones';
import { mensajeError, type Backend, type RangoMeses } from './backend';
import { firebaseConfigurado } from './config';

// ---------------- Avisos (toasts) ----------------
export interface Aviso { id: number; texto: string; tipo: 'ok' | 'error' | 'info' }

// ---------------- App ----------------
interface AppCtx {
  backend: Backend;
  user: AppUser | null | undefined;
  families: FamilyRef[] | undefined;
  familyId: string | null;
  elegirFamilia: (id: string | null) => void;
  avisos: Aviso[];
  avisar: (texto: string, tipo?: Aviso['tipo']) => void;
  error: (e: unknown) => void;
}

const Ctx = createContext<AppCtx | null>(null);

export const useApp = () => {
  const c = useContext(Ctx);
  if (!c) throw new Error('Falta AppProvider');
  return c;
};

const LS_FAMILIA = 'ff_familia_actual';

let backendPromise: Promise<Backend> | null = null;
export function cargarBackend(): Promise<Backend> {
  backendPromise ||= firebaseConfigurado
    ? import('./firebase').then((m) => m.crearBackendFirebase())
    : import('./local').then((m) => m.crearBackendLocal());
  return backendPromise;
}

export function AppProvider({ backend, children }: { backend: Backend; children: ReactNode }) {
  const [user, setUser] = useState<AppUser | null | undefined>(undefined);
  const [families, setFamilies] = useState<FamilyRef[] | undefined>(undefined);
  const [familyId, setFamilyId] = useState<string | null>(() => {
    try {
      return localStorage.getItem(LS_FAMILIA);
    } catch {
      return null;
    }
  });
  const [avisos, setAvisos] = useState<Aviso[]>([]);
  const n = useRef(0);

  const avisar = useCallback((texto: string, tipo: Aviso['tipo'] = 'ok') => {
    const id = ++n.current;
    setAvisos((a) => [...a, { id, texto, tipo }]);
    setTimeout(() => setAvisos((a) => a.filter((x) => x.id !== id)), tipo === 'error' ? 6000 : 3000);
  }, []);
  const error = useCallback((e: unknown) => {
    console.error(e);
    avisar(mensajeError(e), 'error');
  }, [avisar]);

  useEffect(() => backend.onAuth(setUser), [backend]);
  const uid = user?.uid;
  const userRef = useRef(user);
  userRef.current = user;
  useEffect(() => {
    if (!uid || !userRef.current) {
      setFamilies(user === null ? [] : undefined);
      return;
    }
    setFamilies(undefined);
    return backend.watchMyFamilies(userRef.current, setFamilies);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [backend, uid]);

  const elegirFamilia = useCallback((id: string | null) => {
    setFamilyId(id);
    try {
      if (id) localStorage.setItem(LS_FAMILIA, id);
      else localStorage.removeItem(LS_FAMILIA);
    } catch {
      /* nada */
    }
  }, []);

  // Si la familia guardada ya no está en la lista, elegir la primera.
  useEffect(() => {
    if (!families) return;
    if (familyId && families.some((f) => f.id === familyId)) return;
    elegirFamilia(families[0]?.id ?? null);
  }, [families, familyId, elegirFamilia]);

  const value = useMemo(() => ({ backend, user, families, familyId, elegirFamilia, avisos, avisar, error }),
    [backend, user, families, familyId, elegirFamilia, avisos, avisar, error]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

// ---------------- Familia ----------------
export interface FamiliaCtx {
  family: Family;
  settings: Settings;
  members: Member[];
  miRol: Rol;
  esAdmin: boolean;
  clave: string;
  mes: MesKey;
  setMes: (m: MesKey) => void;
  gastos: Gasto[];
  ingresos: Ingreso[];
  boletas: Boleta[];
  deudas: Deuda[];
  cargando: boolean;
  acciones: Acciones;
  bloquear: () => void;
}

const FCtx = createContext<FamiliaCtx | null>(null);

export const useFamilia = () => {
  const c = useContext(FCtx);
  if (!c) throw new Error('Falta FamiliaProvider');
  return c;
};

function useColeccion<T>(familyId: string, llave: CryptoKey | null, coll: ColeccionNombre, rango?: RangoMeses): T[] | undefined {
  const { backend } = useApp();
  const [items, setItems] = useState<T[] | undefined>(undefined);
  const [intento, setIntento] = useState(0);
  const desde = rango?.desde;
  const hasta = rango?.hasta;
  useEffect(() => {
    if (!llave) return;
    let vivo = true;
    let ultimo = 0;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const off = backend.watchCollection(familyId, coll, (raws) => {
      const turno = ++ultimo;
      deRaws<T>(llave, raws).then((xs) => {
        if (vivo && turno === ultimo) setItems(xs);
      });
    }, desde && hasta ? { desde, hasta } : undefined, () => {
      // p. ej. permisos aún no sincronizados justo al crear/unirse: reintentar
      if (vivo && intento < 6) timer = setTimeout(() => vivo && setIntento((i) => i + 1), 1500 * (intento + 1));
      else if (vivo) setItems((x) => x ?? []);
    });
    return () => {
      vivo = false;
      clearTimeout(timer);
      off();
    };
  }, [backend, familyId, llave, coll, desde, hasta, intento]);
  useEffect(() => setItems(undefined), [familyId, coll, desde, hasta]);
  return items;
}

export type EstadoFamilia =
  | { paso: 'cargando' }
  | { paso: 'sin-acceso' }
  | { paso: 'bloqueada'; doc: FamilyDoc; desbloquear: (clave: string) => Promise<boolean> }
  | { paso: 'lista' };

export function FamiliaProvider({ familyId, children, renderEstado }: {
  familyId: string;
  children: ReactNode;
  renderEstado: (e: EstadoFamilia) => ReactNode;
}) {
  const { backend, user, error } = useApp();
  const [doc, setDoc] = useState<FamilyDoc | null | undefined>(undefined);
  const [sinAcceso, setSinAcceso] = useState(false);
  const [members, setMembers] = useState<Member[]>([]);
  const [llave, setLlave] = useState<{ key: CryptoKey; clave: string; sal: string } | null>(null);
  const [verificando, setVerificando] = useState(true);
  const [settings, setSettings] = useState<Settings | null>(null);
  const [mes, setMes] = useState<MesKey>(mesActual());

  useEffect(() => {
    setDoc(undefined);
    setSinAcceso(false);
    setLlave(null);
    setSettings(null);
    setVerificando(true);
    const off = backend.watchFamily(familyId, setDoc, (e) => {
      const code = (e as { code?: string }).code;
      if (code === 'permission-denied') setSinAcceso(true);
      else error(e);
    });
    const offM = backend.watchMembers(familyId, setMembers);
    return () => {
      off();
      offM();
    };
  }, [backend, familyId, error]);

  const probarClave = useCallback(async (clave: string, d: FamilyDoc) => {
    const key = await derivarLlave(clave, d.cifrado.sal);
    if (!(await verificarLlave(key, d.cifrado.verificador))) return null;
    return key;
  }, []);

  // Desbloqueo automático con la clave guardada en este dispositivo.
  const sal = doc?.cifrado?.sal;
  useEffect(() => {
    if (!doc || !sal) return;
    if (llave && llave.sal === sal) return;
    const clave = claveGuardada(familyId);
    if (!clave) {
      setVerificando(false);
      return;
    }
    let vivo = true;
    probarClave(clave, doc).then((key) => {
      if (!vivo) return;
      if (key) setLlave({ key, clave, sal });
      else olvidarClave(familyId);
      setVerificando(false);
    });
    return () => {
      vivo = false;
    };
  }, [doc, sal, familyId, llave, probarClave]);

  const settingsEnc = doc?.settingsEnc;
  useEffect(() => {
    if (!llave || !settingsEnc) return;
    let vivo = true;
    descifrar<Settings>(llave.key, settingsEnc)
      .then((s) => vivo && setSettings(s))
      .catch(error);
    return () => {
      vivo = false;
    };
  }, [llave, settingsEnc, error]);

  const key = llave?.key ?? null;
  const rangoMes = useMemo(() => ({ desde: mes, hasta: mes }), [mes]);
  const gastos = useColeccion<Gasto>(familyId, key, 'gastos', rangoMes);
  const ingresos = useColeccion<Ingreso>(familyId, key, 'ingresos', rangoMes);
  const boletas = useColeccion<Boleta>(familyId, key, 'boletas');
  const deudas = useColeccion<Deuda>(familyId, key, 'deudas');

  const boletasRef = useRef<Boleta[]>([]);
  const deudasRef = useRef<Deuda[]>([]);
  boletasRef.current = boletas ?? [];
  deudasRef.current = deudas ?? [];

  const acciones = useMemo(() => {
    if (!key || !user) return null;
    return crearAcciones({
      backend, familyId, llave: key, user, onError: error,
      get boletas() { return boletasRef.current; },
      get deudas() { return deudasRef.current; },
    });
  }, [backend, familyId, key, user, error]);

  const yo = members.find((m) => m.uid === user?.uid);
  const miRol: Rol = yo?.rol ?? 'miembro';

  const value = useMemo<FamiliaCtx | null>(() => {
    if (!doc || !llave || !settings || !acciones) return null;
    return {
      family: { id: doc.id, nombre: doc.nombre, creadoPor: doc.creadoPor, creadoEn: doc.creadoEn, settings },
      settings,
      members,
      miRol,
      esAdmin: miRol === 'admin',
      clave: llave.clave,
      mes,
      setMes,
      gastos: gastos ?? [],
      ingresos: ingresos ?? [],
      boletas: boletas ?? [],
      deudas: deudas ?? [],
      cargando: !gastos || !ingresos || !boletas || !deudas,
      acciones,
      bloquear: () => {
        olvidarClave(familyId);
        setLlave(null);
      },
    };
  }, [doc, llave, settings, acciones, members, miRol, mes, gastos, ingresos, boletas, deudas, familyId]);

  if (sinAcceso) return <>{renderEstado({ paso: 'sin-acceso' })}</>;
  if (doc === undefined || (doc && verificando && !llave)) return <>{renderEstado({ paso: 'cargando' })}</>;
  if (doc === null) return <>{renderEstado({ paso: 'sin-acceso' })}</>;
  if (!llave) {
    return <>{renderEstado({
      paso: 'bloqueada',
      doc,
      desbloquear: async (clave) => {
        const k = await probarClave(clave, doc);
        if (!k) return false;
        guardarClave(familyId, clave);
        setLlave({ key: k, clave, sal: doc.cifrado.sal });
        return true;
      },
    })}</>;
  }
  if (!value) return <>{renderEstado({ paso: 'cargando' })}</>;
  return <FCtx.Provider value={value}>{children}</FCtx.Provider>;
}
