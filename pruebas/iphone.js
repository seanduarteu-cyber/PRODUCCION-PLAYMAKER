const { chromium, contexto } = require('./comun_movil');
const UAS = {
  safari: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1',
  whatsapp: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 WhatsApp/25.20.80',
  instagram: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 390.0.0.27.81',
  chrome: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/141.0.7390.41 Mobile/15E148 Safari/604.1'
};
(async () => {
  const b = await chromium.launch(); const errores = [];
  for (const [k, ua] of Object.entries(UAS)) {
    const ctx = await contexto(b, { tablas: { plan_usuarios: [{ usuario: 'sean.duarte', nombre: 'Sean Duarte' }] } }, { userAgent: ua, permissions: ['clipboard-read', 'clipboard-write'] });
    const p = await ctx.newPage(); p.on('pageerror', e => errores.push(k + ': ' + e.message));
    await p.goto('https://planificacion-playmaker.netlify.app/sistemas.html'); await p.waitForTimeout(600);
    const vis = await p.isVisible('#btn-instalar');
    await p.click('#btn-instalar'); await p.waitForTimeout(200);
    const txt = (await p.textContent('#pasos-instalar')).replace(/\s+/g, ' ');
    let copiado = '';
    if (await p.$('#pasos-instalar .pmk-copiar')) { await p.click('#pasos-instalar .pmk-copiar'); await p.waitForTimeout(200); copiado = await p.evaluate(() => navigator.clipboard.readText()).catch(e => 'error ' + e.message); }
    console.log('[' + k + '] botón', vis, '|', txt.slice(0, 150), '| copiado:', copiado);
    await p.screenshot({ path: 'movil/iphone_' + k + '.png', fullPage: true });
    // Planificación (pantalla de ingreso): «Instalar en este teléfono»
    await p.goto('https://planificacion-playmaker.netlify.app/'); await p.waitForTimeout(800);
    if (await p.isVisible('#l-instalar')) { await p.click('#l-instalar'); await p.waitForTimeout(300);
      console.log('   planificación:', (await p.textContent('#modal')).replace(/\s+/g, ' ').slice(0, 110)); }
    else console.log('   planificación: sin botón instalar');
    await ctx.close();
  }
  console.log('errores JS:', errores.join(' | ') || 'ninguno');
  await b.close();
})();
