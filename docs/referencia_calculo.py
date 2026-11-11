"""Referencia de cálculo independiente (aritmética Decimal).

Este módulo NO importa ni ejecuta envios.py. Implementa la especificación
R1-R8 desde cero para obtener los resultados esperados de los casos de prueba.

Código estudiantil 0182410093 -> A=4 B=1 C=0 D=0 E=9 F=3
PMAX=50, L1=3, L2=10, RR=15%, RN=40%, V=15%, S=2000, CAMBIO=1
D par: tramo1 incluye limite. E impar: finde despues de descuentos.
B impar: ambos descuentos. F impar: cupon inexistente = error.
"""

from decimal import Decimal, ROUND_HALF_UP

PMAX = Decimal(50)
L1 = Decimal(3)
L2 = Decimal(10)
RR = Decimal("0.15")
RN = Decimal("0.40")
V = Decimal("0.15")
S = Decimal(2000)
MINIMO = Decimal(5000)
ZONAS = ("urbana", "rural", "nacional")


def calcular(peso, zona, cliente, dia, cupon=None):
    p = Decimal(str(peso))
    if not (Decimal(0) < p <= PMAX):
        raise ValueError("peso inválido")
    if zona not in ZONAS:
        raise ValueError("zona inválida")
    if not (isinstance(dia, int) and 1 <= dia <= 7):
        raise ValueError("día inválido")
    if cupon is not None and cupon != "ENVIO10":
        raise ValueError("cupón inválido")

    if p <= L1:
        t = Decimal(6000)
    elif p <= L2:
        t = Decimal(9000)
    else:
        t = Decimal(9000) + (p - L2) * Decimal(800)

    if zona == "rural":
        t = t * (Decimal(1) + RR)
    elif zona == "nacional":
        t = t * (Decimal(1) + RN)

    if cliente == "frecuente":
        t = t * (Decimal(1) - Decimal("0.05"))
    elif cliente == "vip":
        t = t * (Decimal(1) - V)

    if cupon == "ENVIO10":
        t = t * (Decimal(1) - Decimal("0.10"))

    if dia in (6, 7):
        t = t + S

    if t < MINIMO:
        t = MINIMO

    t = (t / Decimal(100)).quantize(Decimal(1), rounding=ROUND_HALF_UP) * Decimal(100)
    return int(t)


CASOS = [
    ("C01", 2, "urbana", "ninguno", 3, None),
    ("C02", 3, "urbana", "ninguno", 3, None),
    ("C03", 4, "urbana", "ninguno", 3, None),
    ("C04", 10, "urbana", "ninguno", 3, None),
    ("C05", 11, "urbana", "ninguno", 3, None),
    ("C06", 12.5, "urbana", "ninguno", 3, None),
    ("C07", 5, "rural", "ninguno", 3, None),
    ("C08", 5, "nacional", "ninguno", 3, None),
    ("C09", 5, "urbana", "ninguno", 3, None),
    ("C10", 5, "urbana", "frecuente", 3, None),
    ("C11", 5, "urbana", "vip", 3, None),
    ("C12", 5, "urbana", "ninguno", 3, "ENVIO10"),
    ("C13", 5, "urbana", "vip", 3, "ENVIO10"),
    ("C14", 5, "urbana", "frecuente", 3, "ENVIO10"),
    ("C15", 5, "urbana", "ninguno", 6, None),
    ("C16", 5, "urbana", "ninguno", 7, None),
    ("C17", 5, "urbana", "vip", 6, None),
    ("C18", 5, "urbana", "vip", 6, "ENVIO10"),
    ("C24", 50, "urbana", "ninguno", 3, None),
    ("C30", 2, "urbana", "vip", 3, "ENVIO10"),
    ("C31", 10.1, "urbana", "ninguno", 3, None),
    ("C32", 2, "rural", "frecuente", 6, "ENVIO10"),
    ("C33", 10.1, "nacional", "ninguno", 3, None),
]

ERRORES = [
    ("C21", 0, "urbana", "ninguno", 3, None),
    ("C22", -1, "urbana", "ninguno", 3, None),
    ("C23", 51, "urbana", "ninguno", 3, None),
    ("C25", 5, "express", "ninguno", 3, None),
    ("C26", 5, "Urbana", "ninguno", 3, None),
    ("C27", 5, "urbana", "ninguno", 0, None),
    ("C28", 5, "urbana", "ninguno", 8, None),
    ("C19", 5, "urbana", "ninguno", 3, "OTRO"),
    ("C20", 5, "urbana", "ninguno", 3, "ENVIO20"),
]

if __name__ == "__main__":
    print("ID   peso zona      cliente     dia cupon     -> esperado")
    for cid, p, z, c, d, cup in CASOS:
        print(f"{cid:4} {p:<4} {z:<9} {c:<11} {d:<3} {str(cup):<9} -> {calcular(p, z, c, d, cup)}")
    print("\nCasos de error esperado:")
    for cid, p, z, c, d, cup in ERRORES:
        try:
            calcular(p, z, c, d, cup)
            print(f"{cid:4} -> NO lanzó error (inesperado)")
        except ValueError as exc:
            print(f"{cid:4} -> ValueError: {exc}")
