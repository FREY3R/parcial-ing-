# 03 · Caja negra

Diseño de casos **desde la especificación**, sin mirar el código heredado. Todos
los valores esperados se obtuvieron con la calculadora independiente
`docs/referencia_calculo.py` (Decimal) y se verificaron paso a paso.

## 1. Particiones de equivalencia

### 1.1 Peso (R1, R3)

| Clase | Rango | Tipo | Representante |
|-------|-------|------|---------------|
| P-V1 | `0 < p ≤ 3` (tramo 1) | válida | 2 |
| P-V2 | `3 < p ≤ 10` (tramo 2) | válida | 5 |
| P-V3 | `10 < p ≤ 50` (tramo 3) | válida | 12,5 |
| P-I1 | `p ≤ 0` | inválida | 0 y −1 |
| P-I2 | `p > 50` | inválida | 51 |

### 1.2 Zona (R2, R4)

| Clase | Valor | Tipo | Representante |
|-------|-------|------|---------------|
| Z-V1 | `urbana` | válida | urbana |
| Z-V2 | `rural` | válida | rural |
| Z-V3 | `nacional` | válida | nacional |
| Z-I1 | otro texto | inválida | `express` |
| Z-I2 | distinta capitalización | inválida | `Urbana` |

### 1.3 Cliente (R6)

| Clase | Valor | Tipo | Representante |
|-------|-------|------|---------------|
| C-V1 | `ninguno` | válida (0 %) | ninguno |
| C-V2 | `frecuente` | válida (5 %) | frecuente |
| C-V3 | `vip` | válida (15 %) | vip |

> La especificación no define error para un cliente desconocido; se comporta como
> sin descuento. Solo se prueban las categorías definidas.

### 1.4 Día (R2, R5)

| Clase | Rango | Tipo | Representante |
|-------|-------|------|---------------|
| D-V1 | 1–5 (entre semana) | válida | 3 |
| D-V2 | 6 (sábado) | válida | 6 |
| D-V3 | 7 (domingo) | válida | 7 |
| D-I1 | `d ≤ 0` | inválida | 0 |
| D-I2 | `d ≥ 8` | inválida | 8 |

### 1.5 Cupón (R6, R7)

| Clase | Valor | Tipo | Representante |
|-------|-------|------|---------------|
| K-V1 | `None` (ausente) | válida | None |
| K-V2 | `ENVIO10` | válida (10 %) | ENVIO10 |
| K-I1 | otro texto | inválida (F impar → error) | `OTRO`, `ENVIO20` |

---

## 2. Valores límite

Con **D par**, el tramo 1 **incluye** `L1 = 3`. Con L2 y PMAX los límites son
inclusivos según R3 y R1.

### 2.1 Peso

| Punto | Valor | Esperado | Motivo |
|-------|-------|----------|--------|
| Bajo 0 | −0,01 | `ValueError` | fuera de rango |
| Límite 0 | 0 | `ValueError` | 0 no es válido |
| Justo sobre 0 | 0,01 | $6.000 | tramo 1 |
| Justo bajo L1 | 2,99 | $6.000 | tramo 1 |
| **L1 exacto** | **3** | **$6.000** | **incluido por D par** |
| Justo sobre L1 | 3,01 | $9.000 | tramo 2 |
| Justo bajo L2 | 9,99 | $9.000 | tramo 2 |
| **L2 exacto** | **10** | **$9.000** | **incluido** |
| Justo sobre L2 | 10,01 | $9.000 + 0,01·800 = $9.008 → $9.000 | tramo 3 |
| Justo bajo PMAX | 49,99 | $9.000 + 39,99·800 = $40.992 → $41.000 | tramo 3 |
| **PMAX exacto** | **50** | **$41.000** | **válido** |
| Sobre PMAX | 50,01 | `ValueError` | fuera de rango |

> El caso 10,01 es especialmente útil: el valor intermedio $9.008 redondea a
> $9.000, pero con aritmética `float` y truncamiento el heredado puede devolver
> otro valor. Se prueba con 10,1 en C31 para hacerlo evidente.

### 2.2 Día

| Valor | Esperado | Motivo |
|-------|----------|--------|
| 0 | `ValueError` | fuera de [1,7] |
| 1 | sin recargo | lunes |
| 5 | sin recargo | viernes |
| **6** | **+$2.000** | **sábado (R5)** |
| **7** | **+$2.000** | **domingo** |
| 8 | `ValueError` | fuera de [1,7] |

### 2.3 Zona y cupón

| Entrada | Esperado |
|---------|----------|
| `urbana` / `rural` / `nacional` | válidas |
| `express`, `Urbana`, `""` | `ValueError` |
| cupón `None` | válido, sin descuento |
| cupón `ENVIO10` | válido, −10 % |
| cupón `OTRO` / `ENVIO20` | `ValueError` (F impar) |

---

## 3. Tabla de decisión

