# Programa LAD — versión SIMULACIÓN (solo reemplazo de tags)

Igual que antes, pero **todas las entradas `I_` pasan a `M_HMI_...`** para que la HMI pueda escribirlas.

Crea los tags Bool `M_HMI_*` del listado anterior.  
`M_SistemaOn`, `M_ModoAuto`, `M_Alarma`, `M_Clasificando`, `M_PulsePlastico`, `M_EdgePlastico`, `M_ResetAlarma`, `Q_*`, `DatosEstacion` = **igual**.

---

# OB1 (igual)
1. Call `FC_Modos`  
2. Call `FC_Secuencia`  
3. Call `FC_Alarmas`  
4. Call `FC_EspejoWeb`

---

# FC_Modos

## NW1 — Start
```
---| M_HMI_Start |-----|/ M_HMI_Stop |-----|/ M_HMI_Emergencia |-----(S M_SistemaOn)
```

## NW2 — Stop / Emergencia
```
---| M_HMI_Stop       |----+-----(R M_SistemaOn)
                           |
---| M_HMI_Emergencia |----+
```

## NW3 — Modo auto
*(Si el switch HMI ya escribe `M_ModoAuto`, esta red puedes omitirla.)*
```
---| M_ModoAuto |-----( M_ModoAuto )
```
→ mejor: **no pongas NW3**; deja solo el switch HMI → `M_ModoAuto`.

## NW4 — Lámpara RUN
```
---| M_SistemaOn |-----|/ M_HMI_Emergencia |-----( Q_LamparaRun )
```

## NW5 — Lámpara emergencia
```
---| M_HMI_Emergencia |-----( Q_LamparaEmergencia )
```

---

# FC_Secuencia

## NW1 — Banda (AUTO // MANUAL) → `Q_Banda`
```
  AUTO:
---| M_SistemaOn |---| M_ModoAuto |---|/ M_HMI_Emergencia |---|/ M_Alarma |---|/ M_Clasificando |--+
                                                                                                    |
  MANUAL:                                                                                           +----( Q_Banda )
---| M_SistemaOn |---|/ M_ModoAuto |---| M_HMI_ManualBanda |----------------------------------------+
```

## NW2 — Pulso plástico
```
---| M_SistemaOn |---| M_ModoAuto |---| M_HMI_SensorPieza |---| M_HMI_BasculaLista |
---| M_HMI_SensorPlastico |---|/ M_HMI_SensorAluminio |-----(P M_PulsePlastico)
                                                         (+ M_EdgePlastico en el otro ???)
```

## NW3 — Contar plástico (SCL)
```scl
IF M_PulsePlastico THEN
    DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
    DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 1;
END_IF;
```

## NW4 — Aluminio → Set clasificando
```
---| M_SistemaOn |---| M_ModoAuto |---| M_HMI_SensorPieza |---| M_HMI_BasculaLista |
---| M_HMI_SensorAluminio |---|/ M_HMI_SensorPlastico |-----(S M_Clasificando)
```

## NW5 — Pistón (AUTO // MANUAL) → `Q_Piston`
```
  AUTO:
---| M_Clasificando |---|/ M_HMI_PistonExtendido |--+
                                                    |
  MANUAL:                                           +----( Q_Piston )
---| M_SistemaOn |---|/ M_ModoAuto |---| M_HMI_ManualPiston |--+
```

## NW6 — TON retardo
```
---| M_Clasificando |---| M_HMI_PistonExtendido |----[ TON  T_RetardoPiston  PT:=T#500ms ]
```

## NW7 — Timer OK
**LAD:**
```
---| T_RetardoPiston.Q |-----(R M_Clasificando)
```
**SCL:**
```scl
IF T_RetardoPiston.Q THEN
    DatosEstacion.ContAluminio := DatosEstacion.ContAluminio + 1;
    DatosEstacion.PesoAluminioKg := DatosEstacion.PesoAluminioKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 2;
END_IF;
```

## NW8 — Timeout
**TON:**
```
---| M_Clasificando |----[ TON  T_TimeoutPiston  PT:=T#3s ]
```
**Alarma:**
```
---| T_TimeoutPiston.Q |---|/ M_HMI_PistonExtendido |-----(S M_Alarma)
```

## NW9 — Sensores contradictorios
```
---| M_HMI_SensorPieza |---| M_HMI_SensorPlastico |---| M_HMI_SensorAluminio |-----(S M_Alarma)
```

---

# FC_Alarmas

## NW1
```
---| M_Alarma |-----( Q_LamparaAlarma )
```

## NW2
```
---| M_ResetAlarma |-----(R M_Alarma)
```

## NW3
```
---| M_HMI_Emergencia |-----(S M_Alarma)
```

---

# FC_EspejoWeb (SCL)

```scl
DatosEstacion.SistemaOn  := M_SistemaOn;
DatosEstacion.ModoAuto   := M_ModoAuto;
DatosEstacion.Emergencia := M_HMI_Emergencia;
DatosEstacion.Alarma     := M_Alarma;
DatosEstacion.BandaOn    := Q_Banda;
DatosEstacion.PistonOn   := Q_Piston;
DatosEstacion.FinSesion  := M_HMI_FinSesion;

IF M_HMI_Emergencia THEN
    DatosEstacion.EstadoMaquina := 4;
ELSIF M_Alarma THEN
    DatosEstacion.EstadoMaquina := 3;
ELSIF M_Clasificando THEN
    DatosEstacion.EstadoMaquina := 2;
ELSIF M_SistemaOn THEN
    DatosEstacion.EstadoMaquina := 1;
ELSE
    DatosEstacion.EstadoMaquina := 0;
END_IF;
```

---

# Tabla de reemplazo (resumen)

| Quitas | Pones |
|---|---|
| `I_Start` | `M_HMI_Start` |
| `I_Stop` | `M_HMI_Stop` |
| `I_Emergencia` | `M_HMI_Emergencia` |
| `I_FinSesion` | `M_HMI_FinSesion` |
| `I_ManualBanda` | `M_HMI_ManualBanda` |
| `I_ManualPiston` | `M_HMI_ManualPiston` |
| `I_BasculaLista` | `M_HMI_BasculaLista` |
| `I_SensorPieza` | `M_HMI_SensorPieza` |
| `I_SensorPlastico` | `M_HMI_SensorPlastico` |
| `I_SensorAluminio` | `M_HMI_SensorAluminio` |
| `I_PistonRetractado` | `M_HMI_PistonRetractado` |
| `I_PistonExtendido` | `M_HMI_PistonExtendido` |
| `I_ModoAuto` | (nada: HMI escribe `M_ModoAuto`) |
