// Pruebas de las reglas de seguridad de Firestore (requiere el emulador):
//   npm run test:reglas
import {
  assertFails, assertSucceeds, initializeTestEnvironment, type RulesTestEnvironment,
} from '@firebase/rules-unit-testing';
import {
  collection, deleteDoc, doc, getDoc, getDocs, setDoc, Timestamp, updateDoc, writeBatch, type Firestore,
} from 'firebase/firestore';
import { readFileSync } from 'node:fs';
import { afterAll, beforeAll, beforeEach, describe, it } from 'vitest';

let env: RulesTestEnvironment;
const FID = 'familiaDY';
const OTRA = 'familiaPerez';

const db = (uid: string | null): Firestore =>
  (uid ? env.authenticatedContext(uid).firestore() : env.unauthenticatedContext().firestore()) as unknown as Firestore;

const raw = (creadoPor: string, extra: Record<string, unknown> = {}) => ({ enc: 'CIFRADO==', mes: '2026-10', creadoPor, creadoEn: 1, ...extra });

async function crearFamilia(d: Firestore, uid: string, fid: string) {
  const b = writeBatch(d);
  b.set(doc(d, 'families', fid), { nombre: 'Casa', creadoPor: uid, creadoEn: 1, cifrado: { v: 1, sal: 's', verificador: 'v' }, settingsEnc: 'x' });
  b.set(doc(d, 'families', fid, 'members', uid), { uid, nombre: uid, email: null, rol: 'admin', unidoEn: 1 });
  b.set(doc(d, 'users', uid), { families: { [fid]: { nombre: 'Casa', rol: 'admin' } } }, { merge: true });
  await b.commit();
}

async function invitar(d: Firestore, uid: string, codigo: string, rol = 'admin', dias = 7) {
  await setDoc(doc(d, 'invites', codigo), {
    familyId: FID, familyNombre: 'Casa', rol, creadoPor: uid, expira: Timestamp.fromMillis(Date.now() + dias * 86400000),
  });
}

async function unirse(d: Firestore, uid: string, codigo: string, rol = 'admin', fid = FID) {
  const b = writeBatch(d);
  b.update(doc(d, 'invites', codigo), { usadoPor: uid });
  b.set(doc(d, 'families', fid, 'members', uid), { uid, nombre: uid, email: null, rol, unidoEn: 2, codigo });
  await b.commit();
}

beforeAll(async () => {
  env = await initializeTestEnvironment({
    projectId: 'demo-finanzas-familia',
    firestore: { rules: readFileSync('firestore.rules', 'utf8') },
  });
});
afterAll(() => env.cleanup());
beforeEach(async () => {
  await env.clearFirestore();
  await crearFamilia(db('sean'), 'sean', FID);
  await crearFamilia(db('rosa'), 'rosa', OTRA);
});

describe('creación de familias', () => {
  it('cualquiera puede crear su propia familia como administrador', async () => {
    await assertSucceeds(crearFamilia(db('nuevo'), 'nuevo', 'fam3'));
  });
  it('no se puede crear una familia a nombre de otro', async () => {
    const d = db('malo');
    const b = writeBatch(d);
    b.set(doc(d, 'families', 'fam4'), { nombre: 'X', creadoPor: 'sean', creadoEn: 1, cifrado: {}, settingsEnc: 'x' });
    b.set(doc(d, 'families', 'fam4', 'members', 'malo'), { uid: 'malo', rol: 'admin' });
    await assertFails(b.commit());
  });
  it('no se puede auto-agregar como admin a una familia existente', async () => {
    await assertFails(setDoc(doc(db('malo'), 'families', FID, 'members', 'malo'), { uid: 'malo', rol: 'admin' }));
  });
  it('sin sesión no se puede hacer nada', async () => {
    await assertFails(getDoc(doc(db(null), 'families', FID)));
    await assertFails(crearFamilia(db(null), 'x', 'fam5'));
  });
});

describe('aislamiento entre familias (centros de costo)', () => {
  beforeEach(async () => {
    await setDoc(doc(db('sean'), 'families', FID, 'gastos', 'g1'), raw('sean'));
  });
  it('un miembro lee y escribe en su familia', async () => {
    await assertSucceeds(getDoc(doc(db('sean'), 'families', FID)));
    await assertSucceeds(getDocs(collection(db('sean'), 'families', FID, 'gastos')));
    await assertSucceeds(setDoc(doc(db('sean'), 'families', FID, 'boletas', 'b1'), { enc: 'CIFRADO==', creadoPor: 'sean', creadoEn: 1 }));
  });
  it('otra familia no puede leer, listar ni escribir', async () => {
    const rosa = db('rosa');
    await assertFails(getDoc(doc(rosa, 'families', FID)));
    await assertFails(getDoc(doc(rosa, 'families', FID, 'gastos', 'g1')));
    await assertFails(getDocs(collection(rosa, 'families', FID, 'gastos')));
    await assertFails(getDocs(collection(rosa, 'families', FID, 'members')));
    await assertFails(setDoc(doc(rosa, 'families', FID, 'gastos', 'g2'), raw('rosa')));
    await assertFails(deleteDoc(doc(rosa, 'families', FID, 'gastos', 'g1')));
    await assertFails(updateDoc(doc(rosa, 'families', FID), { settingsEnc: 'robado' }));
  });
  it('nadie puede listar todas las familias ni leer el perfil de otro', async () => {
    await assertFails(getDocs(collection(db('rosa'), 'families')));
    await assertFails(getDoc(doc(db('rosa'), 'users', 'sean')));
  });
  it('los datos deben venir cifrados (sin campos en claro)', async () => {
    await assertFails(setDoc(doc(db('sean'), 'families', FID, 'gastos', 'g3'), { ...raw('sean'), monto: 5000, descripcion: 'pan' }));
  });
  it('no se puede registrar a nombre de otro miembro', async () => {
    await assertFails(setDoc(doc(db('sean'), 'families', FID, 'gastos', 'g4'), raw('daniela')));
  });
});

