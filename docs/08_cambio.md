# 08 · Gestión del cambio — `CAMBIO = 1`

## 1. Identificación del cambio

| Campo | Valor |
|-------|-------|
| Código de cambio | `CAMBIO = 1` |
| Origen | Indicación del docente (video de la Parte 8) |
| Rama | `feature/cambio-1` |
| Versión que lo entrega | `v2.1.0` |
| Tipo | **Adaptativo** (nuevo requisito del cliente) |
| Estado | Implementado y verificado |

## 2. Requisito nuevo

Cuando `CAMBIO = 1`:

1. **Cliente empresarial:** paga un descuento del **12 %** sobre el costo con
   recargo de zona.
2. **Peso mayor que `L2`:** **no se cobra recargo de zona**, sin importar la zona
   ni el cliente.

## 3. Decisiones de interpretación

| Duda | Decisión | Justificación |
|------|----------|---------------|
| ¿El 12 % aplica antes o después del cupón? | Cliente primero, cupón después | Consistente con B impar (ambos descuentos, cliente → cupón) |
| ¿El 12 % aplica antes o después del fin de semana? | Antes | Se mantiene el orden oficial: descuentos → finde |
| ¿"Peso > L2" incluye exactamente `L2`? | No; solo estrictamente mayor | El texto dice "supera L2"; en `L2` se conserva el recargo |
| ¿La exención de zona aplica a todos los clientes? | Sí | La regla está redactada sobre el peso, no sobre el cliente |
| ¿El mínimo de $5.000 se aplica después? | Sí | El mínimo es la última regla antes del redondeo |
| ¿El empresarial puede usar cupón y fin de semana? | Sí | No se excluye; se suman las reglas existentes |

## 4. Análisis de impacto

| Artefacto | Cambio |
|-----------|--------|
| `envios.py` | Nueva constante `CAMBIO`, `DESC_EMPRESARIAL`; nueva estrategia `DescuentoEmpresarial`; guarda de zona en `calc` |
| `tests/test_envios.py` | C33 actualizado; nuevos C34–C42 (válidos) y C43–C44 (errores); prueba `test_cambio_activo` |
| `docs/00_parametros.md` | Ya documenta `CAMBIO = 1` |
| `docs/07_configuracion.md` | Matriz v2.1.0 |
| `CHANGELOG.md` | Sección `[2.1.0]` |
| `docs/notas_v2.1.0.md` | Notas de la versión |

### Funciones afectadas

- `calc`: decide si aplica el recargo de zona (`CAMBIO == 1 and peso > L2`).
- `ESTRATEGIAS_CLIENTE`: agrega `"empresarial"`.
- `DescuentoEmpresarial.aplicar`: nueva estrategia.
- `costo_base`, validaciones, finde, mínimo y redondeo: **sin cambios**.

## 5. Análisis de riesgo

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Cambiar el resultado de casos existentes con `peso > L2` y zona | Alta | Medio | Se identificó solo C33; se actualizó su esperado a $9.100 |
| Confundir `>` con `>=` en el límite `L2` | Media | Medio | Caso C39 con `peso = 10` conserva recargo; C40 con `10,1` no |
| Olvidar que la exención aplica a todos los clientes | Media | Bajo | Casos C38 (ninguno) y C40 (rural, ninguno) |
| Duplicar lógica de descuento | Baja | Bajo | Se reutiliza el patrón Strategy |
| Romper la API | Baja | Alto | No cambia la firma de `calc`; solo se agrega un valor de cliente |

## 6. Plan TDD aplicado

1. **Rojo:** se actualizó C33 y se agregaron C34–C44 y `test_cambio_activo`.
   Resultado: **10 fallos, 45 pasan**.
2. **Verde:** se agregaron `CAMBIO`, `DESC_EMPRESARIAL`,
   `DescuentoEmpresarial` y la guarda de zona. Resultado: **55/55 pasan**,
   cobertura **100 %** de sentencias y ramas.
3. **Refactor:** no fue necesario; el cambio se integró al patrón Strategy
   existente.

## 7. Valores esperados de los casos nuevos

| Caso | Entrada | Cálculo | Esperado |
|------|---------|---------|----------|
| C33 | 10,1 · nacional · ninguno · día 3 | base 9.080; sin zona; redondeo | $9.100 |
| C34 | 5 · urbana · empresarial · día 3 | 9.000 × 0,88 = 7.920 | $7.900 |
| C35 | 5 · urbana · empresarial · ENVIO10 | 7.920 × 0,90 = 7.128 | $7.100 |
| C36 | 5 · rural · empresarial · sábado | 9.000 × 1,15 × 0,88 + 2.000 = 11.108 | $11.100 |
| C37 | 11 · rural · empresarial | sin zona: 9.800 × 0,88 = 8.624 | $8.600 |
| C38 | 11 · nacional · ninguno | sin zona: 9.800 | $9.800 |
| C39 | 10 · nacional · ninguno | 9.000 × 1,40 = 12.600 (L2 exacto) | $12.600 |
| C40 | 10,1 · rural · ninguno | sin zona: 9.080 | $9.100 |
| C41 | 5 · urbana · empresarial · sábado | 7.920 + 2.000 = 9.920 | $9.900 |
| C42 | 2 · urbana · empresarial · ENVIO10 | 6.000 × 0,88 × 0,90 = 4.752 → mínimo | $5.000 |

## 8. Verificación

```powershell
python -m pytest -q --cov=envios --cov-branch --cov-report=term-missing
```

Resultado: **55 passed**, `envios.py` 100 % de sentencias y 100 % de ramas.

Evidencia: `evidence/v2.1.0_pytest.txt` y `.png`.

## 9. Plan de reversión

Si el cambio no se aprueba, basta con volver al tag `v2.0.0`. La rama
`feature/cambio-1` es independiente y se integró con `--no-ff`, por lo que un
`git revert -m 1 <merge>` restaura el comportamiento anterior sin perder la
historia.
