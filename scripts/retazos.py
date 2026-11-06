"""Merma de la marcada (retazos) visible en la receta.

Los metros de la marcada ya incluyen los retazos: 68,5 m para 100 prendas con 71% de aprovechamiento
significa que el 29% de esos metros se pagan pero quedan como retazo. Estas columnas muestran cuánto
del costo de tela son retazos (no lo suman de nuevo).

Uso: python3 -I scripts/retazos.py receta.xlsx   (agrega las columnas a una receta ya construida)
También lo llama construir_receta.py.
"""
import sys
from openpyxl.styles import Font, PatternFill, Alignment

F0, ND, NM, H0, NP = 5, 1000, 150, 7, 16
AZUL = PatternFill('solid', fgColor='DDEBF7'); GRIS = PatternFill('solid', fgColor='F2F2F2'); HF = PatternFill('solid', fgColor='1F3864')
H = Font(bold=True, color='FFFFFF'); WC = Alignment(wrap_text=True, vertical='center', horizontal='center')
MONEY = '"$"#,##0;-"$"#,##0;"$"0'


def agregar(wb):
    D, M, F = wb['Despiece'], wb['Moldes'], wb['Ficha']
    DA, DG, DJ, DK, DCL = (f'Despiece!${c}${F0}:${c}${F0+ND-1}' for c in 'AGJKH')
    # Despiece J = aprovechamiento de la marcada, K = $ de retazos incluido en G
    for col, t, w in ((10, 'APROVECHAMIENTO\nde la marcada (%)', 15), (11, '$ de retazos\n(ya incluido en\n$ tela)', 13)):
        c = D.cell(4, col, t); c.font = H; c.fill = HF; c.alignment = WC
        D.column_dimensions[chr(64 + col)].width = w
    for r in range(F0, F0 + ND):
        D.cell(r, 10).fill = AZUL; D.cell(r, 10).number_format = '0%'
        c = D.cell(r, 11, f'=IF(AND(ISNUMBER(G{r}),N(J{r})>0),G{r}*(1-J{r}),"")'); c.fill = GRIS; c.number_format = MONEY
    D.auto_filter.ref = f'A4:K{F0+ND-1}'
    # Moldes X = $ de retazos incluido en la tela del molde
    c = M.cell(4, 24, '$ de retazos\n(ya incluido en\n$ Tela)'); c.font = H; c.fill = HF; c.alignment = WC
    M.column_dimensions['X'].width = 13
    for r in range(F0, F0 + NM):
        em, ft = f'IF(S{r}="",A{r},S{r})', f'IF(N(T{r})>0,T{r},1)'
        c = M.cell(r, 24, f'=IF(OR(A{r}="",NOT(ISNUMBER(L{r}))),"",IF(COUNTIFS({DA},{em},{DK},">0")=0,"",SUMIFS({DK},{DA},{em})*{ft}))')
        c.fill = GRIS; c.number_format = MONEY
    M.auto_filter.ref = f'A4:X{F0+NM-1}'
    # Ficha: columna L oculta por pieza con su $ de retazos, y nota en la fila "Tela" del resumen
    F.column_dimensions['L'].width = 11
    for i in range(NP):
        r = H0 + 1 + i; idx = f'MATCH($L$4&"|"&{i+1},{DCL},0)'
        c = F.cell(r, 12, f'=IF(ISNUMBER(H{r}),IFERROR(H{r}*(1-IF(N(INDEX({DJ},{idx}))>0,INDEX({DJ},{idx}),1)),0),"")')
        c.number_format = MONEY; c.font = Font(color='BBBBBB', size=8)
    F.cell(H0, 12, 'retazos').font = Font(color='BBBBBB', size=8)
    for r in range(H0 + NP + 1, H0 + NP + 6):
        if F.cell(r, 2).value == 'Tela':
            F.cell(r, 11, f'=IF(SUM(L{H0+1}:L{H0+NP})>0,"Incluye "&TEXT(SUM(L{H0+1}:L{H0+NP}),"$#,##0")&" de retazos (lo que la marcada no aprovecha)","Suma de las piezas")')
            F.cell(r, 11).font = Font(color='595959', size=9)


if __name__ == '__main__':
    from openpyxl import load_workbook
    wb = load_workbook(sys.argv[1]); agregar(wb); wb.save(sys.argv[1]); print('ok')