describe('invitaciones', () => {
  it('un admin invita; la pareja se une con el código y ve los datos', async () => {
    await assertSucceeds(invitar(db('sean'), 'sean', 'ABCD2345'));
    await assertSucceeds(unirse(db('daniela'), 'daniela', 'ABCD2345'));
    await assertSucceeds(getDoc(doc(db('daniela'), 'families', FID)));
    await assertSucceeds(setDoc(doc(db('daniela'), 'families', FID, 'gastos', 'gd'), raw('daniela')));
  });
  it('el código es de un solo uso', async () => {
    await invitar(db('sean'), 'sean', 'ABCD2345');
    await unirse(db('daniela'), 'daniela', 'ABCD2345');
    await assertFails(unirse(db('intruso'), 'intruso', 'ABCD2345'));
  });
  it('no se puede unir sin marcar el código como usado', async () => {
    await invitar(db('sean'), 'sean', 'ABCD2345');
    await assertFails(setDoc(doc(db('x'), 'families', FID, 'members', 'x'), { uid: 'x', rol: 'admin', codigo: 'ABCD2345' }));
  });
  it('no se puede elegir un rol distinto al de la invitación', async () => {
    await invitar(db('sean'), 'sean', 'MMMM2345', 'miembro');
    await assertFails(unirse(db('x'), 'x', 'MMMM2345', 'admin'));
    await assertSucceeds(unirse(db('x'), 'x', 'MMMM2345', 'miembro'));
  });
  it('un código de otra familia no sirve para entrar a esta', async () => {
    await invitar(db('sean'), 'sean', 'ABCD2345');
    await assertFails(unirse(db('x'), 'x', 'ABCD2345', 'admin', OTRA));
  });
  it('las invitaciones vencidas no sirven', async () => {
    await env.withSecurityRulesDisabled(async (c) => {
      await setDoc(doc(c.firestore(), 'invites', 'VIEJ2345'), {
        familyId: FID, familyNombre: 'Casa', rol: 'admin', creadoPor: 'sean', expira: Timestamp.fromMillis(Date.now() - 1000),
      });
    });
    await assertFails(unirse(db('x'), 'x', 'VIEJ2345'));
  });
  it('solo un admin de la familia puede invitar, y no se pueden listar códigos', async () => {
    await assertFails(setDoc(doc(db('rosa'), 'invites', 'ROSA2345'), {
      familyId: FID, familyNombre: 'Casa', rol: 'admin', creadoPor: 'rosa', expira: Timestamp.fromMillis(Date.now() + 86400000),
    }));
    await invitar(db('sean'), 'sean', 'ABCD2345', 'miembro');
    await unirse(db('hijo'), 'hijo', 'ABCD2345', 'miembro');
    await assertFails(invitar(db('hijo'), 'hijo', 'HIJO2345'));
    await assertFails(getDocs(collection(db('rosa'), 'invites')));
  });
});

describe('roles', () => {
  beforeEach(async () => {
    await invitar(db('sean'), 'sean', 'MMMM2345', 'miembro');
    await unirse(db('hijo'), 'hijo', 'MMMM2345', 'miembro');
  });
  it('un miembro edita el presupuesto pero no el nombre ni roles', async () => {
    await assertSucceeds(updateDoc(doc(db('hijo'), 'families', FID), { settingsEnc: 'nuevo' }));
    await assertFails(updateDoc(doc(db('hijo'), 'families', FID), { nombre: 'Otra' }));
    await assertFails(updateDoc(doc(db('hijo'), 'families', FID, 'members', 'hijo'), { rol: 'admin' }));
    await assertFails(deleteDoc(doc(db('hijo'), 'families', FID, 'members', 'sean')));
  });
  it('un admin cambia roles y quita miembros; quitado ya no ve nada', async () => {
    await assertSucceeds(updateDoc(doc(db('sean'), 'families', FID, 'members', 'hijo'), { rol: 'admin' }));
    await assertSucceeds(deleteDoc(doc(db('sean'), 'families', FID, 'members', 'hijo')));
    await assertFails(getDoc(doc(db('hijo'), 'families', FID)));
    await assertFails(unirse(db('hijo'), 'hijo', 'MMMM2345', 'miembro'));
  });
  it('cualquiera puede salirse', async () => {
    await assertSucceeds(deleteDoc(doc(db('hijo'), 'families', FID, 'members', 'hijo')));
  });
});
