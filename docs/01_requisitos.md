# 01 · Requisitos (R1–R8)

Especificación funcional del cálculo de costos de envío, particularizada con los
parámetros del código **0182410093**.

## Parámetros de referencia

| PMAX | L1 | L2 | RR | RN | V | S | D | E | B | F |
|------|----|----|----|----|----|-------|---|---|---|---|
| 50 kg | 3 kg | 10 kg | 15 % | 40 % | 15 % | $2.000 | par | impar | impar | impar |

Reglas de paridad vigentes:

- **D = 0 (par):** el tramo 1 incluye el límite → `peso ≤ L1`.
- **E = 9 (impar):** el recargo de fin de semana se aplica **después** de los descuentos.
- **B = 1 (impar):** se aplican **ambos** descuentos (cliente y luego cupón).
- **F = 3 (impar):** un cupón inexistente **es un error** (`ValueError`).

---

## R1 · Validación del peso

- Entrada `peso` numérico.
- Válido si `0 < peso ≤ PMAX`, es decir `0 < peso ≤ 50`.
- Si no se cumple, lanzar `ValueError("peso inválido")`.
- El límite superior **50 es válido**; 50,01 y 51 no lo son.

## R2 · Validación de zona y día

- `zona ∈ {"urbana", "rural", "nacional"}` (sensible a mayúsculas). Cualquier otro
  valor lanza `ValueError`.
- `día` debe ser un entero en `[1, 7]`. Valores como `0`, `8` o no enteros lanzan
  `ValueError`.
- Día 6 = sábado, día 7 = domingo; 1–5 son días entre semana.

## R3 · Cálculo por tramos de peso

| Condición | Costo base |
|-----------|------------|
| `peso ≤ 3` (L1, incluido por D par) | $6.000 |
| `3 < peso ≤ 10` (L2, incluido) | $9.000 |
| `peso > 10` | `$9.000 + $800 · (peso − 10)` |

En el tercer tramo el cobro por kilogramo adicional es **proporcional** (admite
peso decimal, p. ej. 10,1 kg → $9.080).

## R4 · Recargo por zona

| Zona | Recargo |
|------|---------|
| urbana | 0 % |
| rural | +15 % (RR) |
| nacional | +40 % (RN) |

El recargo se aplica sobre el costo base del tramo.

## R5 · Recargo de fin de semana

- Sábado (6) y domingo (7): se suma **$2.000** (S).
- Por **E impar**, el recargo se aplica **después** de los descuentos.
- Días 1–5: sin recargo.

## R6 · Descuentos

| Cliente | Descuento |
|---------|-----------|
| frecuente | 5 % |
| vip | 15 % (V) |
| ninguno | 0 % |

| Cupón | Descuento |
|-------|-----------|
| `ENVIO10` | 10 % |
| ausente (`None`) | 0 % |

Por **B impar**, si hay cliente con descuento **y** cupón válido, se aplican
**ambos**: primero el descuento de cliente y luego el del cupón (multiplicativo).

## R7 · Cupón inexistente

Por **F impar**, si `cupón` no es `None` y no es `"ENVIO10"`, se lanza
`ValueError`. Un cupón ausente (`None`) es válido y no descuenta.

## R8 · Costo mínimo y redondeo

- Costo mínimo final: **$5.000**.
- Redondeo al múltiplo de **$100** más cercano, con **half-up**: los $50
  exactos redondean hacia arriba.
  - Ej.: $10.350 → $10.400; $8.550 → $8.600; $10.115 → $10.100.

## Orden de operaciones (obligatorio)

```
1. Validar peso, zona, día y cupón
2. Costo base por tramo (R3)
3. Recargo de zona (R4)
4. Descuento de cliente y luego cupón (R6)
5. Recargo de fin de semana (R5, después por E impar)
6. Aplicar mínimo $5.000 (R8)
7. Redondear half-up a $100 (R8)
```

> El orden 4 → 5 es determinante: con E impar el fin de semana se suma **después**
> de los descuentos, no antes.

---

## Ejemplo de verificación del método (código ajeno 2023184706)

No corresponde a mis parámetros; se usa **solo** para validar el procedimiento de
cálculo. Con ese código: PMAX=35, L1=4, L2=14, RR=10 %, RN=40 %, V=15 %, S=2000,
D=7 (impar → tramo1 `peso < L1`), E=0 (par → finde antes), B=8 (par → solo el
mayor descuento), F=6 (par → cupón inexistente se ignora).

Caso: peso 4, rural, vip, día 6, ENVIO10.

```
Tramo: 4 < 4 es falso → tramo 2 = 9000
Rural +10 %          → 9000 · 1,10 = 9900
Finde (E par, antes) → 9900 + 2000 = 11900
Descuentos (B par, solo el mayor: vip 15 % > cupón 10 %) → 11900 · 0,85 = 10115
Mínimo 5000          → 10115
Redondeo half-up     → 10100   ✔ coincide con el ejemplo oficial ($10.100)
```

Esto confirma que el método (orden de operaciones y redondeo) es correcto antes de
compararlo contra el código heredado.
