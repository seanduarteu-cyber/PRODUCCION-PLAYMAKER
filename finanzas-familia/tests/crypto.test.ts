import { describe, expect, it } from 'vitest';
import {
  cifrar, claveValida, crearVerificador, derivarLlave, descifrar, fmtClave, generarClaveFamilia, generarSal, verificarLlave,
} from '../src/lib/crypto';

describe('cifrado de la familia', () => {
  it('cifra y descifra con la clave correcta', async () => {
    const clave = generarClaveFamilia();
    expect(claveValida(clave)).toBe(true);
    expect(fmtClave(clave)).toMatch(/^[A-Z2-9]{4}(-[A-Z2-9]{4}){4}$/);
    const sal = generarSal();
    const llave = await derivarLlave(clave, sal);
    const dato = { monto: 66000, descripcion: 'almacén', fecha: '2026-10-30' };
    const texto = await cifrar(llave, dato);
    expect(texto).not.toContain('almac');
    expect(await descifrar(llave, texto)).toEqual(dato);
    // la clave se acepta con guiones o minúsculas
    const llave2 = await derivarLlave(fmtClave(clave).toLowerCase(), sal);
    expect(await descifrar(llave2, texto)).toEqual(dato);
  });

  it('cada cifrado es distinto (IV aleatorio)', async () => {
    const llave = await derivarLlave(generarClaveFamilia(), generarSal());
    expect(await cifrar(llave, 1)).not.toBe(await cifrar(llave, 1));
  });

  it('una clave incorrecta no descifra ni pasa el verificador', async () => {
    const sal = generarSal();
    const buena = await derivarLlave(generarClaveFamilia(), sal);
    const mala = await derivarLlave(generarClaveFamilia(), sal);
    const v = await crearVerificador(buena);
    expect(await verificarLlave(buena, v)).toBe(true);
    expect(await verificarLlave(mala, v)).toBe(false);
    await expect(descifrar(mala, await cifrar(buena, { x: 1 }))).rejects.toThrow();
  });
});
