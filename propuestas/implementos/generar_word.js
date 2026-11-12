// Catálogo técnico de implementos en Word (editable), con el diseño del catálogo PDF.
// Uso: node propuestas/implementos/generar_word.js   ->  Catalogo_Implementos_Rugby.docx
// Textos: catalogo.json (compartido con el PDF). Las fotos salen de fotos/ y los logos de ../_recursos/.

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, Header, Footer,
  AlignmentType, WidthType, ShadingType, BorderStyle, LevelFormat, PageNumber, PageBreak,
  TabStopType, VerticalAlign, TableLayoutType,
} = require("docx");

const DIR = __dirname;
const REC = path.join(DIR, "..", "_recursos");
const NAVY = "141E3C", ORO = "B1A542", GRIS = "6E7280", TEXTO = "3A3F52", LINEA = "DCD8CB", MARFIL = "F7F3E7";
const TITULO = "Georgia", CUERPO = "Arial";
const ANCHO = 9638; // A4 (11906) menos márgenes de 2 cm (1134 x 2), en DXA
const PX = ANCHO / 15; // ancho útil en píxeles de imagen (1 px = 15 DXA)

// ---------------------------------------------------------------- contenido

// mismo contenido que el PDF (generar_html.js): textos, fotos y especificaciones
const CATALOGO = JSON.parse(fs.readFileSync(path.join(DIR, "catalogo.json"), "utf8"));
const CONFIRMAR = "a confirmar";

// ---------------------------------------------------------------- utilidades

function tamanoJpeg(buf) { // ancho y alto de un JPEG (marcador SOF)
  let i = 2;
  while (i < buf.length) {
    const marcador = buf[i + 1], largo = buf.readUInt16BE(i + 2);
    if (marcador >= 0xc0 && marcador <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(marcador)) {
      return { alto: buf.readUInt16BE(i + 5), ancho: buf.readUInt16BE(i + 7) };
    }
    i += 2 + largo;
  }
  throw new Error("JPEG sin tamaño");
}

function tamanoPng(buf) { return { ancho: buf.readUInt32BE(16), alto: buf.readUInt32BE(20) }; }

function imagen(archivo, alto) {
  const buf = fs.readFileSync(archivo);
  const png = archivo.endsWith(".png");
  const t = png ? tamanoPng(buf) : tamanoJpeg(buf);
  return new ImageRun({ type: png ? "png" : "jpg", data: buf,
    transformation: { width: Math.round(alto * t.ancho / t.alto), height: alto },
    altText: { title: path.basename(archivo), description: path.basename(archivo), name: path.basename(archivo) } });
}

const SIN_BORDE = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const SIN_BORDES = { top: SIN_BORDE, bottom: SIN_BORDE, left: SIN_BORDE, right: SIN_BORDE };
const BORDE_FINO = { style: BorderStyle.SINGLE, size: 4, color: LINEA };

function t(texto, o = {}) { return new TextRun({ text: texto, font: o.font || CUERPO, size: o.size || 18, color: o.color || TEXTO, ...o }); }

function confirmar(detalle) {
  const texto = detalle ? `${CONFIRMAR}: ${detalle}` : CONFIRMAR;
  return new TextRun({ text: ` ${texto.toUpperCase()} `, font: CUERPO, size: 13, bold: true, color: "5A4A00",
    shading: { type: ShadingType.CLEAR, color: "auto", fill: "FFF2A8" }, characterSpacing: 10 });
}

function etiqueta(texto, color = ORO, size = 14) {
  return t(texto.toUpperCase(), { size, bold: true, color, characterSpacing: 40 });
}

function kicker(izq, der) {
  return new Paragraph({
    tabStops: [{ type: TabStopType.RIGHT, position: ANCHO }],
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINEA, space: 6 } },
    spacing: { after: 240 },
    children: [etiqueta(izq), new TextRun({ text: "\t" }), etiqueta(der, GRIS)],
  });
}

function titulo(texto, size = 44) {
  return new Paragraph({ keepNext: true, spacing: { after: 60 },
    children: [t(texto, { font: TITULO, size, bold: true, color: NAVY })] });
}

