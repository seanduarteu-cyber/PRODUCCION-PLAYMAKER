"""Arma un vbaProject.bin con código VBA propio, para guardar planillas .xlsm con macros desde openpyxl.

Parte de una plantilla hecha en Excel (_recursos/vba/plantilla_vbaProject.bin, del proyecto XlsxWriter, licencia
BSD) con los módulos ThisWorkbook, Sheet1, Sheet2 y Module1, y reemplaza el código de ThisWorkbook y de Module1.
Como en las herramientas de "purga" de VBA, se quita el código compilado (p-code) de cada módulo y se marca el
proyecto para que Excel lo vuelva a compilar desde el código fuente al abrir el archivo (_VBA_PROJECT con versión
0xFFFF, MODULEOFFSET en 0 y sin los streams __SRP_). El contenedor OLE se escribe de nuevo con escribir_cfb().

Uso desde un generador con openpyxl:
    from vba_proyecto import agregar_vba
    agregar_vba(wb, codigo_modulo, codigo_libro)   # antes de wb.save("archivo.xlsm")
La hoja que quieras asociar a un módulo de hoja usa ws.sheet_properties.codeName = "Sheet1" o "Sheet2".
"""

import io
import struct
import zipfile
from pathlib import Path

import olefile
from oletools.olevba import decompress_stream

PLANTILLA = Path(__file__).parent / "_recursos" / "vba" / "plantilla_vbaProject.bin"
CODEPAGE = "cp1252"


# ---------------------------------------------------------------- compresión MS-OVBA 2.4.1

def comprimir(datos: bytes) -> bytes:
    salida = bytearray(b"\x01")
    for ini in range(0, max(len(datos), 1), 4096):
        trozo = datos[ini:ini + 4096]
        cuerpo = _comprimir_trozo(trozo)
        if len(cuerpo) > 4096:  # trozo sin comprimir: siempre de 4096 bytes literales
            if len(trozo) < 4096:
                raise ValueError("Último trozo no comprimible: no se puede guardar sin rellenar")
            salida += struct.pack("<H", 0x0FFF | 0x3000) + trozo
        else:
            salida += struct.pack("<H", (len(cuerpo) + 2 - 3) | 0x3000 | 0x8000) + cuerpo
    return bytes(salida)


def _comprimir_trozo(d: bytes) -> bytes:
    out = bytearray()
    i, n = 0, len(d)
    while i < n:
        pos_flag = len(out)
        out.append(0)
        flag = 0
        for bit in range(8):
            if i >= n:
                break
            # largo de bits del offset según la posición dentro del trozo
            bits = max((i - 1).bit_length(), 4) if i > 0 else 4
            largo_max = (0xFFFF >> bits) + 3
            mejor_len, mejor_off = 0, 0
            for j in range(i - 1, max(-1, i - (1 << bits) - 1), -1):
                k = 0
                while i + k < n and k < largo_max and d[j + k] == d[i + k]:
                    k += 1
                if k > mejor_len:
                    mejor_len, mejor_off = k, i - j
            if mejor_len >= 3:
                token = ((mejor_off - 1) << (16 - bits)) | (mejor_len - 3)
                out += struct.pack("<H", token)
                flag |= 1 << bit
                i += mejor_len
            else:
                out.append(d[i])
                i += 1
        out[pos_flag] = flag
    return bytes(out)


# ---------------------------------------------------------------- stream dir

def _registros(dir_bytes: bytes):
    """Registros (id, datos) del stream dir. PROJECTVERSION (0x09) declara 4 bytes pero trae 6."""
    regs, i = [], 0
    while i < len(dir_bytes):
        rid, size = struct.unpack_from("<HI", dir_bytes, i)
        i += 6
        if rid == 0x0009:
            size = 6
        regs.append((rid, dir_bytes[i:i + size]))
        i += size
    return regs


def _dir_bytes(regs) -> bytes:
    out = bytearray()
    for rid, datos in regs:
        size = 4 if rid == 0x0009 else len(datos)
        out += struct.pack("<HI", rid, size) + datos
    return bytes(out)


# ---------------------------------------------------------------- contenedor OLE (CFB versión 3)

