# 02 · Plan de pruebas

## 1. Alcance

El objeto de prueba es la función pública `calc(p, z, c, d, cup=None, flag=False)`
del módulo `envios.py`, que calcula el costo de un envío. Se cubren:

- Validación de entradas (peso, zona, día, cupón).
- Cálculo por tramos de peso.
- Recargos por zona y fin de semana.
- Descuentos por cliente y cupón, y su combinación.
- Mínimo y redondeo half-up.
- Refactorización (comportamiento equivalente) y la solicitud de cambio 1.

**Fuera de alcance:** interfaz gráfica, persistencia, autenticación, integración
con pasarela de pagos (no existen en el código heredado).

## 2. Niveles de prueba

| Nivel | Aplicación concreta | Responsable | Herramienta |
|-------|---------------------|-------------|-------------|
| **Unidad** | `calc` con cada regla R1–R8 de forma aislada: tramos, recargos, descuentos, validaciones, redondeo. | Desarrollador | pytest |
| **Integración** | Interacción entre reglas: recargo de zona + descuentos + fin de semana + mínimo + redondeo en una misma llamada. | Desarrollador | pytest (parametrizado) |
| **Sistema** | Ejecución completa del módulo `envios.py` tal como se importa en producción, verificando contratos de entrada/salida y excepciones. | Desarrollador/QA | pytest + cobertura |
| **Aceptación** | Historias HU-01, HU-02, HU-03 verificadas con los casos de la Parte 3 y los resultados calculados a mano. | Docente/Cliente | revisión + suite |

## 3. Estrategia

- **Caja negra primero:** particiones de equivalencia, valores límite y tabla de
  decisión derivadas de la especificación (no del código).
- **Caja blanca después:** grafo de flujo, complejidad ciclomática y caminos
  independientes para garantizar cobertura de sentencias y ramas.
- **Resultados esperados calculados a mano** con aritmética `Decimal`
  independiente (`docs/referencia_calculo.py`), nunca ejecutando el código
  heredado.
- **Automatización:** suite `pytest` parametrizada, IDs de caso estables,
  invocación posicional para sobrevivir a la eliminación de `flag`.
- **Regresión:** la misma suite debe fallar contra `v1.0.0` (defectos reales) y
  pasar 100 % en `v2.0.0` y `v2.1.0`.

## 4. Ambiente

| Elemento | Versión |
|----------|---------|
| Sistema operativo | Windows 11 |
| Python | 3.13.5 |
| pytest | 9.2.0 |
| pytest-cov / coverage | 7.1.0 / 7.17.2 |
| Git | 2.56.0 |
| Repositorio | https://github.com/FREY3R/parcial-ing-.git |

## 5. Roles

| Rol | Persona | Responsabilidad |
|-----|---------|-----------------|
| Desarrollador | Yerfreth Mejía Sierra | Diseño de casos, automatización, corrección |
| QA / revisor | Yerfreth Mejía Sierra (auto-revisión) | Verificación de resultados a mano |
| Aceptación | Docente del curso | Validación de historias y entrega |

## 6. Riesgos y mitigación

| ID | Riesgo | Prob. | Impacto | Mitigación |
|----|--------|-------|---------|------------|
| R-01 | Calcular el esperado ejecutando el código heredado (circularidad) | Media | Alto | Cálculo independiente con `Decimal` y paso a paso en el informe |
| R-02 | Error de redondeo por usar `float` | Alta | Alto | Referencia en `Decimal`, casos con $50 exactos |
| R-03 | Confundir paridad de reglas (D/E/B/F) | Media | Alto | Tabla de parámetros y verificación doble |
| R-04 | Tests acoplados a `flag` | Media | Medio | Llamadas posicionales sin `flag` |
| R-05 | Cobertura insuficiente de ramas | Media | Medio | `--cov-branch` y caminos independientes |
| R-06 | Pérdida de evidencia | Baja | Medio | Guardar salidas en `evidence/` y commitear |

## 7. Criterios de entrada

- Especificación R1–R8 aprobada y parámetros calculados (`docs/00_parametros.md`).
- Código heredado disponible y etiquetado `v1.0.0`.
- Suite de pruebas escrita y ejecutable.
- Entorno con Python, pytest y pytest-cov.

## 8. Criterios de salida

- **100 %** de los casos de la Parte 3 automatizados.
- Suite **en verde** sobre `v2.0.0` y `v2.1.0`.
- Cobertura de sentencias y ramas **≥ 95 %** en el código refactorizado.
- Todos los defectos reales documentados, corregidos y con prueba de regresión.
- Evidencias (`pytest`, cobertura, `git log`) guardadas en `evidence/`.
