# Notas de la versión 2.1.0

Fecha: 2026-11-11
Tag: `v2.1.0`
Rama de origen: `feature/cambio-1`
Cambio aplicado: `CAMBIO = 1`

## Resumen

v2.1.0 agrega el cambio solicitado en la Parte 8 sin romper la API de v2.0.0:
cliente **empresarial** con 12 % de descuento y **sin recargo de zona** cuando el
peso supera `L2` (10 kg).

## Comportamiento nuevo

| Regla | Detalle |
|-------|---------|
| Cliente `"empresarial"` | 12 % de descuento, después del recargo de zona y antes del cupón |
| `peso > L2` con `CAMBIO = 1` | No se aplica recargo de zona (rural/nacional), para cualquier cliente |
| `peso = L2` | Sí se aplica el recargo (el límite no se considera "supera") |
| Interacción con cupón | Se acumulan: empresarial y luego `ENVIO10` |
| Interacción con finde | El recargo de fin de semana se suma después de los descuentos |
| Mínimo | Se aplica al final, antes del redondeo |

## Compatibilidad

No hay cambios incompatibles respecto a v2.0.0:

- La firma `calc(peso, zona, cliente, dia, cupon)` no cambia.
- Se agrega un valor válido de `cliente` (`"empresarial"`).
- Los clientes existentes conservan su comportamiento, salvo los casos con
  `peso > L2` y zona rural/nacional, que ahora no pagan recargo de zona.
- El retorno sigue siendo un entero múltiplo de 100.

## Ejemplos

```python
from envios import calc

calc(5, "urbana", "empresarial", 3)              # 7900
calc(5, "urbana", "empresarial", 3, "ENVIO10")   # 7100
calc(11, "rural", "empresarial", 3)              # 8600 (sin recargo de zona)
calc(10, "nacional", "ninguno", 3)               # 12600 (L2 exacto, sí hay zona)
calc(10.1, "nacional", "ninguno", 3)             # 9100  (sin recargo de zona)
```

## Verificación

```powershell
python -m pytest -q --cov=envios --cov-branch
```

Resultado: **55 passed**, cobertura **100 %** de sentencias y ramas.

## Limitaciones conocidas

- `CAMBIO` es una constante de módulo; no se lee de variables de entorno.
- Un cliente distinto de los cuatro válidos no se valida y se trata como
  `"ninguno"`; queda como mejora futura si el cliente lo exige.
- El formato de presentación del monto sigue siendo responsabilidad del llamador.

## Archivos principales

- `envios.py` — implementación v2.1.0.
- `docs/08_cambio.md` — análisis, decisiones, riesgos y plan TDD.
- `docs/07_configuracion.md` — matriz de configuración.
- `CHANGELOG.md` — historial de versiones.
