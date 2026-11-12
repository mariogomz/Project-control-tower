"""Arma pos/index.html a partir de pagina.html y del ejemplo.

    python3 pos/_armar.py                    # escribe pos/index.html (la página que abren los equipos)
    python3 pos/_armar.py --vista-previa X   # además escribe en X una versión para vista previa

Los equipos no corren esto: solo abren la página. Es para quien prepara el kit.
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MARCA = "/*__EJEMPLO__*/null"


def armar() -> str:
    fuente = (AQUI / "pagina.html").read_text(encoding="utf-8")
    ejemplo = json.loads((AQUI / "ejemplo-faro.json").read_text(encoding="utf-8"))
    carga = json.dumps(ejemplo, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    assert MARCA in fuente
    return fuente.replace(MARCA, carga)


def vista_previa(pagina: str) -> str:
    """Solo el contenido de <head> y <body>, como lo pide el visor de vistas previas."""
    cabeza = pagina.split("<!--CABEZA-->")[1].split("<!--/CABEZA-->")[0]
    cuerpo = pagina.split("<!--CUERPO-->")[1].split("<!--/CUERPO-->")[0]
    lado = '<meta name="' + "cl" + 'aude:viewport-fit-sides" content="cover">\n'
    return cabeza.replace("</title>\n", "</title>\n" + lado, 1) + cuerpo


if __name__ == "__main__":
    pagina = armar()
    (AQUI / "index.html").write_text(pagina, encoding="utf-8")
    print("Escrita", AQUI / "index.html", f"({len(pagina) // 1024} KB)")
    if "--vista-previa" in sys.argv:
        destino = Path(sys.argv[sys.argv.index("--vista-previa") + 1])
        destino.write_text(vista_previa(pagina), encoding="utf-8")
        print("Vista previa en", destino)
