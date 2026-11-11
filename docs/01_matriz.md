# 01 · Matriz de trazabilidad

Matriz viva: se completará con los IDs de casos de prueba de la Parte 3 y con las
pruebas automatizadas de la Parte 5.

| Requisito | Descripción breve | Historia | Casos de prueba (Parte 3) | Prueba automatizada |
|-----------|-------------------|----------|---------------------------|---------------------|
| R1 | Validación de peso 0 < p ≤ 50 | HU-01, HU-03 | C21, C22, C23, C24 | `test_peso_invalido`, `test_peso_limite_superior` |
| R2 | Validación de zona y día | HU-01, HU-03 | C25, C26, C27, C28 | `test_zona_invalida`, `test_dia_invalido` |
| R3 | Tramos de peso | HU-01 | C01–C06, C33 | `test_tramos` |
| R4 | Recargos por zona | HU-01 | C07, C08, C09 | `test_zonas` |
| R5 | Recargo fin de semana | HU-01 | C15, C16, C17, C18 | `test_fin_de_semana` |
| R6 | Descuentos cliente/cupón | HU-01, HU-02 | C10–C14 | `test_descuentos` |
| R7 | Cupón inexistente | HU-02 | C19, C20 | `test_cupon_inexistente` |
| R8 | Mínimo y redondeo half-up | HU-03 | C07, C10, C13, C30 | `test_minimo`, `test_redondeo_half_up` |

## Cobertura requisito → historia

| Historia | Requisitos cubiertos |
|----------|----------------------|
| HU-01 | R1, R2, R3, R4, R5, R6 |
| HU-02 | R6, R7 |
| HU-03 | R1, R2, R8 |

> Los IDs de casos se fijan definitivamente en `docs/03_caja_negra.md`.
