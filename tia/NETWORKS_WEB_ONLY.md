# Networks — solo Web (sin Automation Studio)

**Regla:** todo sensor/comando operador viene de `DB_HMI.*`.  
`M_Banda` / `M_Piston` / latches siguen siendo internos del PLC.

Ver también: `docs/11_SIN_AS_SOLO_WEB.md`.

---

## OB1
| NW | Call |
|---|---|
| 1 | `FC_Modos` |
| 2 | `FC_Secuencia` |
| 3 | `FC_Alarmas` |
| 4 | `FC_EspejoWeb` |

---

## FC_Modos (igual que antes)

### NW1 START
```
---| DB_HMI.Start |---|/ DB_HMI.Stop |---|/ DB_HMI.Emergencia |----(S M_SistemaOn)
```

### NW2 STOP / EMERGENCIA
```
---| DB_HMI.Stop       |----+----(R M_SistemaOn)
---| DB_HMI.Emergencia |----+
```

### NW3 Modo
```
---| DB_HMI.ModoAuto |----( M_ModoAuto )
```

### NW4 / NW5 Lámparas (opcionales)
```
---| M_SistemaOn |---|/ DB_HMI.Emergencia |----( M_LamparaRun )
---| DB_HMI.Emergencia |----( M_LamparaEmergencia )
```

---

## FC_Secuencia — sensores = DB_HMI

### NW1 Banda
```
  AUTO:
---| M_SistemaOn |---| M_ModoAuto |---|/ DB_HMI.Emergencia |---|/ M_Alarma |---|/ M_Clasificando |--+
                                                                                                        |
  MANUAL:                                                                                               +----( M_Banda )
---| M_SistemaOn |---|/ M_ModoAuto |---| DB_HMI.ManualBanda |------------------------------------------+
```

### NW2 Pulso plástico
```
---| M_SistemaOn |---| M_ModoAuto |---| DB_HMI.SensorPieza |---| DB_HMI.BasculaLista |
---| DB_HMI.SensorPlastico |---|/ DB_HMI.SensorAluminio |----(P M_PulsePlastico)
```
Memoria flanco: `M_EdgePlastico`

### NW3 Contar plástico (SCL)
```scl
IF M_PulsePlastico THEN
    DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
    DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 1;
END_IF;
```

### NW4 Aluminio → clasificar
```
---| M_SistemaOn |---| M_ModoAuto |---| DB_HMI.SensorPieza |---| DB_HMI.BasculaLista |
---| DB_HMI.SensorAluminio |---|/ DB_HMI.SensorPlastico |----(S M_Clasificando)
```

### NW5 Pistón
```
  AUTO:
---| M_Clasificando |---|/ DB_HMI.PistonExtendido |--+
                                                      |
  MANUAL:                                             +----( M_Piston )
---| M_SistemaOn |---|/ M_ModoAuto |---| DB_HMI.ManualPiston |--+
```

### NW6 TON retardo
```
---| M_Clasificando |---| DB_HMI.PistonExtendido |----[ TON T_RetardoPiston  PT:=T#500ms ]
```

### NW7 Fin + contar aluminio
**LAD:** `---| T_RetardoPiston.Q |----(R M_Clasificando)`

**SCL:**
```scl
IF T_RetardoPiston.Q THEN
    DatosEstacion.ContAluminio := DatosEstacion.ContAluminio + 1;
    DatosEstacion.PesoAluminioKg := DatosEstacion.PesoAluminioKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 2;
END_IF;
```

### NW8 Timeout
```
---| M_Clasificando |----[ TON T_TimeoutPiston  PT:=T#3s ]
---| T_TimeoutPiston.Q |---|/ DB_HMI.PistonExtendido |----(S M_Alarma)
```

### NW9 Contradicción
```
---| DB_HMI.SensorPieza |---| DB_HMI.SensorPlastico |---| DB_HMI.SensorAluminio |----(S M_Alarma)
```

---

## FC_Alarmas (igual)

```
---| M_Alarma |----( M_LamparaAlarma )
---| DB_HMI.ResetAlarma |----(R M_Alarma)
---| DB_HMI.Emergencia |----(S M_Alarma)
```

---

## FC_EspejoWeb (SCL, igual)

Copia `M_Banda`/`M_Piston`/`DB_HMI.PesoActualKg`/estado → `DatosEstacion`.