function bajada(texto) {
  return new Paragraph({ spacing: { after: 240 }, children: [t(texto, { font: TITULO, size: 22, italics: true, color: "8A8672" })] });
}

function parrafo(texto, o = {}) {
  return new Paragraph({ spacing: { after: 160, line: 300 }, children: [t(texto, { size: 19, ...o })] });
}

function celda(children, ancho, o = {}) {
  return new TableCell({ width: { size: ancho, type: WidthType.DXA }, children,
    margins: { top: 90, bottom: 90, left: 120, right: 120 }, verticalAlign: VerticalAlign.CENTER, ...o });
}

function tabla(columnas, filas, o = {}) {
  return new Table({ width: { size: ANCHO, type: WidthType.DXA }, columnWidths: columnas, layout: TableLayoutType.FIXED,
    rows: filas, ...o });
}

function filaCabecera(textos, columnas, alineaciones = []) {
  return new TableRow({ tableHeader: true, children: textos.map((x, i) => celda(
    [new Paragraph({ alignment: alineaciones[i] || AlignmentType.LEFT, children: [etiqueta(x, "FFFFFF", 13)] })], columnas[i],
    { shading: { type: ShadingType.CLEAR, color: "auto", fill: NAVY }, borders: { top: SIN_BORDE, left: SIN_BORDE, right: SIN_BORDE, bottom: SIN_BORDE } })) });
}

const bordesFila = { top: SIN_BORDE, left: SIN_BORDE, right: SIN_BORDE, bottom: BORDE_FINO };

function fotos(lista, alto) {
  // todas a la misma altura; cada columna mide lo que su foto (más un margen) y el sobrante se reparte
  const aspectos = lista.map(f => { const d = tamanoJpeg(fs.readFileSync(path.join(DIR, "fotos", f))); return d.ancho / d.alto; });
  const margen = 12;
  const altoFinal = Math.min(alto, Math.floor((PX - margen * lista.length) / aspectos.reduce((a, b) => a + b, 0)));
  const anchos = aspectos.map(a => Math.round((altoFinal * a + margen) * 15));
  const extra = Math.floor((ANCHO - anchos.reduce((a, b) => a + b, 0)) / lista.length);
  const columnas = anchos.map(a => a + extra);
  columnas[columnas.length - 1] += ANCHO - columnas.reduce((a, b) => a + b, 0);
  return tabla(columnas, [new TableRow({ children: lista.map((f, i) => celda(
    [new Paragraph({ alignment: AlignmentType.CENTER, children: [imagen(path.join(DIR, "fotos", f), altoFinal)] })], columnas[i],
    { borders: SIN_BORDES, shading: { type: ShadingType.CLEAR, color: "auto", fill: "FAF9F5" }, margins: { top: 80, bottom: 80, left: 40, right: 40 } })) })],
  { borders: { top: BORDE_FINO, bottom: BORDE_FINO, left: BORDE_FINO, right: BORDE_FINO, insideHorizontal: SIN_BORDE, insideVertical: SIN_BORDE } });
}

function marcas(altoPm, altoPz, separador = LINEA) {
  return [imagen(path.join(REC, "playmaker_logo_horizontal_navy.png"), altoPm),
          new TextRun({ text: "   |   ", font: CUERPO, size: Math.round(altoPm * 0.9), color: separador }),
          imagen(path.join(REC, "proeza_logo_azul.png"), altoPz)];
}

const salto = () => new Paragraph({ children: [new PageBreak()] });

// ---------------------------------------------------------------- páginas

function portada() {
  const c = CATALOGO.fichas, p = CATALOGO.portada;
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 1400 }, children: marcas(44, 27) }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [etiqueta(p.kicker, ORO, 17)] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: p.titulo.map((linea, k) => t(linea, { font: TITULO, size: 64, bold: true, color: NAVY, ...(k ? { break: 1 } : {}) })) }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 900 },
      children: [t(p.subtitulo,
        { font: TITULO, size: 24, italics: true, color: "8A8672" })] }),
    fotos(p.tira.map(f => f.archivo), 230),
    ...(p.estado ? [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 80 }, children: [etiqueta(p.estado, ORO, 15)] })] : []),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: p.estado ? 0 : 900 }, children: [t(p.fecha, { size: 16, color: GRIS })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200 },
      children: [t(`${c.length} productos · ${c.map(f => f.codigo).join(" · ")}`, { size: 14, color: GRIS })] }),
    salto(),
  ];
}

