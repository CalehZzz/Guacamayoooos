# Automation Studio — componentes en español (Guacamayos)

Proyecto: `Guacamayos_ElectroNeumatica`

Si Automation Studio está en **español**, busca estos nombres.  
Si está en **inglés**, usa el de la columna “En inglés”.

---

## Bibliotecas

| En español | En inglés |
|---|---|
| **Neumática** | Pneumatic |
| **Control eléctrico** (IEC) | Electrical Control |

Plantilla al crear: **Neumática / Símbolos / Unidades métricas**  
(o *Pneumatic / Symbols / Metric Units*).

---

## Neumática — lista exacta

Biblioteca: **Neumática**

| # | Nombre en español (búscale así) | En inglés | Cant. | Para qué |
|---|---|---|---|---|
| 1 | **Fuente de presión neumática** | Pneumatic Pressure Source | 1 | Aire comprimido |
| 2 | **Escape** | Exhaust | 2 | Salidas de escape de la válvula |
| 3 | **Cilindro de doble efecto** | Double-Acting Cylinder | 1 | Pistón que empuja las latas |
| 4 | **Válvula 5/2 NC** (o **Válvula de 5 vías / 2 posiciones NC**) | 5/2-Way NC Valve | 1 | Electroválvula del pistón |
| 5 | **Ref. de sensor** / **Referencia de sensor** | Sensor Ref. | 2 | Fin de carrera retractado y extendido |

### Dónde están en la librería
- Cilindro → **Actuadores** (*Actuators*)
- Válvula 5/2 → **Válvulas direccionales** → **5/2** (*Directional Valves → 5/2-Way*)
- Sensores → **Sensores** → **Referencias de sensor** (*Sensors → Sensor References*)

### Configurar la válvula 5/2
Doble clic → **Especificaciones técnicas** (*Technical Specifications*):
- Comando: **Solenoide CC/CA** (*Solenoid DC/AC*)
- Retorno: **Retorno por resorte / muelle** (*Spring Return*)

### Colocar los 2 sensores en el cilindro
1. Extensión del cilindro al **0%** → alinea el 1.er sensor → **retractado**
2. Extensión al **100%** → alinea el 2.º → **extendido**
3. Vuelve a **0%**

---

## Eléctrica — lista exacta

Biblioteca: **Control eléctrico**

| # | Nombre en español | En inglés | Alias (ponle este nombre) | Equivale en TIA |
|---|---|---|---|---|
| 1 | **Fuente de alimentación 24 V** | Power Supply 24 Volts | `+24V` | — |
| 2 | **Común (0 V)** | Common (0 Volts) | `0V` | — |
| 3 | **Pulsador NA** (normalmente abierto) | Normally Open Push-Button | `I_Start` | `I_Start` |
| 4 | **Pulsador NA** | Normally Open Push-Button | `I_Stop` | `I_Stop` |
| 5 | **Pulsador NA** | Normally Open Push-Button | `I_Emergencia` | `I_Emergencia` |
| 6 | **Pulsador NA** | Normally Open Push-Button | `I_SensorPieza` | `I_SensorPieza` |
| 7 | **Pulsador NA** | Normally Open Push-Button | `I_SensorPlastico` | `I_SensorPlastico` |
| 8 | **Pulsador NA** | Normally Open Push-Button | `I_SensorAluminio` | `I_SensorAluminio` |
| 9 | **Pulsador NA** | Normally Open Push-Button | `I_ManualBanda` | `I_ManualBanda` |
| 10 | **Pulsador NA** | Normally Open Push-Button | `I_ManualPiston` | `I_ManualPiston` |
| 11 | **Detector de proximidad NA** | Normally Open Proximity Switch | `I_PistonRetractado` | `I_PistonRetractado` |
| 12 | **Detector de proximidad NA** | Normally Open Proximity Switch | `I_PistonExtendido` | `I_PistonExtendido` |
| 13 | **Solenoide CC/CA** | Solenoid, DC/AC | `Q_Piston` | `Q_Piston` |
| 14 | **Bobina** (opcional, banda) | Coil | `Q_Banda` | `Q_Banda` |
| 15 | **Contacto NA** | Normally Open Contact | (de la bobina banda) | — |
| 16 | **Lámpara piloto** / **Piloto** | Pilot Light | `Q_LamparaRun` | `Q_LamparaRun` |
| 17 | **Lámpara piloto** | Pilot Light | `Q_LamparaAlarma` | `Q_LamparaAlarma` |
| 18 | **Lámpara piloto** | Pilot Light | `Q_LamparaEmergencia` | `Q_LamparaEmergencia` |

### Dónde están
- Fuente / común → **Fuentes de alimentación** (*Power Sources*)
- Pulsadores → **Interruptores** / **Pulsadores** (*Switches*)
- Proximidad → **Interruptores de sensor** (*Sensor Switches*)
- Solenoide / bobina → **Componentes de salida** (*Output Components*)

### Enlazar solenoide eléctrico con la válvula
1. Doble clic en la **Válvula 5/2 NC**
2. **Asignación de variables** (*Variable Assignment*)
3. Click en el solenoide de la válvula (`?(ls)`)
4. Elige el alias **`Q_Piston`**
5. Cuando enlace, deja de verse `?(ls)` y aparece `Q_Piston`

Haz lo mismo: cada **Ref. de sensor** ↔ su **Detector de proximidad**.

---

## BOM corto (copia y busca)

### Neumática
```
1 × Fuente de presión neumática
2 × Escape
1 × Cilindro de doble efecto
1 × Válvula 5/2 NC          (Solenoide + retorno por muelle)
2 × Ref. de sensor
```

### Eléctrica
```
1 × Fuente 24 V
1 × Común 0 V
8 × Pulsador NA
2 × Detector de proximidad NA
1 × Solenoide CC/CA     → alias Q_Piston
1 × Bobina              → alias Q_Banda (opcional)
2–3 × Lámpara piloto
```

---

## Cómo va el aire

```
Fuente de presión
      │
      ▼
Válvula 5/2 NC ── Escape (×2)
      │
      ▼
Cilindro de doble efecto
      ├─ Ref. sensor @ 0%   → retractado
      └─ Ref. sensor @ 100% → extendido
```

---

## Simulación

Menú **Simulación** → **Simulación normal** (*Simulation → Normal Simulation*).

1. Pulsas `I_Start`
2. Pieza + plástico → **no** actives `Q_Piston`
3. Pieza + aluminio → activa `Q_Piston` → cilindro sale → sensor 100%
4. Quítas `Q_Piston` → vuelve → sensor 0%
5. `I_Emergencia` → todo apagado

---

## Si no lo encuentras con ese nombre

Prueba el buscador de la librería con:
- `5/2`
- `cilindro` / `cylinder`
- `solenoide` / `solenoid`
- `proximidad` / `proximity`
- `pulsador` / `push`

Clic derecho → **Ayuda contextual** (F1) te dice el nombre oficial del componente.
