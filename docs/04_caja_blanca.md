# 04 · Caja blanca

Análisis estructural de la función heredada `calc` (v1.0.0).

## 1. Grafo de flujo

Cada nodo representa una sentencia o un predicado. Los predicados son `P1…P13`.

```mermaid
flowchart TD
    S[1 S: def calc] --> P1{2 P1: p<=0 or p>50}
    P1 -- inválido --> R[3 R: raise ValueError]
    R --> X[29 End]
    P1 -- válido --> P2{4 P2: p<=L1}
    P2 -- sí --> T1[5 t=6000]
    P2 -- no --> P3{6 P3: p<=L2}
    P3 -- sí --> T2[7 t=9000]
    P3 -- no --> T3[8 t=9000+(p-L2)*800]
    T1 --> P4
    T2 --> P4
    T3 --> P4
    P4{9 P4: z==urbana} -- sí --> Z1[10 t=t]
    P4 -- no --> P5{11 P5: z==rural}
    P5 -- sí --> Z2[12 t+=t*RR]
    P5 -- no --> P6{13 P6: z==nacional}
    P6 -- sí --> Z3[14 t+=t*RN]
    Z1 --> P7
    Z2 --> P7
    Z3 --> P7
    P6 -- no --> P7
    P7{15 P7: d>6} -- sí --> W1[16 t+=S]
    P7 -- no --> P8
    W1 --> P8
    P8{17 P8: c==frecuente} -- sí --> F1[18 t-=t*0.05]
    P8 -- no --> P9{19 P9: c==vip}
    F1 --> P10
    P9 -- sí --> F2[20 t-=t*V]
    P9 -- no --> P10
    F2 --> P10
    P10{21 P10: cup!=None} -- sí --> P11{22 P11: cup==ENVIO10}
    P10 -- no --> P12
    P11 -- sí --> K1[23 t-=t*0.10]
    P11 -- no --> P12
    K1 --> P12
    P12{24 P12: t<5000} -- sí --> M1[25 t=5000]
    P12 -- no --> P13
    M1 --> P13
    P13{26 P13: flag} -- sí --> I1[27 print]
    P13 -- no --> RET[28 return]
    I1 --> RET
    RET --> X
```

> La imagen PNG se genera con `docs/grafo_flujo.py` en
> `evidence/grafo_flujo.png`.

## 2. Conteo de nodos y aristas

| Elemento | Cantidad |
|----------|----------|
| Nodos (N) | 29 |
| Aristas (E) | 41 |
| Predicados | 13 (P1–P13) |
| Regiones | 14 (incluye la exterior) |

Detalle de nodos: `S, P1, R, P2, T1, P3, T2, T3, P4, Z1, P5, Z2, P6, Z3, P7,
W1, P8, F1, P9, F2, P10, P11, K1, P12, M1, P13, I1, RET, End` = 29.

## 3. Complejidad ciclomática (tres formas)

| Forma | Cálculo | Resultado |
|-------|---------|-----------|
| Aristas − nodos + 2 | 41 − 29 + 2 | **14** |
| Nodos predicado + 1 | 13 + 1 | **14** |
| Regiones | regiones del grafo plano | **14** |

**Las tres coinciden en M = 14.**

> Nota: `P1` contiene `or`, pero se modela como **un** nodo predicado (un solo
> `if`). Si se descompusiera el cortocircuito en dos predicados, el grafo tendría
> un nodo y una arista más, y las tres formas subirían a 15 de manera consistente.

## 4. Caminos independientes (14) y caso de prueba por camino

| # | Camino (resumen de decisiones) | Caso | Entradas | Esperado |
|---|--------------------------------|------|----------|----------|
| CP01 | P1 V · P2 T · P4 T · P7 F · P8 F · P9 F · P10 F · P12 F · P13 F | C01 | 2, urbana, ninguno, 3, — | $6.000 |
| CP02 | P1 I → R | C21 | 0, urbana, ninguno, 3, — | `ValueError` |
| CP03 | P2 F · P3 T | C03 | 4, urbana, ninguno, 3, — | $9.000 |
| CP04 | P2 F · P3 F | C05 | 11, urbana, ninguno, 3, — | $9.800 |
| CP05 | P4 F · P5 T | C07 | 5, rural, ninguno, 3, — | $10.400 |
| CP06 | P5 F · P6 T | C08 | 5, nacional, ninguno, 3, — | $12.600 |
| CP07 | P6 F | C25* | 5, express, ninguno, 3, — | `ValueError` (spec) |
| CP08 | P7 T | C15 | 5, urbana, ninguno, 6, — | $11.000 |
| CP09 | P8 T | C10 | 5, urbana, frecuente, 3, — | $8.600 |
| CP10 | P9 T | C11 | 5, urbana, vip, 3, — | $7.700 |
| CP11 | P10 T · P11 T | C12 | 5, urbana, ninguno, 3, ENVIO10 | $8.100 |
| CP12 | P11 F | C19* | 5, urbana, ninguno, 3, OTRO | `ValueError` (spec) |
| CP13 | P12 T | C30 | 2, urbana, vip, 3, ENVIO10 | $5.000 |
| CP14 | P13 T | sonda† | 2, urbana, ninguno, 3, —, flag=True | imprime y retorna $6.000 |

\* En el heredado, `C25` y `C19` **no** lanzan error (defectos DEF-01 y DEF-05);
esos caminos existen precisamente porque falta la validación. Tras el refactor,
esos caminos desaparecen del código y los casos pasan a verificar el error en la
validación de entrada.

† `CP14` solo es alcanzable con `flag=True`; se usa una sonda exclusiva del
heredado, porque la suite principal invoca posicionalmente sin `flag` para poder
sobrevivir a su eliminación en v2.0.0.

## 5. Cobertura de sentencias vs. ramas

- **Cobertura de sentencias:** los caminos CP01–CP13 ejecutan todas las
  sentencias (tramos, tres zonas, recargo finde, tres descuentos, mínimo, raise y
  return). CP14 cubre además el `print` del `flag`.
- **Cobertura de ramas:** CP01–CP14 cubren las dos salidas de cada uno de los 13
  predicados (P1–P13), es decir, el 100 % de las ramas del heredado.
- La diferencia es que la cobertura de sentencias puede lograrse sin pasar por
  `P13=True`; la de ramas exige CP14.

## 6. Relación con los defectos

Varios caminos del grafo son **inalcanzables según la especificación** y solo
existen por defectos del heredado:

| Defecto | Camino/estructura implicada |
|---------|------------------------------|
| DEF-01 zona inválida | `P6 -- no --> P7` (CP07) no debería existir |
| DEF-02 día inválido | `P7` con `d=8` entra por `d>6` |
| DEF-03 sábado | `P7` usa `d>6` y excluye el día 6 |
| DEF-04 orden finde | posición de `W1` respecto a descuentos |
| DEF-05 cupón inválido | `P11 -- no --> P12` (CP12) no debería existir |
| DEF-06 redondeo | nodo `RET` con `int()` |
| DEF-07 float | nodo `T3` con aritmética flotante |