function linea() {
  const col = [1150, 2550, 4738, 1200];
  const filas = CATALOGO.fichas.map((f, i) => new TableRow({ children: [
    celda([new Paragraph({ children: [t(f.codigo, { font: TITULO, size: 18, color: GRIS })] })], col[0], { borders: bordesFila }),
    celda([new Paragraph({ children: [t(f.titulo, { size: 18, bold: true, color: NAVY })] })], col[1], { borders: bordesFila }),
    celda([new Paragraph({ children: [t(f.usoCorto, { size: 18 })] })], col[2], { borders: bordesFila }),
    celda([new Paragraph({ alignment: AlignmentType.RIGHT, children: [t(`Ficha ${String(i + 1).padStart(2, "0")}`, { size: 17, color: GRIS })] })], col[3], { borders: bordesFila }),
  ] }));
  const colC = [2400, ANCHO - 2400];
  const criterios = CATALOGO.linea.criterios.map(([k, v]) => new TableRow({ children: [
    celda([new Paragraph({ children: [etiqueta(k, MARFIL, 13)] })], colC[0], { shading: { type: ShadingType.CLEAR, color: "auto", fill: NAVY }, borders: SIN_BORDES }),
    celda([new Paragraph({ children: [t(v, { size: 18, color: "C9C4B4" })] })], colC[1], { shading: { type: ShadingType.CLEAR, color: "auto", fill: NAVY }, borders: SIN_BORDES }),
  ] }));
  return [
    kicker("Sección 01", "Línea de equipamiento"),
    titulo(CATALOGO.linea.titulo),
    parrafo(CATALOGO.linea.intro),
    tabla(col, [filaCabecera(["Código", "Producto", "Uso", "Ficha"], col, [, , , AlignmentType.RIGHT]), ...filas]),
    new Paragraph({ spacing: { before: 400, after: 140 }, children: [etiqueta("Criterios comunes a toda la línea")] }),
    tabla(colC, criterios, { borders: { top: SIN_BORDE, bottom: SIN_BORDE, left: SIN_BORDE, right: SIN_BORDE, insideHorizontal: SIN_BORDE, insideVertical: SIN_BORDE } }),
    new Paragraph({ spacing: { before: 360, after: 80 }, children: [etiqueta("Fotos de referencia")] }),
    parrafo(CATALOGO.linea.notaFotos),
    salto(),
  ];
}

