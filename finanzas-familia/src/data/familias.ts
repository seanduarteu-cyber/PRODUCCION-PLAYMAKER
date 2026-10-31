import { cifrar, crearVerificador, derivarLlave, generarClaveFamilia, generarSal, guardarClave } from '../lib/crypto';
import { settingsIniciales } from '../lib/defaults';
import type { AppUser } from '../lib/types';
import type { Backend } from './backend';

/**
 * Crea una familia nueva (centro de costos) con su propia clave de cifrado.
 * La clave queda guardada en este dispositivo y se devuelve para mostrarla
 * una vez al usuario (debe guardarla e incluirla en las invitaciones).
 */
export async function crearFamiliaCifrada(backend: Backend, user: AppUser, nombre: string): Promise<{ id: string; clave: string }> {
  const clave = generarClaveFamilia();
  const sal = generarSal();
  const llave = await derivarLlave(clave, sal);
  const id = backend.newFamilyId();
  guardarClave(id, clave);
  await backend.createFamily(user, {
    nombre: nombre.trim(),
    creadoPor: user.uid,
    creadoEn: Date.now(),
    cifrado: { v: 1, sal, verificador: await crearVerificador(llave) },
    settingsEnc: await cifrar(llave, settingsIniciales()),
  }, id);
  return { id, clave };
}
