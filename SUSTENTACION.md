# Guía de sustentación

Duración objetivo: 10–12 minutos. Enlaces y comandos listos para ejecutar.

## 1. Guion sugerido

| Min | Bloque | Idea fuerza |
|-----|--------|-------------|
| 0:00 | Presentación | Nombre, código 0182410093, repo y objetivo del parcial |
| 0:45 | Parámetros | Últimos 6 dígitos → A4 B1 C0 D0 E9 F3; PMAX=50, L1=3, L2=10, RR=15 %, RN=40 %, V=15 %, S=2000, CAMBIO=1 |
| 1:30 | Requisitos | R1–R8 y las cuatro paridades: D par (L1 incluido), E impar (finde después), B impar (ambos descuentos), F impar (cupón inválido = error) |
| 2:30 | Caja negra | Particiones, valores límite, tabla de decisión y 33 casos; los esperados se calcularon con Decimal, no ejecutando el heredado |
| 4:00 | Caja blanca | Grafo con N=30, E=43 y M=15 por las tres formas; 15 caminos; coincidencia con `radon` |
| 5:30 | Defectos | 7 defectos (5 alta, 1 media, 1 baja), densidad 17,1/100 líneas; 14/36 pruebas pasaban |
| 6:30 | TDD | Una rama por defecto: prueba en rojo, corrección en verde, merge `--no-ff` |
| 7:30 | Refactor | 13 malos olores; Strategy, constantes, `Decimal`, sin `flag`; complejidad 15 → 3 |
| 8:45 | Cambio | `CAMBIO=1`: empresarial 12 % y sin zona si peso > L2; 55 pruebas en verde |
| 9:45 | Demo | Comandos de la sección 2 |
| 11:00 | Cierre | Trazabilidad, versiones y aprendizajes |

## 2. Demo en vivo

```powershell
# 1. Estado del repositorio y versiones
git log --oneline --decorate -12
git tag

# 2. Suite completa (55 pruebas)
python -m pytest -q

# 3. Cobertura
python -m pytest -q --cov=envios --cov-branch --cov-report=term-missing

# 4. Complejidad
python -m radon cc envios.py -s -a

# 5. Casos representativos
python -c "from envios import calc; print(calc(5,'urbana','empresarial',3)); print(calc(11,'nacional','ninguno',3)); print(calc(10,'nacional','ninguno',3))"
```

Salidas esperadas:

- `55 passed`
- `envios.py 100 %` en sentencias y ramas
- Complejidad promedio `A (1,76)`, máximo `3`
- `7900`, `9800`, `12600`

## 3. Preguntas frecuentes

**¿Por qué M=15 y no 14?**
`radon` y McCabe cuentan el `or` de `p <= 0 or p > 50` como dos predicados
(`P1a` y `P1b`). Al descomponerlo, N=30, E=43 y M=43−30+2=15; las tres formas
coinciden y también con `radon`.

**¿Por qué usar `Decimal`?**
Evita errores de coma flotante en dinero y permite redondear *half-up* de forma
exacta. Los esperados se calcularon con `Decimal` en
`docs/referencia_calculo.py`, sin ejecutar el heredado.

**¿Por qué el patrón Strategy?**
Agregar zonas o descuentos no obliga a editar `calc`; se registra una nueva
estrategia. Reduce la complejidad de 15 a 3 y respeta el principio abierto/cerrado.

**¿Por qué eliminar `flag`?**
Era un argumento bandera: la función calculaba e imprimía. Ahora `calc` es pura;
la impresión es del llamador. Es un cambio incompatible documentado en v2.0.0.

**¿Cómo se calcularon los defectos?**
Cada defecto se reprodujo con un caso de la matriz, se documentó con requisito,
severidad, prioridad y prueba, y se corrigió en su propia rama con TDD.

**¿Qué significa CAMBIO=1?**
Activa dos reglas: cliente empresarial con 12 % de descuento y sin recargo de
zona cuando el peso supera L2. El límite exacto `L2` conserva el recargo.

**¿Por qué la cobertura es 100 %?**
Porque las ramas de validación, zonas, descuentos, finde, mínimo y redondeo
tienen al menos un caso. La cobertura es un medio, no el objetivo: también se
revisó que los esperados fueran correctos.

**¿Qué mejoraría?**
Validar el nombre del cliente (hoy un valor desconocido se trata como
`"ninguno"`), leer `CAMBIO` de configuración externa y agregar pruebas de
propiedad o mutación.

## 4. Checklist de entrega

- [x] Repositorio público con historial y ramas.
- [x] Tags `v1.0.0`, `v2.0.0`, `v2.1.0`.
- [x] Documentos 00–08 y notas de versión.
- [x] Suite de 55 pruebas y cobertura 100 %.
- [x] Evidencias en `evidence/` (txt y PNG).
- [x] Grafo de flujo y UML en PNG.
- [x] `CHANGELOG.md`, `README.md` e informe PDF.
