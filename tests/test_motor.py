"""Pruebas del motor con el caso Faro y con la plantilla vacía.  python3 -m unittest discover -s tests"""
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "torre"))
import construir  # noqa: E402
import motor  # noqa: E402


class Faro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pos = motor.cargar(RAIZ / "ejemplos" / "faro")
        cls.e = motor.linea_de_tiempo(cls.pos)

    def claves(self, w):
        return {a["clave"]: a for a in self.e[w]["alertas"]}

    def test_registros_bien_formados(self):
        self.assertEqual(motor.revisar(self.pos), [])

    def test_doce_semanas_y_arranque_sin_datos(self):
        self.assertEqual(len(self.e), 13)
        self.assertEqual(self.e[0]["salud"], "sin_datos")
        self.assertEqual(self.e[0]["alertas"], [])

    def test_arco_de_salud(self):
        salud = [x["salud"] for x in self.e]
        self.assertEqual(salud[1], "verde")
        self.assertEqual(salud[2], "ambar")
        self.assertTrue(all(s == "rojo" for s in salud[3:11]))
        self.assertEqual(salud[11:], ["ambar", "ambar"])

    def test_senales_sin_decision_aparecen_antes_que_la_crisis(self):
        self.assertEqual(self.claves(2)["senal-S3"]["severidad"], "atencion")
        self.assertEqual(self.claves(3)["senal-S3"]["severidad"], "critica")
        self.assertEqual(self.claves(6)["senal-S3"]["desde"], 2)

    def test_la_decision_apaga_las_alertas_que_atiende(self):
        self.assertIn("sup-S3", self.claves(6))
        self.assertIn("corte-0", self.claves(6))
        for clave in ("sup-S3", "senal-S3", "corte-0"):
            self.assertNotIn(clave, self.claves(7))
        s3 = next(s for s in self.e[7]["supuestos"] if s["id"] == "S3")
        self.assertEqual((s3["estado"], s3["decidido"]), ("roto", 7))

    def test_indicador_sin_medir(self):
        self.assertNotIn("ind-apagado-I4", self.claves(6))
        self.assertIn("ind-apagado-I4", self.claves(7))
        self.assertNotIn("ind-apagado-I4", self.claves(8))

    def test_valor_ganado(self):
        ev = self.e[6]["evm"]
        self.assertAlmostEqual(ev["pct_real"], 0.635)
        self.assertAlmostEqual(ev["spi"], 254000 / 275000)
        self.assertAlmostEqual(ev["cpi"], 254000 / 318000)

    def test_rastro_de_la_senal_a_la_decision(self):
        r = {x["ref"]: x for x in self.e[12]["rastros"]}
        self.assertEqual((r["S3"]["senales"][0], r["S3"]["decision"], r["S3"]["espera"]), (1, 7, 6))
        self.assertEqual(r["S4"]["espera"], 3)

    def test_corte_por_semana(self):
        self.assertEqual(len(motor.linea_de_tiempo(self.pos, 6)), 7)

    def test_brief_nombra_a_quien_decide(self):
        self.assertIn("Director de Experiencia del Cliente", self.e[6]["brief"])
        self.assertIn("ROJO", self.e[6]["brief"])

    def test_construye_un_solo_archivo(self):
        with tempfile.TemporaryDirectory() as d:
            salida = Path(d) / "torre.html"
            self.assertEqual(construir.main([str(RAIZ / "ejemplos" / "faro"), "--salida", str(salida)]), 0)
            texto = salida.read_text(encoding="utf-8")
            self.assertTrue(texto.startswith("<!doctype html>"))
            self.assertIn("Estatus sin llamar", texto)
            self.assertNotIn("/*__DATOS__*/null", texto)


class Plantilla(unittest.TestCase):
    def test_plantilla_vacia_no_rompe(self):
        pos = motor.cargar(RAIZ / "plantilla")
        self.assertTrue(motor.revisar(pos))  # avisa de lo que falta
        e = motor.linea_de_tiempo(pos)
        self.assertEqual((len(e), e[0]["salud"]), (1, "sin_datos"))
        d = construir.datos(pos)
        self.assertEqual(d["etapa_maxima"], 1)
        self.assertIn("<title>", construir.html(d, three="cdn"))


if __name__ == "__main__":
    unittest.main()
