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