def escribir_cfb(streams: dict) -> bytes:
    """streams: {"PROJECT": bytes, "VBA/dir": bytes, ...} (una carpeta como máximo). Todo va al mini stream si
    pesa menos de 4096 bytes."""
    SECT, MINI, CORTE = 512, 64, 4096
    FREE, END, FATSECT, NOSTREAM = 0xFFFFFFFF, 0xFFFFFFFE, 0xFFFFFFFD, 0xFFFFFFFF

    # entradas de directorio: raíz, carpetas y streams
    entradas = [{"nombre": "Root Entry", "tipo": 5, "hijos": []}]
    carpetas = {}
    for ruta, datos in streams.items():
        partes = ruta.split("/")
        padre = entradas[0]
        if len(partes) == 2:
            if partes[0] not in carpetas:
                c = {"nombre": partes[0], "tipo": 1, "hijos": []}
                carpetas[partes[0]] = c
                entradas.append(c)
                entradas[0]["hijos"].append(c)
            padre = carpetas[partes[0]]
        e = {"nombre": partes[-1], "tipo": 2, "datos": datos, "hijos": []}
        entradas.append(e)
        padre["hijos"].append(e)
    for k, e in enumerate(entradas):
        e["id"] = k

    # mini stream
    mini, minifat = bytearray(), []
    for e in entradas:
        if e["tipo"] == 2 and len(e["datos"]) < CORTE:
            e["inicio"] = len(mini) // MINI if e["datos"] else END
            nsec = (len(e["datos"]) + MINI - 1) // MINI
            for s in range(nsec):
                minifat.append(len(minifat) + 1 if s < nsec - 1 else END)
            mini += e["datos"].ljust(nsec * MINI, b"\x00")
    grandes = [e for e in entradas if e["tipo"] == 2 and len(e["datos"]) >= CORTE]

    def sectores(n_bytes):
        return (n_bytes + SECT - 1) // SECT

    n_dir = sectores(len(entradas) * 128)
    n_minifat = sectores(len(minifat) * 4)
    n_mini = sectores(len(mini))
    n_grandes = sum(sectores(len(e["datos"])) for e in grandes)
    n_fat = 1
    while n_fat * 128 < n_fat + n_dir + n_minifat + n_mini + n_grandes:
        n_fat += 1
    fat = [FATSECT] * n_fat
    cuerpo = bytearray()

    def cadena(datos):
        inicio = len(fat)
        n = sectores(len(datos))
        for s in range(n):
            fat.append(inicio + s + 1 if s < n - 1 else END)
        cuerpo.extend(bytes(datos).ljust(n * SECT, b"\x00"))
        return inicio if n else END

    # directorio: árbol binario de búsqueda balanceado (todo negro) por hermanos
    def clave(e):
        return (len(e["nombre"]), e["nombre"].upper())

    def arbol(nodos):
        if not nodos:
            return NOSTREAM
        nodos = sorted(nodos, key=clave)
        m = len(nodos) // 2
        nodos[m]["izq"] = arbol(nodos[:m])
        nodos[m]["der"] = arbol(nodos[m + 1:])
        return nodos[m]["id"]

    for e in entradas:
        e["hijo"] = arbol(e["hijos"]) if e["tipo"] in (1, 5) else NOSTREAM
    entradas[0].setdefault("izq", NOSTREAM)
    entradas[0].setdefault("der", NOSTREAM)

    inicio_dir_placeholder = len(fat)
    dir_bytes = bytearray(n_dir * SECT)
    inicio_dir = cadena(dir_bytes)
    inicio_minifat = cadena(b"".join(struct.pack("<I", x) for x in minifat)) if minifat else END
    inicio_mini = cadena(mini) if mini else END
    for e in grandes:
        e["inicio"] = cadena(e["datos"])
    entradas[0]["inicio"] = inicio_mini
    entradas[0]["datos"] = bytes(mini)

    dir_bytes = bytearray()
    for e in entradas:
        nombre = e["nombre"].encode("utf-16-le") + b"\x00\x00"
        tam = len(e["datos"]) if e["tipo"] in (2, 5) else 0
        dir_bytes += struct.pack("<64sHBB3I16sI8s8sIII", nombre.ljust(64, b"\x00"), len(nombre), e["tipo"], 1,
                                 e.get("izq", NOSTREAM), e.get("der", NOSTREAM), e["hijo"], b"\x00" * 16, 0,
                                 b"\x00" * 8, b"\x00" * 8, e.get("inicio", END) if e["tipo"] != 1 else 0, tam, 0)
    for _ in range(n_dir * 4 - len(entradas)):
        dir_bytes += struct.pack("<64sHBB3I16sI8s8sIII", b"\x00" * 64, 0, 0, 0, NOSTREAM, NOSTREAM, NOSTREAM,
                                 b"\x00" * 16, 0, b"\x00" * 8, b"\x00" * 8, 0, 0, 0)
    off = (inicio_dir - n_fat) * SECT
    cuerpo[off:off + len(dir_bytes)] = dir_bytes
    assert inicio_dir_placeholder == inicio_dir

    fat += [FREE] * (n_fat * 128 - len(fat))
    difat = list(range(n_fat)) + [FREE] * (109 - n_fat)
    cabecera = struct.pack("<8s16sHHHHH6sIIIIIIIII", b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", b"\x00" * 16, 0x3E, 3,
                           0xFFFE, 9, 6, b"\x00" * 6, 0, n_fat, inicio_dir, 0, CORTE, inicio_minifat,
                           n_minifat, END, 0)
    cabecera += b"".join(struct.pack("<I", x) for x in difat)
    return cabecera + b"".join(struct.pack("<I", x) for x in fat) + bytes(cuerpo)


