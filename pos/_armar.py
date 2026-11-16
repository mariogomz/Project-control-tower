"""Arma pos/index.html a partir de pagina.html y del ejemplo.

    python3 pos/_armar.py                    # escribe pos/index.html (la página que abren los equipos)
    python3 pos/_armar.py --vista-previa X   # además escribe en X una versión para vista previa

pos/index.html es un solo archivo que no depende de ningún otro: lleva dentro la biblioteca de la
vista 3D, así que se puede publicar en cualquier sitio o abrir con doble clic.

Los equipos no corren esto: solo abren la página. Es para quien prepara el kit.
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MARCA = "/*__EJEMPLO__*/null"
MARCA_SIM = "/*__SIMULACION__*/null"
THREE_CDN = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.min.js"></script>'


def _three_dentro() -> str:
    fuente = (AQUI.parent / "torre" / "vendor" / "three.min.js").read_text(encoding="utf-8")
    if fuente.startswith("console.warn("):  # aviso de obsolescencia del paquete; no aporta aquí
        fuente = "!" + fuente[fuente.index("/**"):]
    return "<script>" + fuente.replace("</script", "<\\/script") + "</script>"


def armar(autonomo: bool = True) -> str:
    fuente = (AQUI / "pagina.html").read_text(encoding="utf-8")
    ejemplo = json.loads((AQUI / "ejemplo-faro.json").read_text(encoding="utf-8"))
    simulacion = json.loads((AQUI / "simulacion-faro.json").read_text(encoding="utf-8"))
    compacto = lambda x: json.dumps(x, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    assert MARCA in fuente and MARCA_SIM in fuente and THREE_CDN in fuente
    pagina = fuente.replace(MARCA, compacto(ejemplo)).replace(MARCA_SIM, compacto(simulacion))
    return pagina.replace(THREE_CDN, _three_dentro()) if autonomo else pagina


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
        destino.write_text(vista_previa(armar(autonomo=False)), encoding="utf-8")
        print("Vista previa en", destino)
