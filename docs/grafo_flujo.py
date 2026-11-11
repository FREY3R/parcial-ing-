"""Genera el grafo de flujo de calc (v1.0.0) como PNG con matplotlib.

P1 se descompone en P1a (p<=0) y P1b (p>50) para contar el cortocircuito del
`or` como predicado independiente. Así N=30, E=43 y M=E-N+2=15, que coincide
con el conteo de nodos predicado (14+1) y con radon.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon


def caja(ax, x, y, texto, ancho=2.2, alto=0.9, rombo=False):
    if rombo:
        pts = [(x, y - alto / 2), (x + ancho / 2, y), (x, y + alto / 2), (x - ancho / 2, y)]
        ax.add_patch(Polygon(pts, closed=True, facecolor="#fff3cd", edgecolor="#8a6d3b", lw=1.2))
    else:
        ax.add_patch(
            FancyBboxPatch(
                (x - ancho / 2, y - alto / 2), ancho, alto,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                facecolor="#dbeafe", edgecolor="#1e40af", lw=1.2,
            )
        )
    ax.text(x, y, texto, ha="center", va="center", fontsize=7)


def flecha(ax, a, b, etiqueta=None):
    ax.add_patch(
        FancyArrowPatch(
            a, b, arrowstyle="-|>", mutation_scale=8, lw=1,
            color="#333333", connectionstyle="arc3,rad=0.12",
            shrinkA=6, shrinkB=6,
        )
    )
    if etiqueta:
        ax.text((a[0] + b[0]) / 2 + 0.15, (a[1] + b[1]) / 2, etiqueta,
                fontsize=6, color="#555555")


fig, ax = plt.subplots(figsize=(12, 19))
ax.set_xlim(-2.5, 9.5)
ax.set_ylim(26, -1.2)
ax.axis("off")

XM, XS, XS2 = 0.0, 3.4, 6.6
pos = {
    "S": (XM, 0.0), "P1a": (XM, 1.7), "P1b": (XM, 2.55), "R": (XS, 2.1),
    "P2": (XM, 3.9), "T1": (XS, 3.9),
    "P3": (XM, 5.5), "T2": (XS, 5.5), "T3": (XS2, 5.5),
    "P4": (XM, 7.1), "Z1": (XS, 7.1),
    "P5": (XM, 8.7), "Z2": (XS, 8.7),
    "P6": (XM, 10.3), "Z3": (XS, 10.3),
    "P7": (XM, 11.9), "W1": (XS, 11.9),
    "P8": (XM, 13.5), "F1": (XS, 13.5),
    "P9": (XM, 15.1), "F2": (XS, 15.1),
    "P10": (XM, 16.7), "P11": (XS, 16.7), "K1": (XS2, 16.7),
    "P12": (XM, 18.3), "M1": (XS, 18.3),
    "P13": (XM, 19.9), "I1": (XS, 19.9),
    "RET": (XM, 21.5), "End": (XM, 23.1),
}

textos = {
    "S": "1  S: def calc",
    "P1a": "2  P1a: p<=0", "P1b": "3  P1b: p>50", "R": "4  raise ValueError",
    "P2": "5  P2: p<=L1", "T1": "6  t=6000",
    "P3": "7  P3: p<=L2", "T2": "8  t=9000", "T3": "9  t=9000+(p-L2)*800",
    "P4": "10  P4: z==urbana", "Z1": "11  t=t",
    "P5": "12  P5: z==rural", "Z2": "13  t+=t*RR",
    "P6": "14  P6: z==nacional", "Z3": "15  t+=t*RN",
    "P7": "16  P7: d>6", "W1": "17  t+=S",
    "P8": "18  P8: c==frecuente", "F1": "19  t-=t*0.05",
    "P9": "20  P9: c==vip", "F2": "21  t-=t*V",
    "P10": "22  P10: cup!=None", "P11": "23  P11: cup==ENVIO10", "K1": "24  t-=t*0.10",
    "P12": "25  P12: t<5000", "M1": "26  t=5000",
    "P13": "27  P13: flag", "I1": "28  print",
    "RET": "29  return int(t/100)*100", "End": "30  End",
}
rombos = {"P1a", "P1b", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "P12", "P13"}

for nid, (x, y) in pos.items():
    ancho = 2.0 if nid in rombos else 2.4
    caja(ax, x, y, textos[nid], ancho=ancho, rombo=nid in rombos)

aristas = [
    ("S", "P1a", None), ("P1a", "R", "sí"), ("P1a", "P1b", "no"),
    ("P1b", "R", "sí"), ("P1b", "P2", "no"), ("R", "End", None),
    ("P2", "T1", "sí"), ("T1", "P4", None), ("P2", "P3", "no"),
    ("P3", "T2", "sí"), ("T2", "P4", None), ("P3", "T3", "no"), ("T3", "P4", None),
    ("P4", "Z1", "sí"), ("Z1", "P7", None), ("P4", "P5", "no"),
    ("P5", "Z2", "sí"), ("Z2", "P7", None), ("P5", "P6", "no"),
    ("P6", "Z3", "sí"), ("Z3", "P7", None), ("P6", "P7", "no"),
    ("P7", "W1", "sí"), ("W1", "P8", None), ("P7", "P8", "no"),
    ("P8", "F1", "sí"), ("F1", "P10", None), ("P8", "P9", "no"),
    ("P9", "F2", "sí"), ("F2", "P10", None), ("P9", "P10", "no"),
    ("P10", "P11", "sí"), ("P10", "P12", "no"),
    ("P11", "K1", "sí"), ("K1", "P12", None), ("P11", "P12", "no"),
    ("P12", "M1", "sí"), ("M1", "P13", None), ("P12", "P13", "no"),
    ("P13", "I1", "sí"), ("I1", "RET", None), ("P13", "RET", "no"),
    ("RET", "End", None),
]
for a, b, et in aristas:
    flecha(ax, pos[a], pos[b], et)

ax.set_title("Grafo de flujo de calc() v1.0.0 — N=30, E=43, M=15", fontsize=11)
plt.tight_layout()
plt.savefig("evidence/grafo_flujo.png", dpi=150, bbox_inches="tight")
print("PNG generado: evidence/grafo_flujo.png")
