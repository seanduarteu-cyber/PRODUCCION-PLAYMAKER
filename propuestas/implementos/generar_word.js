// Catálogo técnico de implementos en Word (editable), con el diseño del catálogo PDF.
// Uso: node propuestas/implementos/generar_word.js   ->  Catalogo_Implementos_Rugby.docx
// Textos: editar CATALOGO, más abajo. Las fotos salen de fotos/ y los logos de ../_recursos/.

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

const CONFIRMAR = "a confirmar";
const CATALOGO = {
  intro: "Cinco productos para cubrir el entrenamiento de contacto y la cancha del club: balones, escudos, " +
    "sacos y aros de tackle, y protectores de poste. Cada pieza se fabrica a pedido, con los colores, el escudo " +
    "y el nombre del club, y con materiales pensados para el uso diario a la intemperie.",
  criterios: [
    ["Exterior", "Lona de PVC con trama antidesgarro o cuero sintético: impermeable, lavable y resistente a la abrasión."],
    ["Relleno", "Espuma de alta densidad que absorbe el impacto sin deformarse."],
    ["Costuras", "Costuras reforzadas en uniones, asas y correas, que son las zonas de mayor exigencia."],
    ["Personalización", "Colores, escudo, nombre del club y auspiciadores en cada pieza."],
    ["Fabricación", "A pedido, con el diseño aprobado por el club antes de producir."],
  ],
  notaFotos: "Las fotos de este catálogo muestran trabajos realizados para otros clubes y sirven como referencia " +
    "de forma y terminaciones. Cada pedido se produce con el diseño propio del club.",
  fichas: [
    {
      codigo: "IMP-01", categoria: "BALONES", titulo: "Balón de rugby Match",
      bajada: "Talla 5, de caucho con grip en relieve y diseño a pedido",
      usoCorto: "Partido y entrenamiento en todas las categorías",
      fotos: ["balon_match_proeza.jpg", "balon_condor_cara.jpg", "balon_fucsia_turquesa_1.jpg"], altoFotos: 220,
      leyenda: "Diseños de referencia. Cada balón se produce con los colores, el escudo y las frases del club.",
      uso: "Partido y entrenamiento en todas las categorías.",
      specs: [
        ["Construcción", "4 paneles cosidos a máquina."],
        ["Cubierta", "Caucho sintético con grip de puntos en relieve en toda la superficie, para un agarre firme con lluvia y barro."],
        ["Interior", "Capas de tela laminada que mantienen la forma y cámara con válvula.", "material de la cámara"],
        ["Personalización", "Diseño completo de la cubierta: colores, escudo, nombre y frases del club."],
        ["Tallas", "Talla 5 para juveniles y adultos; tallas 3 y 4 para infantiles.", ""],
      ],
      medidas: {
        titulo: "Medidas de referencia · talla 5 · reglamento World Rugby",
        nota: "con la ficha del taller",
        valores: [["Largo", "280–300 mm"], ["Circ. longitudinal", "740–770 mm"], ["Circ. transversal", "580–620 mm"],
                  ["Peso", "410–460 g"], ["Presión", "9,5–10 psi"]],
      },
    },
    {
      codigo: "IMP-02", categoria: "CONTACTO", titulo: "Escudo de tackle",
      bajada: "Perfil anatómico, lona de PVC y relleno de alta densidad",
      usoCorto: "Contacto, tackle y ruck: un jugador lo sostiene y recibe el impacto",
      fotos: ["escudo_tackle_old_gergel_frente.jpg", "escudo_tackle_frances_espalda.jpg", "escudo_tackle_palestina.jpg"], altoFotos: 300,
      leyenda: "Lateral con nombre del club, espalda con correas y versión en otros colores. Trabajos realizados para otros clubes.",
      uso: "Entrenamiento de contacto, tackle y ruck: un jugador lo sostiene y recibe el impacto.",
      specs: [
        ["Forma", "Perfil anatómico con cabezal más grueso arriba, que protege la cabeza y el hombro de quien lo sostiene."],
        ["Exterior", "Cara de impacto y laterales en lona de PVC con trama antidesgarro; espalda en cuero sintético liso, más cómoda contra el cuerpo."],
        ["Relleno", "Espuma de alta densidad que absorbe el golpe sin deformarse.", "densidad y espesor"],
        ["Ventilación", "Perforaciones en los laterales que dejan salir el aire con cada impacto: el escudo no rebota y las costuras no se revientan."],
        ["Agarre", "Dos correas para los brazos en la espalda y manilla lateral de traslado, en cinta de polipropileno con costura reforzada en cruz."],
        ["Personalización", "Color de la cara de impacto, nombre del club en vertical en el lateral y escudo."],
        ["Medidas", "Alto 80–90 cm; ancho 40 cm; espesor 20 cm en el cuerpo y 30 cm en el cabezal.", ""],
      ],
    },
    {
      codigo: "IMP-03", categoria: "CONTACTO", titulo: "Saco de tackle",
      bajada: "Cilindro de contacto en dos alturas, para tacklear y llevar al suelo",
      usoCorto: "Tackle y llevada al suelo sin un compañero que sostenga",
      fotos: ["sacos_y_protector_stade_francais.jpg", "saco_y_escudo_varc.jpg"], altoFotos: 360,
      leyenda: "Pedidos en lona de PVC (azul, en varias alturas) y en cuero sintético (negro). Trabajos realizados para otros clubes.",
      uso: "Práctica de tackle y llevada al suelo sin un compañero que sostenga.",
      specs: [
        ["Forma", "Cilindro con tapa y fondo cosidos y manilla en la tapa para trasladarlo."],
        ["Exterior", "Lona de PVC con trama antidesgarro o cuero sintético; impermeable y lavable."],
        ["Relleno", "Espuma de alta densidad en capas, firme y sin zonas blandas.", ""],
        ["Alturas", "Saco alto para juveniles y adultos; saco corto para infantiles o trabajo de ruck."],
        ["Personalización", "Color del cuerpo y escudo o nombre del club en gran formato."],
        ["Medidas", "Alto 1,2–1,4 m (saco alto) y 50–60 cm (saco corto); diámetro 35–40 cm.", ""],
      ],
    },
    {
      codigo: "IMP-04", categoria: "CONTACTO", titulo: "Aro de tackle",
      bajada: "Anillo acolchado para tacklear un objetivo en movimiento",
      usoCorto: "Tackle sobre un objetivo en movimiento",
      fotos: ["aro_tackle_frente.jpg", "aro_tackle_lateral.jpg"], altoFotos: 360,
      leyenda: "Vista frontal y lateral. Trabajo realizado para otro club.",
      uso: "Se hace rodar para que el jugador lo persiga y lo tacklee en movimiento; trabaja lectura, timing y técnica de tackle.",
      specs: [
        ["Forma", "Anillo de gran diámetro con centro abierto, firme para rodar recto."],
        ["Exterior", "Lona de PVC con trama antidesgarro y costuras perimetrales reforzadas."],
        ["Relleno", "Espuma de alta densidad."],
        ["Personalización", "Nombre y logo del club en ambas caras."],
        ["Medidas", "Diámetro exterior 1 m; espesor del anillo 25–30 cm.", ""],
      ],
    },
    {
      codigo: "IMP-05", categoria: "CANCHA", titulo: "Protector de poste",
      bajada: "Funda acolchada de sección cuadrada, con cuatro caras para el club y sus auspiciadores",
      usoCorto: "Protección de los jugadores en la base de los postes de las H",
      fotos: ["protector_poste_curico.jpg", "protector_poste_auspiciador.jpg"], altoFotos: 360,
      leyenda: "Cara con el escudo del club y cara con auspiciador. Trabajos realizados para otros clubes.",
      uso: "Protege a los jugadores en los choques contra la base de los postes de las H.",
      specs: [
        ["Forma", "Sección cuadrada con abertura central para el poste y tapa superior."],
        ["Exterior", "Lona de PVC con trama antidesgarro, apta para estar a la intemperie."],
        ["Relleno", "Espuma de alta densidad."],
        ["Cierre", "A lo largo de una arista, para instalarlo y retirarlo.", "velcro o cierre"],
        ["Reglamento", "World Rugby permite que el acolchado sobresalga como máximo 300 mm desde la línea de gol."],
        ["Personalización", "Las cuatro caras se imprimen con escudo, nombre del club y auspiciadores; un auspiciador puede financiar el set."],
        ["Venta y medidas", "Set de 4 protectores por cancha, dos por cada H; alto 1,5–1,8 m.", ""],
      ],
    },
  ],
  revision: {
    taller: [
      "Medidas reales y peso de cada producto.",
      "Densidad y espesor de la espuma; gramaje de la lona de PVC.",
      "Material de la cámara del balón y tallas disponibles (3, 4 y 5).",
      "Tipo de cierre del protector de poste: velcro o cierre.",
      "Si la pieza cuadrada del pedido de Stade Français es un protector de poste o un saco de sección cuadrada.",
      "Si el tee de pateo azul que aparece bajo los balones también es parte de la oferta.",
      "Costo, mínimo por diseño personalizado y plazo de entrega de cada producto.",
    ],
    antesDeEnviar: [
      "Las fotos muestran el nombre y el escudo de otros clubes. Para la versión final: montajes con los colores y el escudo del club, o permiso de esos clubes para mostrarlos como trabajos realizados.",
      "Agregar precios por producto, o por set (por ejemplo, set de 4 protectores de poste).",
    ],
    aviso: "Los balones les sirven a los socios y pueden ir en la preventa del club. Escudos, sacos, aros y " +
      "protectores los compra el club: conviene presentarlos como una línea aparte de equipamiento institucional.",
  },
};

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
  const c = CATALOGO.fichas;
  const tira = ["balon_match_proeza_crouch_bind_set.jpg", "escudo_tackle_palestina.jpg", "aro_tackle_frente.jpg", "protector_poste_curico.jpg"];
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 1400 }, children: marcas(44, 27) }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [etiqueta("Catálogo técnico", ORO, 17)] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: [t("Balones e implementos", { font: TITULO, size: 64, bold: true, color: NAVY }),
                 t("de rugby", { font: TITULO, size: 64, bold: true, color: NAVY, break: 1 })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 900 },
      children: [t("Equipamiento de entrenamiento y cancha, personalizado con los colores y el escudo de cada club",
        { font: TITULO, size: 24, italics: true, color: "8A8672" })] }),
    fotos(tira, 230),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 80 }, children: [etiqueta("Borrador para revisión", ORO, 15)] }),
    new Paragraph({ alignment: AlignmentType.CENTER, children: [t("Noviembre 2026", { size: 16, color: GRIS })] }),
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
  const criterios = CATALOGO.criterios.map(([k, v]) => new TableRow({ children: [
    celda([new Paragraph({ children: [etiqueta(k, MARFIL, 13)] })], colC[0], { shading: { type: ShadingType.CLEAR, color: "auto", fill: NAVY }, borders: SIN_BORDES }),
    celda([new Paragraph({ children: [t(v, { size: 18, color: "C9C4B4" })] })], colC[1], { shading: { type: ShadingType.CLEAR, color: "auto", fill: NAVY }, borders: SIN_BORDES }),
  ] }));
  return [
    kicker("Sección 01", "Línea de equipamiento"),
    titulo("Equipamiento para entrenar y jugar"),
    parrafo(CATALOGO.intro),
    tabla(col, [filaCabecera(["Código", "Producto", "Uso", "Ficha"], col, [, , , AlignmentType.RIGHT]), ...filas]),
    new Paragraph({ spacing: { before: 400, after: 140 }, children: [etiqueta("Criterios comunes a toda la línea")] }),
    tabla(colC, criterios, { borders: { top: SIN_BORDE, bottom: SIN_BORDE, left: SIN_BORDE, right: SIN_BORDE, insideHorizontal: SIN_BORDE, insideVertical: SIN_BORDE } }),
    new Paragraph({ spacing: { before: 360, after: 80 }, children: [etiqueta("Fotos de referencia")] }),
    parrafo(CATALOGO.notaFotos),
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
    fotos(f.fotos, f.altoFotos),
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
      new Paragraph({ spacing: { before: 300, after: 100 }, children: [etiqueta(f.medidas.titulo, NAVY, 13), t("  "), confirmar(f.medidas.nota)] }),
      tabla(colM, [new TableRow({ children: f.medidas.valores.map(([k, v], j) => celda([
        new Paragraph({ children: [t(k.toUpperCase(), { size: 12, color: GRIS, characterSpacing: 20 })] }),
        new Paragraph({ children: [t(v, { size: 19, bold: true, color: NAVY })] }),
      ], colM[j], { borders: { top: BORDE_FINO, bottom: BORDE_FINO, left: BORDE_FINO, right: BORDE_FINO } })) })]),
    );
  }
  bloques.push(salto());
  return bloques;
}

function revision() {
  const r = CATALOGO.revision;
  const lista = (items, ref) => items.map(x => new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 100, line: 300 }, children: [t(x, { size: 19 })] }));
  return [
    kicker("Para revisión interna", "No va en la versión final"),
    titulo("Notas para la revisión"),
    parrafo("Lo marcado en amarillo en las fichas está estimado desde las fotos o es un estándar de la industria. Antes de enviar el catálogo hay que validarlo con el taller."),
    new Paragraph({ spacing: { before: 240, after: 120 }, children: [etiqueta("Por confirmar con el taller")] }),
    ...lista(r.taller, "taller"),
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

const numeracion = ["taller", "enviar"].map(reference => ({ reference, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
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
    children: [...portada(), ...linea(), ...CATALOGO.fichas.flatMap(ficha), ...revision()],
  }],
});

const salida = path.join(DIR, "Catalogo_Implementos_Rugby.docx");
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(salida, buf); console.log(`OK  ${salida}`); });
