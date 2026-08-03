# Networks — solo Web (sin AS) · 3 pistones simple efecto

**Regla:** sensores + operador = `DB_HMI.*`.  
Actuadores internos = `M_Banda`, `M_Piston1` (retenedor), `M_Piston2` (plástico), `M_Piston3` (aluminio).

Igual que el PLC real (`plc_real/NETWORKS_LAD.md`), pero todo simulado vía HMI virtual.

Ver: `docs/11_SIN_AS_SOLO_WEB.md` · tags: `tia/TABLA_TAGS_DESDE_CERO.md` · DB: `tia/MAPA_DB_HMI.md`.

```
  [Sim entrada] → [Báscula DB_HMI] → [Banda] → [P1 retenedor + sensores]
                                                ├─ plástico  → P2
                                                └─ aluminio  → P3
```

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

### NW1 START → Set `M_SistemaOn`
```
[ DB_HMI.Start ]──[/ DB_HMI.Stop ]──[/ DB_HMI.Emergencia ]──(S) M_SistemaOn
```

### NW2 STOP / EMERGENCIA → Reset
```
[ DB_HMI.Stop       ]──┐
                       ├──(R) M_SistemaOn
[ DB_HMI.Emergencia ]──┘
```

### NW3 Modo
```
[ DB_HMI.ModoAuto ]──( ) M_ModoAuto
```

### NW4 / NW5 Lámparas (opcionales)
```
[ M_SistemaOn ]──[/ DB_HMI.Emergencia ]──( ) M_LamparaRun
[ DB_HMI.Emergencia ]──( ) M_LamparaEmergencia
```

---

## FC_Secuencia

### NW1 Banda → `M_Banda`
```
AUTO:
[ M_SistemaOn ]─[ M_ModoAuto ]─[/ Emerg ]─[/ Alarma ]─[/ M_Clasificando ]─┐
                                                                         ├──( ) M_Banda
MANUAL:                                                                  │
[ M_SistemaOn ]─[/ M_ModoAuto ]─[ DB_HMI.ManualBanda ]───────────────────┘
```

### NW2 P1 retenedor → `M_Piston1`
```
[ M_SistemaOn ]─[ M_ModoAuto ]─[/ Emerg ]─[/ Alarma ]─[ DB_HMI.SensorPieza ]─┐
[ M_SistemaOn ]─[ M_ModoAuto ]─[/ Emerg ]─[/ Alarma ]─[ M_Clasificando ]─────┼──( ) M_Piston1
[ M_SistemaOn ]─[/ M_ModoAuto ]─[ DB_HMI.ManualPiston1 ]────────────────────┘
```

### NW3 Latch aluminio → `(S) M_ClasifAluminio`
```
[ On ]─[ Auto ]─[ SensorPieza ]─[ BasculaLista ]─[ SensorAluminio ]
─[/ SensorPlastico ]─[/ M_ClasifPlastico ]─(S) M_ClasifAluminio
```
(todos los sensores = `DB_HMI.*`)

### NW4 Latch plástico → `(S) M_ClasifPlastico`
```
[ On ]─[ Auto ]─[ SensorPieza ]─[ BasculaLista ]─[ SensorPlastico ]
─[/ SensorAluminio ]─[/ M_ClasifAluminio ]─(S) M_ClasifPlastico
```

### NW5 P3 aluminio → `M_Piston3` (simple efecto)
```
[ M_ClasifAluminio ]─[/ DB_HMI.Piston3Extendido ]─┐
                                                   ├──( ) M_Piston3
[ M_SistemaOn ]─[/ ModoAuto ]─[ DB_HMI.ManualPiston ]─┘
```

### NW6 P2 plástico → `M_Piston2`
```
[ M_ClasifPlastico ]─[/ DB_HMI.Piston2Extendido ]─┐
                                                  ├──( ) M_Piston2
[ M_SistemaOn ]─[/ ModoAuto ]─[ DB_HMI.ManualPiston2 ]─┘
```

### NW7 Retardo + contar aluminio
```
[ M_ClasifAluminio ]─[ DB_HMI.Piston3Extendido ]─[ TON T_RetardoPiston3  PT:=T#500ms ]
[ T_RetardoPiston3.Q ]─(R) M_ClasifAluminio
```
SCL al disparo del TON:
```scl
IF T_RetardoPiston3.Q THEN
    DatosEstacion.ContAluminio := DatosEstacion.ContAluminio + 1;
    DatosEstacion.PesoAluminioKg := DatosEstacion.PesoAluminioKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 2;
END_IF;
```

### NW8 Retardo + contar plástico
```
[ M_ClasifPlastico ]─[ DB_HMI.Piston2Extendido ]─[ TON T_RetardoPiston2  PT:=T#500ms ]
[ T_RetardoPiston2.Q ]─(R) M_ClasifPlastico
```
```scl
IF T_RetardoPiston2.Q THEN
    DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
    DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 1;
END_IF;
```

### NW9 / NW10 Timeouts → alarma
```
[ M_ClasifAluminio ]─[ TON T_TimeoutPiston3  PT:=T#3s ]
[ T_TimeoutPiston3.Q ]─[/ DB_HMI.Piston3Extendido ]─(S) M_Alarma

[ M_ClasifPlastico ]─[ TON T_TimeoutPiston2  PT:=T#3s ]
[ T_TimeoutPiston2.Q ]─[/ DB_HMI.Piston2Extendido ]─(S) M_Alarma
```

### NW11 Contradicción sensores
```
[ DB_HMI.SensorPieza ]─[ DB_HMI.SensorPlastico ]─[ DB_HMI.SensorAluminio ]─(S) M_Alarma
```

### Auxiliar
```
M_Clasificando := M_ClasifPlastico OR M_ClasifAluminio;
```

---

## FC_Alarmas

```
[ M_Alarma ]─( ) M_LamparaAlarma
[ DB_HMI.ResetAlarma ]─(R) M_Alarma
[ DB_HMI.Emergencia ]─(S) M_Alarma
```

---

## FC_EspejoWeb (SCL)

```scl
DatosEstacion.BandaOn      := M_Banda;
DatosEstacion.PistonOn     := M_Piston1 OR M_Piston2 OR M_Piston3;
DatosEstacion.Piston1On    := M_Piston1;
DatosEstacion.Piston2On    := M_Piston2;
DatosEstacion.Piston3On    := M_Piston3;
DatosEstacion.SistemaOn    := M_SistemaOn;
DatosEstacion.ModoAuto     := M_ModoAuto;
DatosEstacion.Emergencia   := DB_HMI.Emergencia;
DatosEstacion.Alarma       := M_Alarma;
DatosEstacion.PesoActualKg := DB_HMI.PesoActualKg;
```

---

## Feedback de sensores en sim (HMI)

La HMI virtual, con “Feedback AUTO”, escribe `Piston1/2/3Extendido` ~450 ms después de ver el actuador ON en `DatosEstacion` (simula el final de carrera de simple efecto). En el 1214C real eso lo hacen los `I_PistonNExtendido` cableados.