# ---------------------------------------------------------------- proyecto

def proyecto_vba(codigo_modulo: str, codigo_libro: str = "") -> bytes:
    """vbaProject.bin con el código de Module1 (macros) y de ThisWorkbook (eventos del libro)."""
    ole = olefile.OleFileIO(str(PLANTILLA))
    dir_viejo = decompress_stream(bytearray(ole.openstream("VBA/dir").read()))
    regs = _registros(dir_viejo)
    # módulos: nombre del stream y offset del código fuente en ese stream
    modulos, actual = [], None
    for k, (rid, datos) in enumerate(regs):
        if rid == 0x001A:
            actual = {"stream": datos.decode(CODEPAGE)}
        elif rid == 0x0031 and actual is not None:
            actual["offset"], actual["reg"] = struct.unpack("<I", datos)[0], k
            modulos.append(actual)
            actual = None
    nuevos = {"Module1": codigo_modulo, "ThisWorkbook": codigo_libro}
    streams = {"PROJECT": ole.openstream("PROJECT").read(), "PROJECTwm": ole.openstream("PROJECTwm").read(),
               "VBA/_VBA_PROJECT": b"\xCC\x61\xFF\xFF\x00\x00\x00"}
    for m in modulos:
        crudo = ole.openstream("VBA/" + m["stream"]).read()
        fuente = decompress_stream(bytearray(crudo[m["offset"]:])).decode(CODEPAGE)
        if m["stream"] in nuevos and nuevos[m["stream"]]:
            # se conservan las líneas Attribute de la plantilla y se reemplaza el código
            attrs = [ln for ln in fuente.replace("\r\n", "\n").split("\n") if ln.startswith("Attribute ")]
            cuerpo = nuevos[m["stream"]].replace("\r\n", "\n").strip("\n")
            fuente = "\r\n".join(attrs + cuerpo.split("\n")) + "\r\n"
        streams["VBA/" + m["stream"]] = comprimir(fuente.encode(CODEPAGE))
        regs[m["reg"]] = (0x0031, struct.pack("<I", 0))
    streams["VBA/dir"] = comprimir(_dir_bytes(regs))
    ole.close()
    return escribir_cfb(streams)


def agregar_vba(wb, codigo_modulo: str, codigo_libro: str = "") -> None:
    """Deja el workbook de openpyxl listo para guardarse como .xlsm con estas macros."""
    tipos = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             '<Default Extension="bin" ContentType="application/vnd.ms-office.vbaProject"/>'
             '<Override PartName="/xl/vbaProject.bin" ContentType="application/vnd.ms-office.vbaProject"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", tipos)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/vbaProject.bin", proyecto_vba(codigo_modulo, codigo_libro))
    buf.seek(0)
    wb.vba_archive = zipfile.ZipFile(buf)
    wb.code_name = "ThisWorkbook"
