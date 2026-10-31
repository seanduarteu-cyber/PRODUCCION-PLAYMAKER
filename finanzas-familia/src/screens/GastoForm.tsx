import { useEffect, useState } from 'react';
import { Campo, CategoriaSelect, Icon, MontoInput, Sheet } from '../components/ui';
import { useApp, useFamilia } from '../data/store';
import { fmtCLP, hoy, mesActual, mesDe, nombreMes, primerDia, sumarMeses } from '../lib/format';
import { comprimirFoto } from '../lib/imagen';
import type { Gasto } from '../lib/types';

const LS_ULTIMA = 'ff_ultima_categoria';

export function GastoForm({ gasto, onClose }: { gasto?: Gasto; onClose: () => void }) {
  const f = useFamilia();
  const { error, avisar } = useApp();
  const enlazado = !!(gasto?.boletaId || gasto?.deudaId);
  const defFecha = f.mes === mesActual() ? hoy() : primerDia(f.mes);
  const ultima = (() => {
    try {
      return localStorage.getItem(`${LS_ULTIMA}_${f.family.id}`) || '';
    } catch {
      return '';
    }
  })();

  const [monto, setMonto] = useState<number | null>(gasto?.monto ?? null);
  const [fecha, setFecha] = useState(gasto?.fecha ?? defFecha);
  const [categoriaId, setCategoriaId] = useState(gasto?.categoriaId ?? ultima);
  const [descripcion, setDescripcion] = useState(gasto?.descripcion ?? '');
  const [medioPago, setMedioPago] = useState(gasto?.medioPago ?? '');
  const [enCuotas, setEnCuotas] = useState(false);
  const [numCuotas, setNumCuotas] = useState(3);
  const [valorCuota, setValorCuota] = useState<number | null>(null);
  const [cuotaManual, setCuotaManual] = useState(false);
  const [primerMes, setPrimerMes] = useState(sumarMeses(mesDe(defFecha), 1));
  const [foto, setFoto] = useState<string | null>(null);
  const [fotoCambiada, setFotoCambiada] = useState(false);
  const [guardando, setGuardando] = useState(false);
  const [err, setErr] = useState('');

  useEffect(() => {
    if (gasto?.adjuntoId) f.acciones.leerAdjunto(gasto.adjuntoId).then(setFoto).catch(() => undefined);
  }, [gasto?.adjuntoId, f.acciones]);

  useEffect(() => {
    if (!cuotaManual && monto && numCuotas > 0) setValorCuota(Math.round(monto / numCuotas));
  }, [monto, numCuotas, cuotaManual]);

  async function elegirFoto(file?: File) {
    if (!file) return;
    try {
      setFoto(await comprimirFoto(file));
      setFotoCambiada(true);
    } catch (e) {
      error(e);
    }
  }

  async function guardar() {
    setErr('');
    if (!monto || monto <= 0) return setErr('Ingresa el monto.');
    if (!f.settings.categorias.some((c) => c.id === categoriaId)) return setErr('Elige una categoría.');
    setGuardando(true);
    try {
      try {
        localStorage.setItem(`${LS_ULTIMA}_${f.family.id}`, categoriaId);
      } catch {
        /* nada */
      }
      if (enCuotas && !gasto) {
        if (numCuotas < 2 || !valorCuota) throw new Error('Indica el número de cuotas y su valor.');
        await f.acciones.compraEnCuotas({
          descripcion: descripcion.trim() || f.settings.categorias.find((c) => c.id === categoriaId)!.nombre,
          categoriaId, total: monto, numCuotas, valorCuota, primerMes, medioPago: medioPago || undefined,
        });
        avisar(`Compra en ${numCuotas} cuotas registrada (desde ${nombreMes(primerMes).toLowerCase()})`);
        onClose();
        return;
      }
      let adjuntoId = gasto?.adjuntoId;
      if (fotoCambiada) {
        if (adjuntoId) f.acciones.eliminarAdjunto(adjuntoId);
        adjuntoId = foto ? await f.acciones.guardarAdjunto(foto) : undefined;
      }
      const datos = { monto, fecha, categoriaId, descripcion: descripcion.trim(), medioPago: medioPago || undefined, adjuntoId };
      const g: Gasto = gasto ? { ...gasto, ...datos } : f.acciones.nuevoGasto(datos);
      await f.acciones.guardarGasto(g);
      if (mesDe(fecha) !== f.mes) avisar(`Guardado en ${nombreMes(mesDe(fecha)).toLowerCase()}`);
      else avisar(gasto ? 'Gasto actualizado' : 'Gasto guardado');
      onClose();
    } catch (e) {
      error(e);
    } finally {
      setGuardando(false);
    }
  }

  function eliminar() {
    if (!gasto) return;
    const extra = gasto.boletaId ? ' La boleta volverá a quedar pendiente por este monto.' : gasto.deudaId ? ' La cuota volverá a quedar pendiente.' : '';
    if (!confirm('¿Eliminar este gasto?' + extra)) return;
    f.acciones.eliminarGasto(gasto);
    avisar('Gasto eliminado', 'info');
    onClose();
  }

  return (
    <Sheet titulo={gasto ? 'Editar gasto' : 'Nuevo gasto'} onClose={onClose} pie={
      <>
        {gasto && <button className="btn danger" onClick={eliminar}>Eliminar</button>}
        <button className="btn primary" disabled={guardando} onClick={guardar}>{guardando ? 'Guardando…' : 'Guardar'}</button>
      </>
    }>
      <MontoInput value={monto} onChange={setMonto} grande autoFocus={!gasto} />
      {enlazado && (
        <div className="alert">
          {gasto?.boletaId ? 'Este gasto es el pago de una boleta. Si cambias el monto, se actualiza la boleta.' : 'Este gasto es el pago de una cuota.'}
        </div>
      )}
      <Campo label="Categoría">
        <CategoriaSelect settings={f.settings} value={categoriaId} onChange={setCategoriaId} />
      </Campo>
      <Campo label="Descripción">
        <input className="input" value={descripcion} onChange={(e) => setDescripcion(e.target.value)} placeholder="Ej: almacén, pan y leche" maxLength={120} />
      </Campo>
      <div className="grid2">
        <Campo label="Fecha">
          <input className="input" type="date" value={fecha} onChange={(e) => e.target.value && setFecha(e.target.value)} />
        </Campo>
        <Campo label="Medio de pago">
          <select className="input" value={medioPago} onChange={(e) => setMedioPago(e.target.value)}>
            <option value="">—</option>
            {f.settings.mediosPago.map((m) => <option key={m}>{m}</option>)}
          </select>
        </Campo>
      </div>

      {!gasto && (
        <div className="card stack">
          <label className="check" style={{ minHeight: 0 }}>
            <input type="checkbox" checked={enCuotas} onChange={(e) => setEnCuotas(e.target.checked)} />
            <span><b>Pagar en cuotas</b><br /><span className="muted small">Compra con tarjeta o crédito: se proyecta cada cuota en los meses siguientes.</span></span>
          </label>
          {enCuotas && (
            <>
              <div className="grid2">
                <Campo label="N° de cuotas">
                  <input className="input num" type="number" inputMode="numeric" min={2} max={120} value={numCuotas} onChange={(e) => setNumCuotas(Math.max(0, parseInt(e.target.value || '0', 10)))} />
                </Campo>
                <Campo label="Valor cuota">
                  <MontoInput value={valorCuota} onChange={(n) => { setCuotaManual(true); setValorCuota(n); }} />
                </Campo>
              </div>
              <Campo label="Primera cuota" ayuda={valorCuota && numCuotas ? `Total a pagar: ${fmtCLP(valorCuota * numCuotas)}${monto && valorCuota * numCuotas > monto ? ` (intereses ${fmtCLP(valorCuota * numCuotas - monto)})` : ''}` : undefined}>
                <input className="input" type="month" value={primerMes} onChange={(e) => e.target.value && setPrimerMes(e.target.value)} />
              </Campo>
            </>
          )}
        </div>
      )}

      {!enCuotas && (
        <div className="stack tight">
          {foto ? (
            <>
              <img className="thumb" src={foto} alt="Foto de la boleta" />
              <button className="btn sm danger" onClick={() => { setFoto(null); setFotoCambiada(true); }}>{Icon.trash} Quitar foto</button>
            </>
          ) : (
            <label className="foto-btn">
              {Icon.camera} Foto de la boleta (opcional)
              <input type="file" accept="image/*" capture="environment" onChange={(e) => elegirFoto(e.target.files?.[0])} />
            </label>
          )}
        </div>
      )}
      {err && <p className="error-text">{err}</p>}
      {gasto && <p className="muted tiny">Registrado por {gasto.creadoPorNombre}</p>}
    </Sheet>
  );
}
