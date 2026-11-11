# Notas de la versión 2.0.0

Fecha: 2026-11-11
Tag: `v2.0.0`
Rama de origen: `refactor/estrategia`

## Resumen

v2.0.0 corrige los siete defectos del heredado (DEF-01…DEF-07) y refactoriza
`envios.py` para eliminar la deuda técnica: constantes, validaciones separadas,
patrón Strategy, `Decimal` y una API pura sin `flag` ni `print`.

## Destacados

- **43/43 pruebas en verde** y **100 % de cobertura** de sentencias y ramas.
- Complejidad ciclomática máxima por bloque: **15 → 3**.
- Complejidad promedio: **15,0 → 1,76** (`radon`, 25 bloques).
- Cálculo monetario exacto con `Decimal` y redondeo *half-up* a múltiplos de 100.
- Errores específicos mediante `ErrorEnvio`, subclase de `ValueError`.

## Cambios incompatibles (breaking changes)

| Antes (v1.0.0) | Ahora (v2.0.0) | Acción de migración |
|----------------|----------------|---------------------|
| `calc(p, z, c, d, cup, flag=False)` | `calc(peso, zona, cliente, dia, cupon)` | Eliminar el argumento `flag` |
| `calc(..., flag=True)` imprime | `calc` nunca imprime | Imprimir en el llamador con el valor retornado |
| Retorna `int` | Retorna `Decimal` | Convertir con `int()`/`float()` solo al presentar |
| `ValueError("peso invalido")` | `ErrorEnvio` con mensaje específico | Capturar `ErrorEnvio` o `ValueError` |
| Zona inválida se ignoraba | `ErrorEnvio` | Validar antes de llamar o capturar |
| Cupón inválido se ignoraba | `ErrorEnvio` | Validar antes de llamar o capturar |

## Migración paso a paso

```python
# v1.0.0
total = calc(5, "urbana", "vip", 3, "ENVIO10", flag=True)

# v2.0.0
from envios import calc, ErrorEnvio

try:
    total = calc(5, "urbana", "vip", 3, "ENVIO10")
    print("costo:", total)
except ErrorEnvio as error:
    print("entrada inválida:", error)
```

## Verificación

```powershell
python -m pytest -q --cov=envios --cov-branch
python -m radon cc envios.py -s -a
```

Salida esperada: `43 passed`, cobertura 100 %, complejidad promedio A (1,76).

## Limitaciones conocidas

- La regla `CAMBIO=1` (cliente empresarial) se implementa en v2.1.0, no en esta
  versión.
- La salida sigue siendo un `Decimal`; el formato de presentación es
  responsabilidad del llamador.

## Archivos principales

- `envios.py` — implementación v2.0.0.
- `docs/06_refactorizacion.md` — malos olores, UML y tabla antes/después.
- `docs/07_configuracion.md` — gestión de parámetros.
- `CHANGELOG.md` — historial de versiones.
