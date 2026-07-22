# Automation Studio — componentes con nombre exacto (Guacamayos)

Proyecto: `Guacamayos_ElectroNeumatica`  
Plantilla al crear: **Pneumatic / Symbols / Metric Units** (o Multitechnology si la tienes).

En AS los nombres salen en **inglés** (librería Famic). Usa exactamente estos.

---

## 1) Dónde están (bibliotecas)

| Librería | Para qué |
|---|---|
| **Pneumatic** | Aire, válvula, cilindro, sensores de posición |
| **Electrical Control** (IEC) | Pulsadores, bobinas, contactos, fuente 24 V |

Al arrastrar un componente eléctrico, AS te pide un **Alias** (nombre visible). Pon los de la columna Alias de abajo.

---

## 2) Lista mínima neumática (pistón clasificador)

Biblioteca: **Pneumatic**

| # | Nombre exacto en AS | Ruta típica en librería | Cant. | Rol en Guacamayos |
|---|---|---|---|---|
| 1 | **Pneumatic Pressure Source** | Pneumatic (raíz / Power) | 1 | Fuente de aire |
| 2 | **Exhaust** | Pneumatic (raíz) | 2 | Escapes de la válvula 5/2 |
| 3 | **Double-Acting Cylinder** | Pneumatic → **Actuators** | 1 | Pistón que empuja latas |
| 4 | **5/2-Way NC Valve** | Pneumatic → **Directional Valves** → **5/2-Way** | 1 | Electroválvula del pistón |
| 5 | **Sensor Ref.** | Pneumatic → **Sensors** → **Sensor References** | 2 | Posición retractado / extendido |

### Configurar la válvula 5/2 (importante)
1. Doble clic en **5/2-Way NC Valve**
2. **Technical Specifications**
3. Comandos: deja / pon **Solenoid DC/AC** (bobina eléctrica) + **Spring Return** (retorno por muelle)  
   → monoestable: 1 bobina = extender; al quitar energía vuelve (retrae el cilindro según el cableado)

> Si tu lista muestra **5/2-Way Valve** genérica: ábrela y configúrala igual (1 Solenoid + Spring Return).  
> Evita por ahora válvulas solo con Push-Button si quieres electroneumática real.

### Colocar los 2 Sensor Ref. en el cilindro
1. Arrastra **Sensor Ref.** cerca del **Double-Acting Cylinder**
2. Doble clic cilindro → Data → `Extension = 0%` → alinea 1er sensor al pistón → ese será **retractado**
3. Pon `Extension = 100%` → alinea 2º sensor → **extendido**
4. Vuelve `Extension = 0%`

---

## 3) Lista eléctrica (control del pistón + demo)

Biblioteca: **Electrical Control** (IEC Standard)

| # | Nombre exacto en AS | Ruta típica | Alias sugerido | Equivale en TIA |
|---|---|---|---|---|
| 1 | **Power Supply 24 Volts** | Power Sources | `+24V` | — |
| 2 | **Common (0 Volts)** | Power Sources | `0V` | — |
| 3 | **Normally Open Push-Button** | Switches | `I_Start` | `I_Start` |
| 4 | **Normally Open Push-Button** | Switches | `I_Stop` | (en AS lo usas como paro; o NC si prefieres) |
| 5 | **Normally Open Push-Button** | Switches | `I_Emergencia` | `I_Emergencia` |
| 6 | **Normally Open Push-Button** | Switches | `I_SensorPieza` | `I_SensorPieza` (simulado) |
| 7 | **Normally Open Push-Button** | Switches | `I_SensorPlastico` | `I_SensorPlastico` |
| 8 | **Normally Open Push-Button** | Switches | `I_SensorAluminio` | `I_SensorAluminio` |
| 9 | **Normally Open Push-Button** | Switches | `I_ManualBanda` | `I_ManualBanda` |
| 10 | **Normally Open Push-Button** | Switches | `I_ManualPiston` | `I_ManualPiston` |
| 11 | **Normally Open Proximity Switch** | Sensor Switches | `I_PistonRetractado` | `I_PistonRetractado` |
| 12 | **Normally Open Proximity Switch** | Sensor Switches | `I_PistonExtendido` | `I_PistonExtendido` |
| 13 | **Solenoid, DC/AC** | Output Components | `Q_Piston` | `Q_Piston` |
| 14 | **Coil** | Output Components → Coils | `C_Banda` | auxiliar banda (opcional) |
| 15 | **Normally Open Contact** | Contacts | (del coil `C_Banda`) | — |
| 16 | **Pilot Light** / Indicator (si está) | Output / Indicators | `Q_LamparaRun` | `Q_LamparaRun` |
| 17 | **Pilot Light** | Output / Indicators | `Q_LamparaAlarma` | `Q_LamparaAlarma` |
| 18 | **Pilot Light** | Output / Indicators | `Q_LamparaEmergencia` | `Q_LamparaEmergencia` |