Condiciones: **B impar** → se aplican ambos descuentos (cliente y luego cupón);
**E impar** → el recargo de fin de semana se suma **después** de los descuentos.

| # | Cliente | Cupón | ¿Finde? | Secuencia aplicada | Ejemplo (base $9.000) |
|---|---------|-------|---------|--------------------|-----------------------|
| 1 | ninguno | None | No | base | 9000 |
| 2 | ninguno | None | Sí | base + 2000 | 11000 |
| 3 | ninguno | ENVIO10 | No | base · 0,90 | 8100 |
| 4 | ninguno | ENVIO10 | Sí | base · 0,90 + 2000 | 10100 |
| 5 | frecuente | None | No | base · 0,95 | 8550 → 8600 |
| 6 | frecuente | None | Sí | base · 0,95 + 2000 | 10550 → 10600 |
| 7 | frecuente | ENVIO10 | No | base · 0,95 · 0,90 | 7695 → 7700 |
| 8 | frecuente | ENVIO10 | Sí | base · 0,95 · 0,90 + 2000 | 9695 → 9700 |
| 9 | vip | None | No | base · 0,85 | 7650 → 7700 |
| 10 | vip | None | Sí | base · 0,85 + 2000 | 9650 → 9700 |
| 11 | vip | ENVIO10 | No | base · 0,85 · 0,90 | 6885 → 6900 |
| 12 | vip | ENVIO10 | Sí | base · 0,85 · 0,90 + 2000 | 8885 → 8900 |

**Lectura clave de la tabla:**

- Si **B fuera par** (no es el caso), las filas 7, 8, 11 y 12 aplicarían solo el
  mayor descuento (VIP 15 %), no ambos.
- Si **E fuera par** (no es el caso), el `+2000` se aplicaría **antes** de los
  descuentos, cambiando las filas 2, 4, 6, 8, 10 y 12.
- El cupón inexistente no aparece en la tabla porque, con **F impar**, es un
  error y no una combinación válida.

---

## 4. Matriz de casos de prueba (30 casos)

| ID | Req. | Peso | Zona | Cliente | Día | Cupón | Resultado esperado | Técnica |
|----|------|------|------|---------|-----|-------|--------------------|---------|
| C01 | R3 | 2 | urbana | ninguno | 3 | — | $6.000 | PE tramo 1 |
| C02 | R3 | 3 | urbana | ninguno | 3 | — | $6.000 | VL L1 (incluido) |
| C03 | R3 | 4 | urbana | ninguno | 3 | — | $9.000 | PE tramo 2 |
| C04 | R3 | 10 | urbana | ninguno | 3 | — | $9.000 | VL L2 (incluido) |
| C05 | R3 | 11 | urbana | ninguno | 3 | — | $9.800 | VL L2+1 |
| C06 | R3 | 12,5 | urbana | ninguno | 3 | — | $11.000 | PE tramo 3 proporcional |
| C07 | R4, R8 | 5 | rural | ninguno | 3 | — | $10.400 | PE zona + half-up |
| C08 | R4 | 5 | nacional | ninguno | 3 | — | $12.600 | PE zona |
| C09 | R4 | 5 | urbana | ninguno | 3 | — | $9.000 | PE zona sin recargo |
| C10 | R6, R8 | 5 | urbana | frecuente | 3 | — | $8.600 | PE cliente + half-up |
| C11 | R6 | 5 | urbana | vip | 3 | — | $7.700 | PE cliente |
| C12 | R6 | 5 | urbana | ninguno | 3 | ENVIO10 | $8.100 | PE cupón |
| C13 | R6 | 5 | urbana | vip | 3 | ENVIO10 | $6.900 | TD ambos (B impar) |
| C14 | R6 | 5 | urbana | frecuente | 3 | ENVIO10 | $7.700 | TD ambos (B impar) |
| C15 | R5 | 5 | urbana | ninguno | 6 | — | $11.000 | VL sábado |
| C16 | R5 | 5 | urbana | ninguno | 7 | — | $11.000 | VL domingo |
| C17 | R5, E | 5 | urbana | vip | 6 | — | $9.700 | TD orden finde |
| C18 | R5, E | 5 | urbana | vip | 6 | ENVIO10 | $8.900 | TD orden + ambos |
| C19 | R7 | 5 | urbana | ninguno | 3 | OTRO | `ValueError` | PE cupón inválido |
| C20 | R7 | 5 | urbana | ninguno | 3 | ENVIO20 | `ValueError` | PE cupón inválido |
| C21 | R1 | 0 | urbana | ninguno | 3 | — | `ValueError` | VL peso 0 |
| C22 | R1 | −1 | urbana | ninguno | 3 | — | `ValueError` | PE peso inválido |
| C23 | R1 | 51 | urbana | ninguno | 3 | — | `ValueError` | VL PMAX+1 |
| C24 | R1, R3 | 50 | urbana | ninguno | 3 | — | $41.000 | VL PMAX válido |
| C25 | R2 | 5 | express | ninguno | 3 | — | `ValueError` | PE zona inválida |
| C26 | R2 | 5 | Urbana | ninguno | 3 | — | `ValueError` | PE capitalización |
| C27 | R2 | 5 | urbana | ninguno | 0 | — | `ValueError` | VL día 0 |
| C28 | R2 | 5 | urbana | ninguno | 8 | — | `ValueError` | VL día 8 |
| C29 | R2 | 5 | urbana | ninguno | 6,5 | — | `ValueError` | Día no entero |
| C30 | R8 | 2 | urbana | vip | 3 | ENVIO10 | $5.000 | Mínimo |
| C31 | R3, R8 | 10,1 | urbana | ninguno | 3 | — | $9.100 | Proporcional + float |
| C32 | R5, R6 | 2 | rural | frecuente | 6 | ENVIO10 | $7.900 | Integración |
| C33 | R3, R4 | 10,1 | nacional | ninguno | 3 | — | $12.700 | Integración |

