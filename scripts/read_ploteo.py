import sys, json, datetime, collections
from pyxlsb import open_workbook, convert_date
rows = []
with open_workbook(sys.argv[1]) as wb:
    with wb.get_sheet('Registro') as sh:
        for i, row in enumerate(sh.rows(), start=1):
            if i < 5: continue
            v = [c.v for c in row] + [None] * 20
            f, tipo, m, R, Sy = v[0], v[4], v[14], v[17], v[18]
            if f is None and v[10] is None: continue
            if isinstance(f, (int, float)):
                d = convert_date(f)
            elif isinstance(f, str):
                try: d = datetime.datetime.strptime(f[:10], '%Y-%m-%d')
                except Exception:
                    try: d = datetime.datetime.strptime(f.strip(), '%d-%m-%Y')
                    except Exception: d = None
            else: d = None
            rows.append(dict(row=i, fecha=d.strftime('%Y-%m-%d') if d else repr(f), mes=d.month if d else None, anio=d.year if d else None,
                             ot=v[1], cliente=v[2], prod=v[3], tipo=tipo, motivo=v[5], area=v[6], ancho=v[9], largo=v[10],
                             obs=v[13], metros=m, R=R, S=Sy))
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, default=str)
agg = collections.defaultdict(float); n = collections.Counter(); bad = []
for r in rows:
    if r['mes'] is None or not isinstance(r['metros'], (int, float)):
        bad.append((r['row'], r['fecha'], r['tipo'], r['metros'])); continue
    agg[(r['anio'], r['mes'], str(r['tipo']))] += r['metros']; n[(r['anio'], r['mes'], str(r['tipo']))] += 1
    if (r['R'], r['S']) != (r['mes'], r['anio']):
        print('MES/AÑO inconsistente fila', r['row'], r['fecha'], r['R'], r['S'], r['cliente'], r['metros'])
for k in sorted(agg): print(k, round(agg[k], 2), n[k])
print('sin fecha o metros:', bad[:20], len(bad))
print('ultima fila con datos:', rows[-1]['row'], rows[-1]['fecha'], rows[-1]['cliente'])
