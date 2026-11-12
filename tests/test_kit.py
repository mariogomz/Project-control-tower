"""El kit que reciben los estudiantes solo nombra la herramienta que ellos usan (Codex)."""
import subprocess
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SOLO_PREPARACION = ("CLAUDE.md", ".claude", ".gitattributes", "tests/test_kit.py", "torre/vendor/")
PALABRA = "cl" + "aude"


class Kit(unittest.TestCase):
    def test_material_para_estudiantes_sin_menciones(self):
        archivos = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout.split()
        con_mencion = []
        for rel in archivos:
            if rel.startswith(SOLO_PREPARACION):
                continue
            ruta = RAIZ / rel
            if ruta.is_file() and PALABRA in ruta.read_text(encoding="utf-8", errors="ignore").lower():
                con_mencion.append(rel)
        self.assertEqual(con_mencion, [])


if __name__ == "__main__":
    unittest.main()
