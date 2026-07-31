# Networks LAD — PLC real 1214C

**Regla:**
- Sensores / finales de carrera → `I_*`
- Actuadores → `Q_*`
- Operador web → `DB_HMI.*` (OR con pulsadores físicos si existen)
- Espejo web → `DatosEstacion`

Los croquis no se pegan: dibuja contactos/bobinas en TIA.

---

## OB1
| NW | Call |
|---|---|
| 1 | `FC_Modos` |
| 2 | `FC_Secuencia` |
| 3 | `FC_Alarmas` |
| 4 | `FC_EspejoWeb` |

---

## FC_Modos

### NW1 — START (web O físico)
```
---| DB_HMI.Start |----+----|/ DB_HMI.Stop |----|/ I_Stop |----|/ DB_HMI.Emergencia |----|/ I_Emergencia |----(S M_SistemaOn)
---| I_Start      |----+
```
Si no cableas `I_Start`/`I_Stop`, omite esos contactos y deja solo `DB_HMI`.

### NW2 — STOP / EMERGENCIA
```
---| DB_HMI.Stop       |----+----(R M_SistemaOn)
---| I_Stop            |----+
---| DB_HMI.Emergencia |----+
---| I_Emergencia      |----+
```

### NW3 — Modo auto (web O selector)
```
---| DB_HMI.ModoAuto |----+----( M_ModoAuto )
---| I_ModoAuto      |----+
```
*(Si ambos pueden estar a 1, OR está bien. Si prefieres solo web: solo `DB_HMI.ModoAuto`.)*

### NW4 — Lámpara RUN
```
---| M_SistemaOn |---|/ DB_HMI.Emergencia |---|/ I_Emergencia |----( Q_LamparaRun )
```

### NW5 — Lámpara emergencia
```
---| DB_HMI.Emergencia |----+----( Q_LamparaEmergencia )
---| I_Emergencia      |----+
```

---

## FC_Secuencia

### NW1 — Banda → `Q_Banda`
```
  AUTO:
---| M_SistemaOn |---| M_ModoAuto |---|/ DB_HMI.Emergencia |---|/ I_Emergencia |
---|/ M_Alarma |---|/ M_Clasificando |--+
                                        |
  MANUAL:                               +----( Q_Banda )
---| M_SistemaOn |---|/ M_ModoAuto |---+----(
---| DB_HMI.ManualBanda |--------------+
---| I_ManualBanda      |--------------+
```

### NW2 — Pulso plástico
```
---| M_SistemaOn |---| M_ModoAuto |---| I_SensorPieza |---| I_BasculaLista |
---| I_SensorPlastico |---|/ I_SensorAluminio |----(P M_PulsePlastico)
```
Memoria flanco: `M_EdgePlastico`

### NW3 — Contar plástico (SCL)
```scl
IF M_PulsePlastico THEN
    DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
    DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 1;
END_IF;
```

### NW4 — Aluminio → clasificar
```
---| M_SistemaOn |---| M_ModoAuto |---| I_SensorPieza |---| I_BasculaLista |
---| I_SensorAluminio |---|/ I_SensorPlastico |----(S M_Clasificando)
```

### NW5 — Pistón → `Q_Piston`
```
  AUTO:
---| M_Clasificando |---|/ I_PistonExtendido |--+
                                                |
  MANUAL:                                       +----( Q_Piston )
---| M_SistemaOn |---|/ M_ModoAuto |---+----(
---| DB_HMI.ManualPiston |-------------+
---| I_ManualPiston      |-------------+
```

### NW6 — TON retardo
```
---| M_Clasificando |---| I_PistonExtendido |----[ TON T_RetardoPiston  PT:=T#500ms ]
```

### NW7 — Fin clasificación + contar aluminio
**LAD:** `---| T_RetardoPiston.Q |----(R M_Clasificando)`

**SCL:**
```scl
IF T_RetardoPiston.Q THEN
    DatosEstacion.ContAluminio := DatosEstacion.ContAluminio + 1;
    DatosEstacion.PesoAluminioKg := DatosEstacion.PesoAluminioKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 2;
END_IF;
```

### NW8 — Timeout pistón
```
---| M_Clasificando |----[ TON T_TimeoutPiston  PT:=T#3s ]
---| T_TimeoutPiston.Q |---|/ I_PistonExtendido |----(S M_Alarma)
```

### NW9 — Sensores contradictorios
```
---| I_SensorPieza |---| I_SensorPlastico |---| I_SensorAluminio |----(S M_Alarma)
```

---

## FC_Alarmas

### NW1
```
---| M_Alarma |----( Q_LamparaAlarma )
```

### NW2
```
---| DB_HMI.ResetAlarma |----+----(R M_Alarma)
---| I_ResetAlarma      |----+
```

### NW3
```
---| DB_HMI.Emergencia |----+----(S M_Alarma)
---| I_Emergencia      |----+
```

---

## FC_EspejoWeb (SCL)

```scl
DatosEstacion.SistemaOn    := M_SistemaOn;
DatosEstacion.ModoAuto     := M_ModoAuto;
DatosEstacion.Emergencia   := DB_HMI.Emergencia OR I_Emergencia;
DatosEstacion.Alarma       := M_Alarma;
DatosEstacion.BandaOn      := Q_Banda;
DatosEstacion.PistonOn     := Q_Piston;
DatosEstacion.FinSesion    := DB_HMI.FinSesion;
DatosEstacion.PesoActualKg := DB_HMI.PesoActualKg;

IF DatosEstacion.Emergencia THEN
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

> Si TIA no deja `OR` con tag `I_` en SCL, usa un Bool intermedio en LAD (`M_EmergenciaActiva`) y asígnalo aquí.
