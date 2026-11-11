# 05 · Registro de defectos

Defectos detectados **comparando el código heredado `v1.0.0` contra la
especificación propia** (R1–R8 con código 0182410093). Solo se reporta lo que es
defecto real con **mis** reglas.

## Resumen

| ID | Título | Requisito | Severidad | Prioridad |
|----|--------|-----------|-----------|-----------|
| DEF-01 | No valida zonas desconocidas | R2 | Alta | Alta |
| DEF-02 | No valida el día (fuera de 1–7 o no entero) | R2 | Alta | Alta |
| DEF-03 | El fin de semana usa `d > 6` y excluye el sábado | R5 | Alta | Alta |
| DEF-04 | Recargo de fin de semana antes de los descuentos | R5 (E impar) | Alta | Media |
| DEF-05 | Ignora cupones inexistentes en vez de lanzar error | R7 (F impar) | Media | Alta |
| DEF-06 | Trunca con `int()` en vez de redondear half-up | R8 | Alta | Alta |
| DEF-07 | Mensaje de peso inválido sin tilde | R1 | Baja | Baja |

**Total: 7 defectos** (5 Alta, 1 Media, 1 Baja).

---

## DEF-01 · No valida zonas desconocidas

- **Requisito incumplido:** R2 (zona ∉ {urbana, rural, nacional} → error).
- **Caso de prueba:** C25, C26.
- **Pasos para reproducir (v1.0.0):**
  ```python
  from envios import calc
  calc(5, "express", "ninguno", 3)   # no lanza error
  calc(5, "Urbana", "ninguno", 3)    # no lanza error
  ```
- **Esperado:** `ValueError("zona inválida")`.
- **Obtenido:** devuelve `9000` en ambos casos (la zona desconocida no suma
  recargo, porque la cadena `if/elif` no tiene rama `else`).
- **Severidad Alta:** acepta envíos a zonas no soportadas y cobra como urbano.
- **Prioridad Alta:** afecta la validez del negocio y es trivial de corregir.

## DEF-02 · No valida el día

- **Requisito incumplido:** R2 (día entero en [1,7]).
- **Caso de prueba:** C27, C28, C29.
- **Pasos:**
  ```python
  calc(5, "urbana", "ninguno", 0)    # día 0
  calc(5, "urbana", "ninguno", 8)    # día 8
  calc(5, "urbana", "ninguno", 6.5)  # no entero
  ```
- **Esperado:** `ValueError("día inválido")` en los tres.
- **Obtenido:** día 0 → `9000`; día 8 y 6,5 → `11000` (entran en `d > 6` y suman
  el recargo de fin de semana).
- **Severidad Alta:** un día inválido altera el cobro.
- **Prioridad Alta:** validación básica de entrada.

## DEF-03 · El fin de semana excluye el sábado

- **Requisito incumplido:** R5 (sábado 6 y domingo 7 → +$2.000).
- **Caso de prueba:** C15 (y `test_sabado_y_domingo`).
- **Pasos:**
  ```python
  calc(5, "urbana", "ninguno", 6)   # sábado
  ```
- **Esperado:** `9000 + 2000 = 11000`.
- **Obtenido:** `9000` (la condición `d > 6` es falsa para 6).
- **Severidad Alta:** deja de cobrar el recargo en la mitad de los fines de semana.
- **Prioridad Alta:** impacto directo en ingresos y caso muy frecuente.

## DEF-04 · Recargo de fin de semana antes de los descuentos

- **Requisito incumplido:** R5 con **E impar** (el recargo va **después** de los
  descuentos).
- **Caso de prueba:** C17, C18 (se usa domingo 7 para aislar el orden de DEF-03).
- **Pasos:**
  ```python
  calc(5, "urbana", "vip", 7)
  ```
- **Esperado:** `9000 · 0,85 + 2000 = 9650 → 9700`.
- **Obtenido:** `(9000 + 2000) · 0,85 = 9350 → 9300` (truncado).
- **Severidad Alta:** cambia el monto para clientes con descuento en fin de semana.
- **Prioridad Media:** solo afecta combinaciones con descuento y fin de semana.

## DEF-05 · Ignora cupones inexistentes

