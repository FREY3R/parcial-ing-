"""Renderiza un archivo de texto (salida de pytest) a PNG para evidencias."""

import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

FUENTE = "C:/Windows/Fonts/consola.ttf"
ANCHO_CAR = 8
ALTO_LINEA = 17


def render(txt_path, png_path, max_lineas=140, ancho_car=118):
    with open(txt_path, encoding="utf-8", errors="replace") as fh:
        crudas = fh.read().splitlines()[:max_lineas]
    lineas = []
    for linea in crudas:
        lineas.extend(textwrap.wrap(linea, width=ancho_car) or [""])
    font = ImageFont.truetype(FUENTE, 12)
    ancho = ancho_car * ANCHO_CAR + 20
    alto = len(lineas) * ALTO_LINEA + 20
    img = Image.new("RGB", (ancho, alto), "white")
    draw = ImageDraw.Draw(img)
    y = 10
    for linea in lineas:
        color = "#111111"
        if linea.startswith("FAILED") or "failed" in linea:
            color = "#b00020"
        elif linea.startswith("==") or linea.startswith("---"):
            color = "#1e40af"
        draw.text((10, y), linea, font=font, fill=color)
        y += ALTO_LINEA
    img.save(png_path)
    print(f"PNG generado: {png_path}")


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
