# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y versionado [SemVer](https://semver.org/lang/es/).

## [Unreleased]

## [2.1.0] - 2026-11-11

### Añadido
- Constante `CAMBIO = 1` y descuento `DESC_EMPRESARIAL = 12 %`.
- Estrategia `DescuentoEmpresarial` y cliente `"empresarial"`.
- Exención del recargo de zona cuando `peso > L2` con `CAMBIO = 1`.
- Casos C34–C42 (válidos) y C43–C44 (errores) en la suite.
- Documentación del cambio en `docs/08_cambio.md` y `docs/notas_v2.1.0.md`.

### Cambiado
- C33: peso 10,1 en zona nacional pasa de $12.700 a $9.100 (sin recargo de zona).
- Total de pruebas: 43 → **55**, todas en verde.

## [2.0.0] - 2026-11-11

### Añadido
- Constantes nombradas para tarifas, recargos, descuentos, mínimo y paso de redondeo.
- Validaciones independientes con `ErrorEnvio` (subclase de `ValueError`).
- Patrón Strategy para zonas (`EstrategiaZona`) y descuentos (`EstrategiaDescuento`).
- Uso de `Decimal` y `ROUND_HALF_UP` en todos los cálculos monetarios.
- *Type hints* y *docstrings* en la API pública.
- Documentación de refactorización, UML y notas de versión.

### Cambiado
- `calc` ya no recibe `flag` ni imprime; es una función pura que retorna el costo.
- La firma pasa a `calc(peso, zona, cliente, dia, cupon)`.
- Los mensajes de error son específicos por campo.
- El redondeo pasa de truncamiento (`int`) a *half-up* a múltiplos de 100.

### Corregido
- DEF-01: zona inválida ahora lanza `ErrorEnvio`.
- DEF-02: día fuera de 0…6 ahora lanza `ErrorEnvio`.
- DEF-03: sábado (día 6) recibe recargo de fin de semana.
- DEF-04: el recargo de fin de semana se aplica **después** de los descuentos.
- DEF-05: cupón inexistente ahora lanza `ErrorEnvio`.
- DEF-06: redondeo *half-up* en lugar de truncamiento.
- DEF-07: mensaje `"peso inválido"` con tilde.

### Eliminado
- `CONFIG` global mutable.
- Sentencia inútil `t = t`.
- Comparación `cup != None`.

## [1.0.0] - 2026-11-11

### Añadido
- Versión heredada de `envios.py` con la lógica original y sus siete defectos.
- Documentación de requisitos, caja negra, caja blanca y defectos.
- Tag `v1.0.0` como línea base reproducible del código heredado.

> La suite de 36 pruebas se aplicó a `v1.0.0` desde un *worktree* para generar
> `evidence/v1.0.0_pytest.txt`; el tag conserva solo el código heredado y la
> documentación previa a las pruebas.
