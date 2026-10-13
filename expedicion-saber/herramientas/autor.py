"""Ayudante compacto para escribir bancos a mano: numera los ids y arma cada tipo de desafío.

    b = Autor("cie", 3, 1)            # prefijo, curso, número de OA → ids cie3-oa1-001, …
    b.om(1, "¿…?", "correcta", ["d1", "d2", "d3"], "pista", "explicación")
    b.om(2, "Escucha y elige.", "🐶", ["🐱", "🐦", "🐟"], "…", "…", audio="dog")   # audio en inglés
    b.om(3, "¿…?", "…", [...], "…", "…", texto="Cuento o lectura que acompaña")
"""
import comun


class Autor:
    def __init__(self, prefijo, curso, oa):
        self.prefijo, self.curso, self.oa, self.k, self.items = prefijo, curso, oa, 0, []

    def _id(self):
        self.k += 1
        return f"{self.prefijo}{self.curso}-oa{self.oa}-{self.k:03d}"

    def _add(self, item, texto=None, audio=None, idioma="en"):
        extra = {}
        if texto:
            extra["texto"] = texto
        if audio:
            extra["audio"] = {"texto": audio, "idioma": idioma}
        if extra:
            orden = ["id", "tipo", "dificultad"] + (["texto"] if texto else []) + ["enunciado"] + (["audio"] if audio else [])
            item = {**item, **extra}
            item = {k: item[k] for k in orden} | {k: v for k, v in item.items() if k not in orden}
        self.items.append(item)
        return item

    def om(self, n, enun, ok, ds, pista, expl, texto=None, audio=None):
        return self._add(comun.opcion_multiple(self._id(), n, enun, ok, ds, pista, expl), texto, audio)

    def co(self, n, enun, ok, ds, pista, expl, texto=None, audio=None):
        return self._add(comun.completar(self._id(), n, enun, ok, ds, pista, expl), texto, audio)

    def ord(self, n, enun, elementos, pista, expl, texto=None, audio=None):
        return self._add(comun.ordenar(self._id(), n, enun, elementos, pista, expl), texto, audio)

    def em(self, n, enun, pares, pista, expl, texto=None, audio=None):
        return self._add(comun.emparejar(self._id(), n, enun, pares, pista, expl), texto, audio)

    def cat(self, n, enun, categorias, elementos, pista, expl, texto=None, audio=None):
        return self._add(comun.categoria(self._id(), n, enun, categorias, elementos, pista, expl), texto, audio)

    def nu(self, n, enun, resp, pista, expl, tol=0, unidad="", texto=None, audio=None):
        return self._add(comun.numerica(self._id(), n, enun, resp, pista, expl, tolerancia=tol, unidad=unidad), texto, audio)
