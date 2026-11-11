"""Genera el diagrama de clases UML de v2.0.0 como PNG (matplotlib)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def caja(ax, x, y, w, h, titulo, lineas=(), color="#dbeafe", borde="#1e40af"):
    ax.add_patch(
        FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=color, edgecolor=borde, lw=1.4,
        )
    )
    ax.text(x, y + h / 2 - 0.22, titulo, ha="center", va="center",
            fontsize=9, fontweight="bold")
    for i, linea in enumerate(lineas):
        ax.text(x - w / 2 + 0.15, y + h / 2 - 0.55 - i * 0.26, linea,
                ha="left", va="center", fontsize=7, family="monospace")


def flecha(ax, a, b, estilo="-|>", linea="--", color="#333333"):
    ax.add_patch(
        FancyArrowPatch(
            a, b, arrowstyle=estilo, mutation_scale=12, lw=1.1,
            linestyle=linea, color=color, shrinkA=4, shrinkB=4,
        )
    )


fig, ax = plt.subplots(figsize=(13, 10))
ax.set_xlim(0, 13)
ax.set_ylim(-5, 10)
ax.axis("off")

caja(
    ax, 2.6, 5.0, 4.6, 5.2, "«module» envios",
    (
        "+ validar_peso(peso: Decimal)",
        "+ validar_zona(zona: str)",
        "+ validar_dia(dia: int)",
        "+ validar_cupon(cupon: str|None)",
        "+ costo_base(peso: Decimal)",
        "+ aplicar_descuentos(...)",
        "+ redondear_half_up(valor)",
        "+ calc(peso, zona, cliente, dia, cupon)",
    ),
)
caja(ax, 2.6, -1.6, 3.2, 1.1, "ErrorEnvio", ("+ mensaje: str",),
     color="#fee2e2", borde="#991b1b")
ax.text(2.6, -2.55, "«hereda de» ValueError", ha="center", fontsize=7, style="italic")

caja(ax, 9.7, 8.2, 4.2, 1.5, "«Protocol» EstrategiaZona",
     ("+ recargo(costo: Decimal) Decimal",), color="#fef3c7", borde="#92400e")
caja(ax, 9.7, 6.0, 4.2, 1.0, "ZonaUrbana", ("+ recargo(costo)",))
caja(ax, 9.7, 4.7, 4.2, 1.0, "ZonaRural", ("+ recargo(costo)",))
caja(ax, 9.7, 3.4, 4.2, 1.0, "ZonaNacional", ("+ recargo(costo)",))

caja(ax, 9.7, 1.0, 4.2, 1.5, "«Protocol» EstrategiaDescuento",
     ("+ aplicar(costo: Decimal) Decimal",), color="#fef3c7", borde="#92400e")
caja(ax, 9.7, -1.2, 4.2, 1.0, "SinDescuento", ("+ aplicar(costo)",))
caja(ax, 9.7, -2.5, 4.2, 1.0, "DescuentoFrecuente", ("+ aplicar(costo)",))
caja(ax, 9.7, -3.8, 4.2, 1.0, "DescuentoVip", ("+ aplicar(costo)",))

flecha(ax, (4.9, 6.2), (7.6, 8.0))
ax.text(6.1, 7.4, "usa", fontsize=7, color="#555555")
flecha(ax, (4.9, 3.8), (7.6, 1.2))
ax.text(6.1, 2.6, "usa", fontsize=7, color="#555555")

for y in (6.0, 4.7, 3.4):
    flecha(ax, (9.7, 7.45), (9.7, y + 0.5))
for y in (-1.2, -2.5, -3.8):
    flecha(ax, (9.7, 0.25), (9.7, y + 0.5))

flecha(ax, (2.6, 2.4), (2.6, -1.05), color="#991b1b")
ax.text(3.4, 0.6, "lanza", fontsize=7, color="#991b1b")

ax.set_title("UML de clases — envios v2.0.0", fontsize=12)
plt.tight_layout()
plt.savefig("evidence/uml_clases.png", dpi=150, bbox_inches="tight")
print("PNG generado: evidence/uml_clases.png")