### Enlazar bobina eléctrica ↔ válvula neumática
1. Doble clic en la **5/2-Way NC Valve**
2. Menú **Variable Assignment**
3. Click en el icono del **Solenoid** de la válvula (`?(ls)`)
4. Elige el Alias **`Q_Piston`** (el **Solenoid, DC/AC** eléctrico)
5. Cuando enlace bien, `?(ls)` cambia a `Q_Piston`

Igual con los **Normally Open Proximity Switch**: enlázalos a cada **Sensor Ref.** del cilindro (retractado / extendido).

---

## 4) Banda transportadora (simple, opcional pero útil en la demo)

No hace falta un conveyor 3D. Con esto basta:

| Nombre exacto | Alias | Nota |
|---|---|---|
| **Coil** | `Q_Banda` | “Motor banda” lógico |
| **Pilot Light** | `HL_Banda` | Se enciende cuando banda ON |
| o un **Normally Open Contact** de `Q_Banda` alimentando el piloto | | |

Si tu licencia tiene motor/actuador de cinta, úsalo; **no es obligatorio** para el PDF del reto. Lo obligatorio electroneumático es cilindro + válvula + sensores.

---

## 5) BOM resumen (copia esta lista al armar)

### Pneumatic library
```
1 × Pneumatic Pressure Source
2 × Exhaust
1 × Double-Acting Cylinder
1 × 5/2-Way NC Valve          (Solenoid + Spring Return)
2 × Sensor Ref.
```

### Electrical Control library
```
1 × Power Supply 24 Volts
1 × Common (0 Volts)
8 × Normally Open Push-Button   (Start, Stop, Emergencia, Pieza, Plastico, Aluminio, ManualBanda, ManualPiston)
2 × Normally Open Proximity Switch   (Retractado, Extendido)
1 × Solenoid, DC/AC             (alias Q_Piston)  ← enlazado a la 5/2
1 × Coil                        (alias Q_Banda)   ← opcional banda
2–3 × Pilot Light               (Run / Alarma / Emergencia)
```

---

## 6) Cómo se conecta el aire (esquema mental)

```
Pneumatic Pressure Source
        │
        ▼
  5/2-Way NC Valve  ── Exhaust
        │    │
        ▼    ▼
   Double-Acting Cylinder
        ▲
   Sensor Ref. @ 0%   → retractado
   Sensor Ref. @ 100% → extendido
```

Eléctrico: `+24V` → pulsadores/lógica → **Solenoid `Q_Piston`** → `0V`

---

## 7) Simulación (demo de 1 minuto)

1. Ribbon → **Simulation** → **Normal Simulation**
2. Click `I_Start` (mano sobre el pulsador)
3. Click `I_SensorPieza` + `I_SensorPlastico` → válvula **NO** debe energizarse (en demo manual tú no activas `Q_Piston`)
4. Suelta plástico; activa `I_SensorAluminio` y energiza/solenoide `Q_Piston` → cilindro **extiende** → proximity extendido
5. Quita `Q_Piston` → retorna → proximity retractado
6. `I_Emergencia` → todo off

---

## 8) Si no encuentras un nombre

| Buscas | Prueba también |
|---|---|
| 5/2-Way NC Valve | `5/2-Way` dentro de Directional Valves; luego configura Solenoid |
| Sensor Ref. | Sensors → Sensor References |
| Solenoid, DC/AC | Output Components → Solenoid |
| Normally Open Push-Button | Switches → Push-Button NO |
| Normally Open Proximity Switch | Sensor Switches → Proximity |

Clic derecho en cualquier componente → **Context Help** (F1) confirma el nombre oficial.