> **Casos que afloran defectos reales del heredado:** C15 y C16 (sábado/domingo
> por `d > 6`), C17 y C18 (orden del fin de semana), C19 y C20 (cupón
> inexistente), C25–C28 (validaciones), C07/C10/C13 (redondeo half-up), C31
> (truncamiento y `float`).

---

## 5. Cálculo paso a paso (7 casos)

Formato idéntico al ejemplo oficial: se parte del tramo, se aplican recargos y
descuentos en el orden de la especificación, luego mínimo y redondeo half-up.

### C07 · peso 5, rural, ninguno, día 3, sin cupón

```
Tramo: 5 > 3 y 5 ≤ 10        → tramo 2 = 9000
Rural +15 %                   → 9000 · 1,15 = 10350
Descuentos                    → 10350 (ninguno)
Fin de semana                 → no aplica (día 3)
Mínimo 5000                   → 10350
Redondeo half-up              → 10350/100 = 103,5 → 104 → 10400
```

### C10 · peso 5, urbana, frecuente, día 3, sin cupón

```
Tramo                         → 9000
Zona urbana                   → 9000
Frecuente −5 %                → 9000 · 0,95 = 8550
Fin de semana                 → no aplica
Mínimo                        → 8550
Redondeo half-up              → 85,5 → 86 → 8600
```

### C13 · peso 5, urbana, vip, día 3, ENVIO10 (B impar → ambos)

```
Tramo                         → 9000
Zona urbana                   → 9000
VIP −15 %                     → 9000 · 0,85 = 7650
Cupón −10 %                   → 7650 · 0,90 = 6885
Fin de semana                 → no aplica
Mínimo                        → 6885
Redondeo half-up              → 68,85 → 69 → 6900
```

### C17 · peso 5, urbana, vip, día 6 (E impar → finde después)

```
Tramo                         → 9000
Zona urbana                   → 9000
VIP −15 %                     → 9000 · 0,85 = 7650
Fin de semana (después) +2000 → 7650 + 2000 = 9650
Mínimo                        → 9650
Redondeo half-up              → 96,5 → 97 → 9700
```

> Si el finde se aplicara antes (como hace el heredado) daría
> `(9000 + 2000) · 0,85 = 9350 → 9400`, distinto de $9.700.

### C30 · peso 2, urbana, vip, día 3, ENVIO10 (mínimo)

```
Tramo (2 ≤ 3)                 → 6000
Zona urbana                   → 6000
VIP −15 %                     → 6000 · 0,85 = 5100
Cupón −10 %                   → 5100 · 0,90 = 4590
Fin de semana                 → no aplica
Mínimo 5000                   → 4590 < 5000 → 5000
Redondeo                      → 5000
```

### C31 · peso 10,1, urbana, ninguno, día 3 (proporcional + float)

```
Tramo: 10,1 > 10              → 9000 + (10,1 − 10)·800
                              → 9000 + 0,1·800 = 9000 + 80 = 9080
Zona urbana                   → 9080
Descuentos                    → 9080
Fin de semana                 → no aplica
Mínimo                        → 9080
Redondeo half-up              → 90,8 → 91 → 9100
```

> Con `float`, `10.1 - 10 = 0.09999999999999964`; el heredado obtiene
> `9079.99…` y trunca a `9000`. Esperado correcto: **$9.100**.

### C32 · peso 2, rural, frecuente, día 6, ENVIO10 (integración)

```
Tramo (2 ≤ 3)                 → 6000
Rural +15 %                   → 6000 · 1,15 = 6900
Frecuente −5 %                → 6900 · 0,95 = 6555
Cupón −10 %                   → 6555 · 0,90 = 5899,5
Fin de semana (después) +2000 → 5899,5 + 2000 = 7899,5
Mínimo                        → 7899,5
Redondeo half-up              → 78,995 → 79 → 7900
```
