"""Datos mensuales PMK (fuente: Control de Ploteo + chat PENDIENTES PMK, vía PMK_Maestro_2026.xlsx).
Para un mes nuevo: agregar una entrada en MESES (y sus causas en CAUSAS_MES) y cambiar MES_ACTUAL.
Los informes usan: corto plazo = últimos 3 meses; largo plazo = ventana de 12 meses."""

MES_ACTUAL = '2026-10'
INICIO_REGISTRO = '2026-05'

NOMBRES = {1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL', 5: 'MAYO', 6: 'JUNIO', 7: 'JULIO', 8: 'AGOSTO',
           9: 'SEPTIEMBRE', 10: 'OCTUBRE', 11: 'NOVIEMBRE', 12: 'DICIEMBRE'}
CORTOS = {1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AGO', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DIC'}

# prod/rep/antes en metros (Control de Ploteo); ev = pedidos en el chat; pr = prendas; est = mes estimado
MESES = {
    '2026-05': dict(prod=1889.90, rep=133.00, antes=11.95, ev=25, pr=50),
    '2026-06': dict(prod=1863.85, rep=148.95, antes=9.05, ev=55, pr=157),
    '2026-07': dict(prod=1901.00, rep=245.00, antes=13.23, ev=48, pr=286, est=True),
    '2026-08': dict(prod=1722.03, rep=278.87, antes=10.24, ev=57, pr=198),
    '2026-09': dict(prod=2097.76, rep=127.13, antes=5.91, ev=51, pr=354),
    '2026-10': dict(prod=2195.03, rep=94.72, antes=10.13, ev=28, pr=171),
}

CATEGORIAS = ['Mesa/Papel', 'Sublimación', 'Pendiente', 'Faltó imp.', 'Corte', 'Confección', 'Diseño/Ficha']
# pedidos del chat por causa (orden de CATEGORIAS)
CAUSAS_MES = {
    '2026-08': [15, 12, 12, 5, 4, 4, 5],
    '2026-09': [10, 12, 7, 2, 7, 6, 7],
    '2026-10': [3, 7, 9, 2, 6, 1, 0],
}
# meses sin desglose mensual completo, sólo agregado (mayo–julio)
CAUSAS_AGREGADAS = {('2026-05', '2026-07'): [55, 36, 11, 6, 9, 7, 4]}

# hoja de ruta: meta % y metros por mes
METAS = {'2026-09': (11, 235), '2026-10': (8, 165), '2026-11': (6, 121), '2026-12': (5, 100)}
META_FINAL = 5

# uso de la línea ETAPA en el chat (registros con ETAPA / total)
ETAPA_CHAT = {'2026-10': (24, 28)}

COSTO_M_COMPLETO, COSTO_M_ANTES = 6000, 2400   # $6.000/m = tela 40% + mesa/ploteo 40% + sublimación 20%


# ------------------------------------------------------------------ cálculos
def ym(key):
    y, m = key.split('-'); return int(y), int(m)


def shift(key, n):
    y, m = ym(key); t = y * 12 + (m - 1) + n
    return f'{t // 12:04d}-{t % 12 + 1:02d}'


def nombre(key):
    return NOMBRES[ym(key)[1]]


def corto(key, con_anio=False):
    y, m = ym(key)
    c = CORTOS[m] + ('*' if MESES.get(key, {}).get('est') else '')
    return f'{c} {str(y)[2:]}' if con_anio else c


def pct(key):
    d = MESES[key]; return 100 * d['rep'] / (d['prod'] + d['rep'])


def costo(key):
    d = MESES[key]; return d['antes'] * COSTO_M_ANTES + (d['rep'] - d['antes']) * COSTO_M_COMPLETO


def ventana(n, hasta=None):
    hasta = hasta or MES_ACTUAL
    return [shift(hasta, -i) for i in range(n - 1, -1, -1)]


def total(keys):
    ks = [k for k in keys if k in MESES]
    t = {f: sum(MESES[k][f] for k in ks) for f in ('prod', 'rep', 'antes', 'ev', 'pr')}
    t['pct'] = 100 * t['rep'] / (t['prod'] + t['rep']) if ks else None
    t['costo'] = sum(costo(k) for k in ks)
    t['meses'] = len(ks)
    return t


def causas_total(keys):
    tot = [0] * len(CATEGORIAS)
    for k in keys:
        if k in CAUSAS_MES:
            tot = [a + b for a, b in zip(tot, CAUSAS_MES[k])]
    for (a, b), v in CAUSAS_AGREGADAS.items():
        if all(k in keys for k in ventana(ym(b)[1] - ym(a)[1] + 1, b)):
            tot = [x + y for x, y in zip(tot, v)]
    return tot


def semaforo(p):
    return 'verde' if p < 7 else ('naranja' if p <= 10 else 'rojo')


def fmt_num(v, dec=0):
    s = f'{v:,.{dec}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fmt_pct(v):
    return fmt_num(v, 1) + '%'


def fmt_clp(v):
    return '$' + fmt_num(round(v))


if __name__ == '__main__':
    for k in ventana(12):
        print(k, corto(k, True), round(pct(k), 2) if k in MESES else '—', round(costo(k)) if k in MESES else '')
    print('3m', total(ventana(3)))
    print('12m', total(ventana(12)))
    print('causas 12m', causas_total(ventana(12)), sum(causas_total(ventana(12))))
