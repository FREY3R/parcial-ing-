# 00 · Parámetros personalizados

**Estudiante:** Yerfreth Mejía Sierra
**Código estudiantil:** 0182410093
**Grupo:** Ingeniería de Sistemas · B1
**Fecha de entrega:** miércoles 11 de noviembre de 2026

---

## 1. Extracción de los dígitos

El código estudiantil es `0182410093`. Se toman sus **6 últimos dígitos**:

```
0 1 8 2 4 1 0 0 9 3
                └─┴─┴─┴─┴─┴── últimos 6 dígitos
```

| Posición | A | B | C | D | E | F |
|----------|---|---|---|---|---|---|
| Dígito   | 4 | 1 | 0 | 0 | 9 | 3 |

---

## 2. Cálculo paso a paso de los parámetros

| Parámetro | Fórmula | Sustitución | Resultado |
|-----------|---------|-------------|-----------|
| **PMAX** | 30 + 5·A | 30 + 5·4 | **50 kg** |
| **L1** | 2 + (B mod 3) | 2 + (1 mod 3) = 2 + 1 | **3 kg** |
| **L2** | 10 + C | 10 + 0 | **10 kg** |
| **RR** | 10 + 5·(E mod 4) % | 10 + 5·(9 mod 4) = 10 + 5·1 | **15 %** |
| **RN** | 40 + 5·(F mod 3) % | 40 + 5·(3 mod 3) = 40 + 5·0 | **40 %** |
| **V** | 10 + 5·(A mod 3) % | 10 + 5·(4 mod 3) = 10 + 5·1 | **15 %** |
| **S** | 2000 + 500·(C mod 4) $ | 2000 + 500·(0 mod 4) = 2000 + 0 | **$2.000** |
| **CAMBIO** | (A + F) mod 3 | (4 + 3) mod 3 = 7 mod 3 | **1** |

Verificación de módulos:

- `B mod 3 = 1 mod 3 = 1`
- `E mod 4 = 9 mod 4 = 1`
- `F mod 3 = 3 mod 3 = 0`
- `A mod 3 = 4 mod 3 = 1`
- `C mod 4 = 0 mod 4 = 0`
- `(A + F) mod 3 = 7 mod 3 = 1`

---

## 3. Tabla de parámetros (validación)

| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO |
|---|---|---|---|---|--------|----|----|----|----|----|----|-------|--------|
| 4 | 1 | 0 | 0 | 9 | 3 | 50 kg | 3 kg | 10 kg | 15 % | 40 % | 15 % | $2.000 | 1 |

---

## 4. Reglas de paridad aplicables

| Regla | Dígito | Paridad | Consecuencia |
|-------|--------|---------|--------------|
| D → tramo 1 | D = 0 | **par** | El tramo 1 **incluye** el límite: se cobra $6.000 si `peso ≤ L1` (≤ 3 kg). |
| E → orden recargo finde | E = 9 | **impar** | El recargo de fin de semana se aplica **DESPUÉS** de los descuentos. |
| B → combinación descuentos | B = 1 | **impar** | Se aplican **ambos** descuentos: primero cliente y luego cupón. |
| F → cupón inexistente | F = 3 | **impar** | Un cupón inexistente **es un error** (`ValueError`). |

---

## 5. Configuración derivada para `envios.py`

```python
CONFIG = {
    "L1": 3,
    "L2": 10,
    "RECARGO_RURAL": 0.15,      # 15 %
    "RECARGO_NACIONAL": 0.40,   # 40 %
    "DESC_VIP": 0.15,           # 15 %
    "RECARGO_FINDE": 2000,      # $2.000
}
```

> **Nota sobre PMAX:** el código heredado valida `p > 50`. Para mis parámetros
> `PMAX = 50`, por lo que el valor coincide con la especificación. Aun así, se
> documenta como *número mágico* (deuda técnica) en la Parte 6, porque no deriva
> de una constante nombrada.
