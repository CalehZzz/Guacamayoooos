# Cómo poner bobinas S, R y P en TIA Portal

**No escribas** `S M_SistemaOn` ni `P_M_PulsePlastico` como texto.  
`S`, `R` y `P` son el **dibujo de la bobina**, no parte del nombre.

El tag siempre se llama igual: `M_SistemaOn`, `M_PulsePlastico`, `M_Clasificando`…

---

## Dónde están (TIA Portal V20)

1. Abre tu FC en lenguaje **LAD** (escalera).
2. Mira la barra de instrucciones a la derecha (o arriba):  
   **Instructions → Basic instructions → Bit logic**
3. Ahí verás varias bobinas distintas:

| Icono / nombre en TIA | Qué es | Cuándo usarlo en Guacamayos |
|---|---|---|
| Coil / bobina normal `( )` | Enciende solo mientras la red es true | `Q_Banda`, `Q_Piston`, lámparas |
| **Set coil** `(S)` | Queda en 1 hasta un Reset | `M_SistemaOn`, `M_Clasificando`, `M_Alarma` |
| **Reset coil** `(R)` | Pone en 0 | apagar `M_SistemaOn`, `M_Clasificando`, `M_Alarma` |
| **Positive edge coil** `(P)` / `--(P)--` | Pulso de 1 ciclo al pasar de 0→1 | `M_PulsePlastico` |
| Negative edge coil `(N)` | Pulso al pasar de 1→0 | no lo necesitamos |

Si no ves Set/Reset: en la misma carpeta **Bit logic** baja un poco; a veces están como:
- `Output set` / `Set`
- `Output reset` / `Reset`
- `Positive edge detection` (a veces es contacto P, a veces bobina P)

---

## Paso a paso (ejemplo Start → Set)

### Network Start (`M_SistemaOn`)
1. Inserta contactos abiertos/cerrados: `I_Start`, `I_Stop` (cerrado), `I_Emergencia` (cerrado).
2. A la **derecha** del riel, **no** pongas bobina normal.
3. Arrastra **Set coil** (S) al final de la red.
4. En el `???` de esa bobina escribe solo: `M_SistemaOn`

Queda visualmente algo así:
```
---| I_Start |---|/ I_Stop |---|/ I_Emergencia |----(S)
                                                 M_SistemaOn
```

### Network Stop (Reset)
1. Contactos: `I_Stop` y en paralelo `I_Emergencia`.
2. Al final: bobina **Reset (R)**.
3. Operand: `M_SistemaOn`

### Network pulso plástico (P)
1. Todos los contactos de la condición.
2. Al final: bobina **Positive edge (P)** (o “P coil”).
3. Operand: `M_PulsePlastico`

### Network aluminio (Set clasificando)
1. Contactos de aluminio…
2. Al final: bobina **Set (S)**.
3. Operand: `M_Clasificando`

### Cuando el TON cumple (Reset clasificando)
1. Contacto: `T_RetardoPiston.Q`
2. Bobina **Reset (R)** → `M_Clasificando`

---

## Si no te aparece la bobina P

En algunos TIA la detección de flanco es un **contacto P**, no bobina. Alternativa igual de válida:

```
---| ...condiciones... |---[P]----+----( S  M_PulsePlastico_latch )  ← complicado
```

Más simple sin bobina P:
1. Usa bobina **normal** `( M_PulsePlastico )` con las condiciones.  
2. En el SCL de contar plástico, el `IF M_PulsePlastico` contará **mientras** el sensor esté activo (puede sumar muchas veces).

Para evitar multicuentas sin bobina P, usa esto en SCL:

```scl
IF M_SistemaOn AND M_ModoAuto AND I_SensorPieza AND I_BasculaLista
   AND I_SensorPlastico AND NOT I_SensorAluminio THEN
    // solo si quieres flanco, declara un Bool M_PlasticoPrev en tags
    IF NOT M_PlasticoPrev THEN
        DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
        DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
        DatosEstacion.UltimoMaterial := 1;
    END_IF;
    M_PlasticoPrev := TRUE;
ELSE
    M_PlasticoPrev := FALSE;
END_IF;
```

Pero primero busca la bobina P; en V20 casi siempre está en Bit logic.

---

## Errores típicos

| Qué hiciste | Por qué falla |
|---|---|
| Escribiste `S_M_SistemaOn` o `S M_SistemaOn` | TIA busca un tag con ese nombre |
| Pusiste Set/Reset en un **contacto** de la izquierda | S/R/P van en la **bobina de la derecha** |
| Network solo con contactos | Falta la bobina → error “A coil/assignment is required” |
| Bobina normal donde iba Set | El bit no “queda latcheado” |

---

## Resumen de Guacamayos

| Network | Tipo de bobina | Tag |
|---|---|---|
| Start sistema | **Set (S)** | `M_SistemaOn` |
| Stop / emergencia | **Reset (R)** | `M_SistemaOn` |
| Pulso plástico | **P** | `M_PulsePlastico` |
| Inicio clasificar aluminio | **Set (S)** | `M_Clasificando` |
| Fin clasificar (TON.Q) | **Reset (R)** | `M_Clasificando` |
| Alarma | **Set (S)** | `M_Alarma` |
| Reset alarma | **Reset (R)** | `M_Alarma` |
| Banda / pistón / lámparas | **Normal** | `Q_Banda`, `Q_Piston`, etc. |