function ficha(f, i) {
  const col = [2300, ANCHO - 2300];
  const filas = f.specs.map(([k, v, pendiente]) => new TableRow({ cantSplit: true, children: [
    celda([new Paragraph({ children: [etiqueta(k, NAVY, 13)] })], col[0], { borders: bordesFila, verticalAlign: VerticalAlign.TOP }),
    celda([new Paragraph({ spacing: { line: 276 }, children: [t(v, { size: 18 }), ...(pendiente !== undefined ? [t(" "), confirmar(pendiente)] : [])] })],
      col[1], { borders: bordesFila, verticalAlign: VerticalAlign.TOP }),
  ] }));
  const bloques = [
    kicker(`Ficha ${String(i + 1).padStart(2, "0")} · ${f.categoria}`, f.codigo),
    titulo(f.titulo),
    bajada(f.bajada),
    fotos(f.fotos.archivos.map(x => x.archivo), f.fotos.altoWord),
    new Paragraph({ spacing: { before: 80, after: 220 }, children: [t(f.leyenda, { size: 14, italics: true, color: GRIS })] }),
    new Paragraph({ spacing: { after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINEA, space: 6 } },
      tabStops: [{ type: TabStopType.LEFT, position: 1100 }], indent: { left: 1100, hanging: 1100 },
      children: [etiqueta("Uso"), new TextRun({ text: "\t" }), t(f.uso, { size: 19, color: "1C2233" })] }),
    tabla(col, filas),
  ];
  if (f.medidas) {
    const n = f.medidas.valores.length, c = Math.floor(ANCHO / n);
    const colM = Array.from({ length: n }, (_, k) => (k === n - 1 ? ANCHO - c * (n - 1) : c));
    bloques.push(
      new Paragraph({ spacing: { before: 300, after: 100 }, children: [etiqueta(f.medidas.titulo, NAVY, 13), ...(f.medidas.pendiente !== undefined ? [t("  "), confirmar(f.medidas.pendiente)] : [])] }),
      tabla(colM, [new TableRow({ children: f.medidas.valores.map(([k, v], j) => celda([
        new Paragraph({ children: [t(k.toUpperCase(), { size: 12, color: GRIS, characterSpacing: 20 })] }),
        new Paragraph({ children: [t(v, { size: 19, bold: true, color: NAVY })] }),
      ], colM[j], { borders: { top: BORDE_FINO, bottom: BORDE_FINO, left: BORDE_FINO, right: BORDE_FINO } })) })]),
    );
  }
  if (i < CATALOGO.fichas.length - 1 || CATALOGO.revision.incluir !== false) bloques.push(salto()); // sin hoja en blanco al final
  return bloques;
}

function revision() {
  const r = CATALOGO.revision;
  const lista = (items, ref) => items.map(x => new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 100, line: 300 }, children: [t(x, { size: 19 })] }));
  return [
    kicker("Para revisión interna", "No va en la versión final"),
    titulo("Notas para la revisión"),
    parrafo(r.intro),
    new Paragraph({ spacing: { before: 240, after: 120 }, children: [etiqueta("Pendiente")] }),
    ...lista(r.pendientes, "pendientes"),
    new Paragraph({ spacing: { before: 240, after: 120 }, children: [etiqueta("Antes de enviarlo a un club")] }),
    ...lista(r.antesDeEnviar, "enviar"),
    new Paragraph({ spacing: { before: 300 }, shading: { type: ShadingType.CLEAR, color: "auto", fill: "FFF8D6" },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: ORO, space: 8 } },
      children: [t(r.aviso, { size: 18 })] }),
  ];
}

// ---------------------------------------------------------------- documento

const cabecera = new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: marcas(16, 10) })] });
const pie = new Footer({ children: [new Paragraph({
  tabStops: [{ type: TabStopType.RIGHT, position: ANCHO }],
  border: { top: { style: BorderStyle.SINGLE, size: 4, color: LINEA, space: 6 } },
  children: [t("UN CLUB, UNA FAMILIA.", { size: 12, color: GRIS, characterSpacing: 30 }), new TextRun({ text: "\t" }),
             new TextRun({ children: [PageNumber.CURRENT], font: TITULO, size: 17, color: NAVY })],
})] });
const vacio = () => new Paragraph({ children: [] });

const numeracion = ["pendientes", "enviar"].map(reference => ({ reference, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
  alignment: AlignmentType.LEFT, style: { run: { color: ORO, bold: true, font: CUERPO }, paragraph: { indent: { left: 400, hanging: 300 } } } }] }));

const doc = new Document({
  creator: "Playmaker · Proeza",
  title: "Catálogo técnico: balones e implementos de rugby",
  styles: { default: { document: { run: { font: CUERPO, size: 18, color: TEXTO } } } },
  numbering: { config: numeracion },
  sections: [{
    properties: { titlePage: true, page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1000, left: 1134, right: 1134, header: 560, footer: 500 } } },
    headers: { default: cabecera, first: new Header({ children: [vacio()] }) },
    footers: { default: pie, first: new Footer({ children: [vacio()] }) },
    children: [...portada(), ...linea(), ...CATALOGO.fichas.flatMap(ficha), ...(CATALOGO.revision.incluir === false ? [] : revision())],
  }],
});

const salida = path.join(DIR, "Catalogo_Implementos_Rugby.docx");
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(salida, buf); console.log(`OK  ${salida}`); });
