# 01 · Historias de usuario

Las tres historias cubren R1–R8 y sirven de base para la matriz de trazabilidad.

---

## HU-01 · Cotizar un envío válido con recargos y descuentos

**Como** cliente de la empresa de envíos
**quiero** conocer el costo de mi envío según peso, zona, tipo de cliente y día
**para** decidir si lo realizo y cuánto pagaré.

**Cubre:** R1, R2, R3, R4, R5, R6.

### Criterios de aceptación (Dado / Cuando / Entonces)

1. **Tramo 1**
   - *Dado* un peso de 2 kg, zona urbana, cliente ninguno, día 3,
   - *cuando* se calcula el envío,
   - *entonces* el costo es $6.000.

2. **Tramo 2 (límite L1 incluido, D par)**
   - *Dado* un peso de 3 kg (igual a L1),
   - *cuando* se calcula,
   - *entonces* se cobra el tramo 1 ($6.000), porque D es par e incluye el límite.

3. **Tramo 3 proporcional**
   - *Dado* un peso de 12,5 kg, zona urbana, sin descuentos, día 3,
   - *cuando* se calcula,
   - *entonces* el costo es `9000 + 2,5·800 = $11.000`.

4. **Recargo rural**
   - *Dado* peso 5 kg, zona rural, sin descuentos, día 3,
   - *cuando* se calcula,
   - *entonces* el costo es `9000 · 1,15 = $10.350 → $10.400` (half-up).

5. **Fin de semana (sábado) después de descuentos (E impar)**
   - *Dado* peso 5 kg, zona urbana, cliente vip, día 6,
   - *cuando* se calcula,
   - *entonces* primero se descuenta 15 % (`7650`) y luego se suman $2.000,
     resultando `$9.650 → $9.700`.

---

## HU-02 · Aplicar descuentos combinados y validar cupones

**Como** cliente frecuente o VIP con cupón
**quiero** que se apliquen correctamente mis descuentos y que un cupón inválido
sea rechazado
**para** tener certeza del beneficio recibido.

**Cubre:** R6, R7.

### Criterios de aceptación

1. **Ambos descuentos (B impar)**
   - *Dado* peso 5 kg, zona urbana, cliente vip, cupón `ENVIO10`, día 3,
   - *cuando* se calcula,
   - *entonces* se aplica 15 % y luego 10 %: `9000 · 0,85 · 0,90 = 6885 → $6.900`.

2. **Cupón ausente**
   - *Dado* un envío sin cupón (`None`),
   - *cuando* se calcula,
   - *entonces* no se aplica descuento por cupón y no hay error.

3. **Cupón inexistente (F impar)**
   - *Dado* un cupón `"OTRO"`,
   - *cuando* se calcula,
   - *entonces* se lanza `ValueError`.

4. **Solo cliente frecuente**
   - *Dado* peso 5 kg, zona urbana, cliente frecuente, sin cupón, día 3,
   - *cuando* se calcula,
   - *entonces* el costo es `9000 · 0,95 = $8.550 → $8.600`.

---

## HU-03 · Rechazar entradas inválidas y respetar mínimo/redondeo

**Como** operador del sistema
**quiero** que las entradas fuera de rango se rechacen y que el costo final
respete el mínimo y el redondeo
**para** evitar cobros incorrectos.

**Cubre:** R1, R2, R8.

### Criterios de aceptación

1. **Peso no positivo**
   - *Dado* peso 0 o negativo,
   - *cuando* se calcula,
   - *entonces* se lanza `ValueError("peso inválido")`.

2. **Peso sobre PMAX**
   - *Dado* peso 51,
   - *cuando* se calcula,
   - *entonces* se lanza `ValueError("peso inválido")`.

3. **Zona inválida**
   - *Dado* zona `"express"`,
   - *cuando* se calcula,
   - *entonces* se lanza `ValueError`.

4. **Día inválido**
   - *Dado* día 0 u 8,
   - *cuando* se calcula,
   - *entonces* se lanza `ValueError`.

5. **Mínimo $5.000**
   - *Dado* peso 2 kg, urbana, vip, cupón `ENVIO10`, día 3,
   - *cuando* se calcula,
   - *entonces* `6000 · 0,85 · 0,90 = 4590`, se aplica el mínimo y resulta $5.000.

6. **Redondeo half-up**
   - *Dado* un costo intermedio de $8.550,
   - *cuando* se redondea,
   - *entonces* sube a $8.600 (los $50 van hacia arriba).
