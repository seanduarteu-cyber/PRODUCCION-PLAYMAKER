// Arma catalogo_implementos.html (la fuente del PDF) desde catalogo.json y estilo_catalogo.css.
// Uso: node propuestas/implementos/generar_html.js   (exportar.sh lo corre antes de imprimir el PDF)

const fs = require("fs");
const path = require("path");

const DIR = __dirname;
const C = JSON.parse(fs.readFileSync(path.join(DIR, "catalogo.json"), "utf8"));

const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const dos = n => String(n).padStart(2, "0");
const mayus = s => esc(s.toUpperCase());

function pie(num) {
  return `<div class="pie"><span>UN CLUB, UNA FAMILIA.</span><span class="marcas">` +
    `<img src="../_recursos/playmaker_logo_horizontal_blanco.png" alt="Playmaker"><i></i>` +
    `<img class="proeza" src="../_recursos/proeza_logo_blanco.png" alt="Proeza"></span>` +
    `<span class="num">${dos(num)}</span></div>`;
}

// lo pendiente de una especificación: tercer valor (texto vacío = solo "a confirmar")
function confirmar(pendiente) {
  if (pendiente === undefined) return "";
  return ` <span class="conf">A CONFIRMAR${pendiente ? ": " + mayus(pendiente) : ""}</span>`;
}

const foto = f => `<img src="fotos/${esc(f.archivo)}" style="object-position: ${esc(f.pos)}" alt="">`;

function portada() {
  const p = C.portada;
  return `<section class="page portada">
  <div class="marcas-portada"><img src="../_recursos/playmaker_logo_horizontal_blanco.png" alt="Playmaker"><i></i><img class="proeza" src="../_recursos/proeza_logo_blanco.png" alt="Proeza"></div>
  <div class="kicker">${mayus(p.kicker)}</div>
  <h1>${p.titulo.map(esc).join("<br>")}</h1>
  <p class="sub">${esc(p.subtitulo)}</p>
  <div class="tira">${p.tira.map(foto).join("")}</div>
  <div class="estado">${p.estado ? mayus(p.estado) : ""}<span>${esc(p.fecha)}</span></div>
  ${pie(1)}
</section>`;
}

function linea() {
  const l = C.linea;
  const filas = C.fichas.map((f, i) => `<tr><td class="cod">${esc(f.codigo)}</td><td class="prod">${esc(f.titulo)}</td>` +
    `<td>${esc(f.usoCorto)}</td><td class="fic">Ficha ${dos(i + 1)}</td></tr>`).join("\n    ");
  const criterios = l.criterios.map(([k, v]) => `<div class="fila"><b>${mayus(k)}</b><p>${esc(v)}</p></div>`).join("\n    ");
  return `<section class="page">
  <div class="cab"><b>SECCIÓN 01</b><span>LÍNEA DE EQUIPAMIENTO</span></div>
  <h1>${esc(l.titulo)}</h1>
  <p class="intro">${esc(l.intro)}</p>
  <table>
    <tr><th>CÓDIGO</th><th>PRODUCTO</th><th>USO</th><th style="text-align:right">FICHA</th></tr>
    ${filas}
  </table>
  <div class="criterios">
    <h2>CRITERIOS COMUNES A TODA LA LÍNEA</h2>
    ${criterios}
  </div>
  <div class="nota"><b>FOTOS DE REFERENCIA</b><p>${esc(l.notaFotos)}</p></div>
  ${pie(2)}
</section>`;
}

function ficha(f, i) {
  const n = f.specs.length;
  const bloques = f.specs.map(([k, v, pend], j) =>
    `<div class="bloque${n % 2 && j === n - 1 ? " ancho" : ""}"><h3>${mayus(k)}</h3><p>${esc(v)}${confirmar(pend)}</p></div>`).join("\n    ");
  const medidas = f.medidas ? `
  <div class="medidas">
    <div class="tit"><span>${mayus(f.medidas.titulo)}</span>${confirmar(f.medidas.pendiente)}</div>
    <div class="fila" style="grid-template-columns: repeat(${f.medidas.valores.length}, 1fr)">
      ${f.medidas.valores.map(([k, v]) => `<div><small>${esc(k)}</small><strong>${esc(v)}</strong></div>`).join("\n      ")}
    </div>
  </div>` : "";
  return `<section class="page">
  <div class="cab"><b>FICHA ${dos(i + 1)}<span class="sep"></span>${mayus(f.categoria)}</b><span>${esc(f.codigo)}</span></div>
  <h1>${esc(f.titulo)}</h1>
  <p class="bajada">${esc(f.bajada)}</p>
  <div class="fotos ${f.fotos.diseno}">
    ${f.fotos.archivos.map(foto).join("\n    ")}
  </div>
  <p class="leyenda">${esc(f.leyenda)}</p>
  <div class="uso"><b>USO</b><p>${esc(f.uso)}</p></div>
  <div class="bloques">
    ${bloques}
  </div>${medidas}
  ${pie(i + 3)}
</section>`;
}

function revision(num) {
  const r = C.revision;
  const lista = items => items.map(x => `<li>${esc(x)}</li>`).join("\n    ");
  return `<section class="page revision">
  <div class="cab"><b>PARA REVISIÓN INTERNA</b><span>NO VA EN LA VERSIÓN FINAL</span></div>
  <h1>Notas para la revisión</h1>
  <p class="intro">${esc(r.intro)}</p>
  <h2>PENDIENTE</h2>
  <ol>
    ${lista(r.pendientes)}
  </ol>
  <h2>ANTES DE ENVIARLO A UN CLUB</h2>
  <ol>
    ${lista(r.antesDeEnviar)}
  </ol>
  <div class="aviso">${esc(r.aviso)}</div>
  ${pie(num)}
</section>`;
}

const css = fs.readFileSync(path.join(DIR, "estilo_catalogo.css"), "utf8");
const html = `<!doctype html>
<!-- Generado por generar_html.js desde catalogo.json: no editar a mano. -->
<html lang="es">
<head>
<meta charset="utf-8">
<title>Catálogo de implementos de rugby de Playmaker y Proeza</title>
<style>
${css}</style>
</head>
<body>

${portada()}

${linea()}

${C.fichas.map(ficha).join("\n\n")}

${C.revision.incluir === false ? "" : revision(C.fichas.length + 3)}

</body>
</html>
`;
fs.writeFileSync(path.join(DIR, "catalogo_implementos.html"), html);
console.log(`OK  ${path.join(DIR, "catalogo_implementos.html")}`);
