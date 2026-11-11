# Parcial 3 · Ingeniería de Software I

**Estudiante:** Yerfreth Mejía Sierra
**Código:** 0182410093
**Programa:** Ingeniería de Sistemas — Universidad de La Guajira
**Grupo:** B1
**Repositorio:** https://github.com/FREY3R/parcial-ing-.git

Cálculo del costo de envío de una empresa de mensajería, con especificación
propia (R1–R8), análisis de caja negra y caja blanca, suite de pruebas,
corrección de defectos, refactorización y gestión del cambio.

## Especificación (código 0182410093)

Últimos seis dígitos: `4 1 0 0 9 3` → `A=4, B=1, C=0, D=0, E=9, F=3`.

| Parámetro | Valor | Regla |
|-----------|-------|-------|
| `PMAX` | 50 kg | Peso máximo |
| `L1` | 3 kg | Tramo 1 (incluido por D par) |
| `L2` | 10 kg | Tramo 2 |
| `RR` | 15 % | Recargo rural |
| `RN` | 40 % | Recargo nacional |
| `V` | 15 % | Descuento VIP |
| `S` | 2000 | Recargo fin de semana |
| `CAMBIO` | 1 | Cliente empresarial 12 % y sin zona si peso > L2 |

Reglas destacadas:

- **D par:** el tramo 1 incluye exactamente `L1` (`peso ≤ 3`).
- **E impar:** el recargo de fin de semana se aplica **después** de los descuentos.
- **B impar:** se aplican **ambos** descuentos (cliente y luego cupón).
- **F impar:** un cupón inexistente lanza `ValueError`/`ErrorEnvio`.
- Redondeo *half-up* al múltiplo de $100; mínimo $5.000.
- Orden: validar → costo base → zona → descuentos → finde → mínimo → redondeo.

## Versiones

| Tag | Contenido |
|-----|-----------|
| `v1.0.0` | Código heredado con 7 defectos (línea base) |
| `v2.0.0` | Correcciones DEF-01…DEF-07 + refactor con Strategy y `Decimal` |
| `v2.1.0` | `CAMBIO=1`: cliente empresarial y exención de zona para peso > L2 |

## Resultados

| Métrica | v1.0.0 | v2.0.0 | v2.1.0 |
|---------|--------|--------|--------|
| Pruebas | 36 (14 pasan) | 43 (43 pasan) | **55 (55 pasan)** |
| Cobertura | 96 % sentencias | 100 % sentencias y ramas | **100 %** |
| Complejidad máx. por bloque | 15 | 3 | 3 |
| Complejidad promedio | 15,0 | 1,76 | 1,81 |

## Estructura del repositorio

```
.
├── envios.py                  # Implementación v2.1.0
├── tests/
│   ├── test_envios.py         # Suite principal (caja negra + cambio)
│   └── test_def01..07_*.py    # Regresiones TDD por defecto
├── docs/
│   ├── 00_parametros.md       # Parámetros y cálculos base
│   ├── 01_requisitos.md       # R1–R8
│   ├── 01_historias.md        # Historias de usuario
│   ├── 01_matriz.md           # Matriz requisito–prueba
│   ├── 02_plan_pruebas.md     # Plan de pruebas
│   ├── 03_caja_negra.md       # Particiones, límites, decisión, 33 casos
│   ├── 04_caja_blanca.md      # Grafo, M=15, 15 caminos
│   ├── 05_defectos.md         # 7 defectos y métricas
│   ├── 06_refactorizacion.md  # Malos olores, UML, antes/después
│   ├── 07_configuracion.md    # Gestión de parámetros
│   ├── 08_cambio.md           # Análisis del CAMBIO=1
│   ├── notas_v2.0.0.md        # Notas de versión
│   ├── notas_v2.1.0.md        # Notas de versión
│   ├── referencia_calculo.py  # Calculadora Decimal independiente
│   ├── grafo_flujo.py         # Genera el grafo de flujo
│   ├── uml_clases.py          # Genera el UML de clases
│   └── render_evidencia.py    # Convierte salidas de pytest a PNG
├── evidence/
│   ├── v1.0.0_pytest.txt/.png # Evidencia roja del heredado
│   ├── v2.0.0_pytest.txt/.png # Evidencia verde del refactor
│   ├── v2.1.0_pytest.txt/.png # Evidencia verde del cambio
│   ├── grafo_flujo.png
│   └── uml_clases.png
├── CHANGELOG.md
├── SUSTENTACION.md
└── README.md
```

## Cómo ejecutar

Requisitos: Python 3.13+, `pytest`, `pytest-cov`, `matplotlib`, `Pillow`,
`reportlab`, `radon`.

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python -m pytest -q --cov=envios --cov-branch --cov-report=term-missing
python -m radon cc envios.py -s -a
```

Generar artefactos:

```powershell
python docs/grafo_flujo.py
python docs/uml_clases.py
python docs/render_evidencia.py evidence/v2.1.0_pytest.txt evidence/v2.1.0_pytest.png
```

## Uso de la API

```python
from envios import calc, ErrorEnvio

calc(5, "urbana", "ninguno", 3)                  # 9000
calc(5, "rural", "vip", 6, "ENVIO10")            # 8900
calc(11, "nacional", "empresarial", 3)           # 8600 (sin recargo de zona)
calc(5, "urbana", "empresarial", 3, "ENVIO10")   # 7100

try:
    calc(5, "express", "ninguno", 3)
except ErrorEnvio as error:
    print(error)  # zona inválida
```

## Estrategia de ramas

- `main`: historia integrada, cada versión etiquetada.
- `test/suite`: suite inicial (merge `--no-ff`).
- `fix/DEF-01` … `fix/DEF-07`: una rama por defecto, con prueba en rojo y
  corrección en verde.
- `refactor/estrategia`: refactor v2.0.0.
- `feature/cambio-1`: cambio v2.1.0.

Cada rama se integra con `--no-ff` para conservar la trazabilidad.

## Documentación de sustentación

Ver `SUSTENTACION.md` para el guion de la exposición y las preguntas frecuentes.
