"""La página del POS, el ejemplo y el kit hablan el mismo formato de bloque."""
import json
import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "pos"))
import _armar  # noqa: E402


def forma(x):
    """Las claves de un bloque, sin sus valores: sirve para comparar dos bloques."""
    if isinstance(x, dict):
        return {k: forma(v) for k, v in sorted(x.items())}
    if isinstance(x, list):
        return [forma(x[0])] if x and isinstance(x[0], (dict, list)) else []
    return ""


class Pos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ejemplo = json.loads((RAIZ / "pos" / "ejemplo-faro.json").read_text(encoding="utf-8"))
        kit = (RAIZ / "kit" / "kit-s5.md").read_text(encoding="utf-8")
        cls.plantilla = json.loads(re.search(r"```json\n(.*?)\n```", kit, re.S).group(1))
        cls.pagina = (RAIZ / "pos" / "pagina.html").read_text(encoding="utf-8")

    def test_plantilla_del_kit_y_ejemplo_tienen_la_misma_forma(self):
        self.assertEqual(forma(self.plantilla), forma(self.ejemplo))

    def test_la_pagina_lee_todas_las_claves_del_bloque(self):
        for clave in self.plantilla:
            if clave in ("pos", "version_brief"):
                continue
            self.assertRegex(self.pagina, rf"\bd\.{clave}\b|\"{clave}\"", f"la página no usa «{clave}»")

    def test_index_esta_al_dia(self):
        self.assertEqual((RAIZ / "pos" / "index.html").read_text(encoding="utf-8"), _armar.armar(),
                         "corre: python3 pos/_armar.py")

    def test_el_ejemplo_tiene_las_seis_casillas_y_una_recomendada(self):
        op = self.ejemplo["opciones"]
        self.assertEqual(len(op), 6)
        self.assertEqual(sum(1 for o in op if o["es_la_solicitud"]), 1)
        self.assertTrue(any(o["recomendada"] for o in op))
        self.assertEqual({e["etiqueta"] for e in self.ejemplo["evidencia"]}, {"dato", "supuesto", "esperanza"})


if __name__ == "__main__":
    unittest.main()
