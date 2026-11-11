# 07 · Gestión de la configuración

## 1. Principios

1. **Una sola fuente de verdad:** los parámetros viven como constantes en
   `envios.py`; la documentación (`docs/00_parametros.md`) y la calculadora de
   referencia (`docs/referencia_calculo.py`) repiten los mismos valores.
2. **Sin estado global mutable:** v2.0.0 elimina el diccionario `CONFIG`. Las
   constantes son de solo lectura por convención (`UPPER_CASE`) y no se
   reasignan en tiempo de ejecución.
3. **Sin secretos ni archivos externos:** no se usan `.env`, variables de entorno
   ni credenciales. El proyecto es autocontenido y reproducible.
4. **La configuración se prueba:** la suite fija los valores esperados; si un
   parámetro cambia sin actualizar pruebas y documentación, el build falla.
5. **Versionado SemVer:** un cambio de parámetro que altera resultados es un
   cambio de comportamiento y exige nueva versión (PATCH si corrige, MINOR si
   agrega una regla, MAJOR si rompe la API).

## 2. Parámetros del proyecto

Derivados de los últimos seis dígitos del código `0182410093` → `4 1 0 0 9 3`:

| Símbolo | Valor | Uso | Constante en v2.0.0 |
|---------|-------|-----|---------------------|
| `PMAX` | 50 kg | Peso máximo permitido | `PESO_MAXIMO` |
| `L1` | 3 kg | Límite del tramo 1 | `LIMITE_TRAMO1` |
| `L2` | 10 kg | Límite del tramo 2 | `LIMITE_TRAMO2` |
| `RR` | 15 % | Recargo zona rural | `RECARGO_RURAL` |
| `RN` | 40 % | Recargo zona nacional | `RECARGO_NACIONAL` |
| `V` | 15 % | Descuento cliente VIP | `DESC_VIP` |
| `S` | 2000 | Recargo fin de semana | `RECARGO_FINDE` |
| `CAMBIO` | 1 | Activa la regla de la Parte 8 | `CAMBIO` (v2.1.0) |

Tarifas y reglas fijas (no derivadas del código, pero configurables):

| Constante | Valor | Uso |
|-----------|-------|-----|
| `TARIFA_TRAMO1` | 6000 | Costo base si `peso ≤ L1` |
| `TARIFA_TRAMO2` | 9000 | Costo base si `L1 < peso ≤ L2` |
| `TARIFA_KG_ADICIONAL` | 800 | Costo por kg sobre `L2` |
| `MINIMO` | 5000 | Cobro mínimo |
| `PASO_REDONDEO` | 100 | Múltiplo de redondeo |
| `DESC_FRECUENTE` | 0,05 | Descuento cliente frecuente |
| `DESC_CUPON` | 0,10 | Descuento cupón `ENVIO10` |
| `DESC_EMPRESARIAL` | 0,12 | Descuento cliente empresarial (v2.1.0) |

## 3. Matriz de configuración por versión

| Parámetro | v1.0.0 (heredado) | v2.0.0 (refactor) | v2.1.0 (cambio) |
|-----------|-------------------|-------------------|-----------------|
| `PMAX` | 50 (literal en `if`) | `PESO_MAXIMO = 50` | `PESO_MAXIMO = 50` |
| `L1` / `L2` | `CONFIG["L1"]` / `CONFIG["L2"]` | constantes | constantes |
| `RR` / `RN` | `CONFIG[...]` | constantes | constantes |
| `V` | `CONFIG["DESC_VIP"]` | `DESC_VIP` | `DESC_VIP` |
| `S` | `CONFIG["RECARGO_FINDE"]` | `RECARGO_FINDE` | `RECARGO_FINDE` |
| Descuento frecuente | literal `0.05` | `DESC_FRECUENTE` | `DESC_FRECUENTE` |
| Descuento cupón | literal `0.10` | `DESC_CUPON` | `DESC_CUPON` |
| Mínimo | literal `5000` | `MINIMO` | `MINIMO` |
| Redondeo | `int(t/100)*100` | `PASO_REDONDEO` + half-up | igual |
| `CAMBIO` | no existe | no aplica | `CAMBIO = 1` |
| Cliente empresarial | no existe | no existe | 12 % y sin recargo de zona si `peso > L2` |

## 4. Procedimiento para cambiar un parámetro

1. Editar la constante en `envios.py`.
2. Actualizar `docs/00_parametros.md` y `docs/referencia_calculo.py`.
3. Actualizar los valores esperados en `tests/` que dependan del parámetro.
4. Ejecutar `python -m pytest -q --cov=envios --cov-branch` y verificar 100 %.
5. Registrar el cambio en `CHANGELOG.md` y crear el tag SemVer correspondiente.
6. Si el cambio altera la API, documentar la migración en `docs/notas_vX.Y.Z.md`.

## 5. Qué no es configuración

Los pesos, zonas (`urbana`, `rural`, `nacional`), clientes (`ninguno`,
`frecuente`, `vip`, `empresarial`), días (0…6) y cupones (`ENVIO10`) son
**enumeraciones del dominio**, no parámetros libres. Un valor fuera de esos
conjuntos es un error de entrada y debe lanzar `ErrorEnvio`.

## 6. Verificación de la configuración

```powershell
python -c "import envios; print(envios.PESO_MAXIMO, envios.LIMITE_TRAMO1, envios.LIMITE_TRAMO2)"
python -m pytest -q
```

Los valores deben coincidir con `docs/00_parametros.md` y con la tabla de la
sección 2.