- **Requisito incumplido:** R7 con **F impar** (cupón inexistente = `ValueError`).
- **Caso de prueba:** C19, C20.
- **Pasos:**
  ```python
  calc(5, "urbana", "ninguno", 3, "OTRO")
  calc(5, "urbana", "ninguno", 3, "ENVIO20")
  ```
- **Esperado:** `ValueError("cupón inválido")`.
- **Obtenido:** `9000` (solo compara contra `"ENVIO10"` y calla).
- **Severidad Media:** no altera el monto, pero oculta cupones mal escritos.
- **Prioridad Alta:** la regla de paridad F impar exige el error explícitamente.

## DEF-06 · Truncamiento en lugar de redondeo half-up

- **Requisito incumplido:** R8 (redondeo al múltiplo de $100 más cercano, $50
  hacia arriba).
- **Caso de prueba:** C07, C10, C11, C13, C14 (y `test_redondeo_half_up_sube`).
- **Pasos:**
  ```python
  calc(5, "rural", "ninguno", 3)      # 10350
  calc(5, "urbana", "frecuente", 3)   # 8550
  calc(5, "urbana", "vip", 3)         # 7650
  ```
- **Esperado:** `10400`, `8600`, `7700` (half-up).
- **Obtenido:** `10300`, `8500`, `7600` (`int(t/100)*100` trunca hacia abajo).
- **Severidad Alta:** error sistemático de hasta $100 en muchos envíos.
- **Prioridad Alta:** afecta casi todos los cálculos con decimales de $50.

## DEF-07 · Mensaje de peso inválido sin tilde

- **Requisito incumplido:** R1 exige `ValueError("peso inválido")`.
- **Caso de prueba:** C21, C22, C23.
- **Pasos:**
  ```python
  calc(0, "urbana", "ninguno", 3)
  ```
- **Esperado:** `ValueError("peso inválido")`.
- **Obtenido:** `ValueError("peso invalido")` (sin tilde).
- **Severidad Baja:** el error se lanza; solo difiere el texto.
- **Prioridad Baja:** no afecta el cálculo, pero incumple el contrato exacto.

---

## Revisado y NO reportado como defecto (con mis reglas)

| Aspecto | Por qué no es defecto |
|---------|-----------------------|
| PMAX hardcodeado en 50 | Mis parámetros dan **PMAX = 50**, así que el valor coincide con R1. Es deuda técnica (número mágico), no defecto funcional. |
| Límite del tramo 1 | **D = 0 (par)** exige `peso ≤ L1`; el heredado usa `p <= L1`, correcto. |
| Descuento múltiple | **B = 1 (impar)** exige aplicar ambos; el heredado aplica cliente y luego cupón, correcto. |
| Imprecisión de `float` | Se probó todo el dominio (pesos 0,1–50, todas las zonas/clientes/días/cupones) contra `Decimal`: **0 diferencias** al aplicar half-up correcto. El fallo de C31 se debe al truncamiento (DEF-06), no al `float`. Se mitiga igualmente en el refactor como cambio **preventivo** usando `Decimal`. |

## Métricas

| Métrica | Valor |
|---------|-------|
| Casos ejecutados contra v1.0.0 | 36 |
| Casos que pasan | 14 |
| Casos que fallan | 22 |
| **% de casos que pasan** | **38,9 %** |
| Defectos totales | 7 |
| Defectos por severidad | Alta 5 · Media 1 · Baja 1 |
| Líneas físicas de `envios.py` | 41 |
| **Densidad** | **7 / 41 · 100 ≈ 17,1 defectos por 100 líneas** |
| Sentencias (SLOC) | 29 |
| Densidad por sentencia | 7 / 29 · 100 ≈ 24,1 por 100 sentencias |
| Cobertura de sentencias (v1.0.0) | 28/29 = **96,6 %** |
| Cobertura de ramas (v1.0.0) | 25/26 = **96,2 %** (1 rama parcial) |
| Cobertura reportada por pytest-cov | **96 %** (falta la línea 40, `print` de `flag`) |

> La cobertura alta del heredado no implica corrección: los 22 fallos son de
> **resultado esperado**, no de ejecución. La suite recorre casi todo el código y
> aun así detecta 7 defectos.
