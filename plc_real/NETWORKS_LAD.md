# Networks LAD — PLC real 1214C (3 pistones · control web)

**Regla:**
- Sensores / finales de carrera → `I_*` (únicos cables de entrada)
- Actuadores → `Q_*` (`Q_Piston1` retenedor · `Q_Piston2` plástico · `Q_Piston3` aluminio)
- **Operador → solo `DB_HMI.*`** (sin pulsadores físicos en la mesa)
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

### NW1 — START (solo web)
```
---| DB_HMI.Start |----|/ DB_HMI.Stop |----|/ DB_HMI.Emergencia |----(S M_SistemaOn)
```

### NW2 — STOP / EMERGENCIA (solo web)
```
---| DB_HMI.Stop       |----+----(R M_SistemaOn)
---| DB_HMI.Emergencia |----+
```

### NW3 — Modo auto (solo web)
```
---| DB_HMI.ModoAuto |----( M_ModoAuto )
```

### NW4 — Flag “clasificando” (para banda / estado)
```
---| M_ClasifPlastico |----+----( M_Clasificando )
---| M_ClasifAluminio |----+
```

### NW5 — Lámpara RUN
```
---| M_SistemaOn |---|/ DB_HMI.Emergencia |----( Q_LamparaRun )
```

### NW6 — Lámpara emergencia
```
---| DB_HMI.Emergencia |----( Q_LamparaEmergencia )
```

---

## FC_Secuencia

### NW1 — Banda → `Q_Banda`
```
  AUTO:
---| M_SistemaOn |---| M_ModoAuto |---|/ DB_HMI.Emergencia |
---|/ M_Alarma |---|/ M_Clasificando |--+
                                        |
  MANUAL (web):                         +----( Q_Banda )
---| M_SistemaOn |---|/ M_ModoAuto |---| DB_HMI.ManualBanda |--+
```

### NW2 — P1 retenedor → `Q_Piston1`
Sujeta la pieza con sistema ON y pieza presente (o mientras clasifica). Una sola bobina:
```
  AUTO:
---| M_SistemaOn |---| M_ModoAuto |---|/ DB_HMI.Emergencia |
---|/ M_Alarma |---+----| I_SensorPieza |----+
                   |----| M_Clasificando |----+----( Q_Piston1 )
  MANUAL (web):
---| M_SistemaOn |---|/ M_ModoAuto |---| DB_HMI.ManualPiston1 |--+
```

### NW3 — Aluminio → latch clasificar P3
```
---| M_SistemaOn |---| M_ModoAuto |---| I_SensorPieza |---| I_BasculaLista |
---| I_SensorAluminio |---|/ I_SensorPlastico |---|/ M_ClasifPlastico |----(S M_ClasifAluminio)
```

### NW4 — Plástico → latch clasificar P2
```
---| M_SistemaOn |---| M_ModoAuto |---| I_SensorPieza |---| I_BasculaLista |
---| I_SensorPlastico |---|/ I_SensorAluminio |---|/ M_ClasifAluminio |----(S M_ClasifPlastico)
```

### NW5 — P3 aluminio → `Q_Piston3`
```
  AUTO:
---| M_ClasifAluminio |---|/ I_Piston3Extendido |--+
                                                    |
  MANUAL (web):                                     +----( Q_Piston3 )
---| M_SistemaOn |---|/ M_ModoAuto |---| DB_HMI.ManualPiston |--+
```
(`ManualPiston` @ 0.7 = manual del pistón de aluminio.)

### NW6 — P2 plástico → `Q_Piston2`
```
  AUTO:
---| M_ClasifPlastico |---|/ I_Piston2Extendido |--+
                                                    |
  MANUAL (web):                                     +----( Q_Piston2 )
---| M_SistemaOn |---|/ M_ModoAuto |---| DB_HMI.ManualPiston2 |--+
```

### NW7 — TON retardo P3 (aluminio)
```
---| M_ClasifAluminio |---| I_Piston3Extendido |----[ TON T_RetardoPiston3  PT:=T#500ms ]
```

### NW8 — Fin clasificación aluminio + contar
**LAD:** `---| T_RetardoPiston3.Q |----(R M_ClasifAluminio)`

**SCL:**
```scl
IF T_RetardoPiston3.Q THEN
    DatosEstacion.ContAluminio := DatosEstacion.ContAluminio + 1;
    DatosEstacion.PesoAluminioKg := DatosEstacion.PesoAluminioKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 2;
END_IF;
```

### NW9 — TON retardo P2 (plástico)
```
---| M_ClasifPlastico |---| I_Piston2Extendido |----[ TON T_RetardoPiston2  PT:=T#500ms ]
```

### NW10 — Fin clasificación plástico + contar
**LAD:** `---| T_RetardoPiston2.Q |----(R M_ClasifPlastico)`

**SCL:**
```scl
IF T_RetardoPiston2.Q THEN
    DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
    DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 1;
END_IF;
```

### NW11 — Timeout P3
```
---| M_ClasifAluminio |----[ TON T_TimeoutPiston3  PT:=T#3s ]
---| T_TimeoutPiston3.Q |---|/ I_Piston3Extendido |----(S M_Alarma)
```

### NW12 — Timeout P2
```
---| M_ClasifPlastico |----[ TON T_TimeoutPiston2  PT:=T#3s ]
---| T_TimeoutPiston2.Q |---|/ I_Piston2Extendido |----(S M_Alarma)
```

### NW13 — Sensores contradictorios
```
---| I_SensorPieza |---| I_SensorPlastico |---| I_SensorAluminio |----(S M_Alarma)
```

---

## FC_Alarmas

### NW1
```
---| M_Alarma |----( Q_LamparaAlarma )
```

### NW2 — Reset (solo web)
```
---| DB_HMI.ResetAlarma |----(R M_Alarma)
```

### NW3 — Emergencia (solo web)
```
---| DB_HMI.Emergencia |----(S M_Alarma)
```

---

## FC_EspejoWeb (SCL)

```scl
DatosEstacion.SistemaOn    := M_SistemaOn;
DatosEstacion.ModoAuto     := M_ModoAuto;
DatosEstacion.Emergencia   := DB_HMI.Emergencia;
DatosEstacion.Alarma       := M_Alarma;
DatosEstacion.BandaOn      := Q_Banda;
// Compat web: “algún pistón activo”
DatosEstacion.PistonOn     := Q_Piston1 OR Q_Piston2 OR Q_Piston3;
// Detalle 3 pistones (byte 17 — ver DB_CONTRATO_WEB.md)
DatosEstacion.Piston1On    := Q_Piston1; // retenedor
DatosEstacion.Piston2On    := Q_Piston2; // plástico
DatosEstacion.Piston3On    := Q_Piston3; // aluminio
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
