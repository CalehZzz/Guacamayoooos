# Networks LAD — PLC real 1214C (3 pistones · control web)

**Reglas:**
- Sensores / finales de carrera → `I_*`
- Actuadores → `Q_*` (P1 plástico · P2 latas · P3 vidrio)
- Operador → **solo** `DB_HMI.*` (sin botonera física)
- Espejo a la web → `DatosEstacion`

Los croquis **no se pegan** en TIA: inserta contactos/bobinas y escribe el tag.

| Símbolo | Significado en TIA |
|---|---|
| contacto NO | normalmente abierto |
| contacto NC | normalmente cerrado (`|/|`) |
| bobina `( )` | normal |
| bobina `(S)` | Set |
| bobina `(R)` | Reset |
| `[TON]` | timer IEC |

**Cómo leer cada network**
1. Contactos en **serie** = todos en la misma línea horizontal.
2. Ramas **paralelas** = dos (o más) líneas que terminan en la **misma bobina**.
3. Una bobina por network (salvo que se diga lo contrario).

---

## OB1

| NW | Call |
|---|---|
| 1 | `FC_Modos` |
| 2 | `FC_Secuencia` |
| 3 | `FC_Alarmas` |
| 4 | `FC_EspejoWeb` |

---

# FC_Modos

## NW1 — START → Set `M_SistemaOn`

Serie → bobina Set:

1. NO `DB_HMI.Start`
2. NC `DB_HMI.Stop`
3. NC `DB_HMI.Emergencia`
4. `(S) M_SistemaOn`

```
[ Start ]──[/ Stop ]──[/ Emergencia ]──(S) M_SistemaOn
```

---

## NW2 — STOP / EMERGENCIA → Reset `M_SistemaOn`

Dos ramas en paralelo → misma bobina Reset:

| Rama | Contactos |
|---|---|
| A | NO `DB_HMI.Stop` |
| B | NO `DB_HMI.Emergencia` |

```
[ Stop       ]──┐
                ├──(R) M_SistemaOn
[ Emergencia ]──┘
```

---

## NW3 — Modo auto

1. NO `DB_HMI.ModoAuto`
2. `( ) M_ModoAuto`

```
[ ModoAuto ]──( ) M_ModoAuto
```

---

## NW4 — Flag `M_Clasificando`

Paralelo de las dos clasificaciones:

| Rama | Contactos |
|---|---|
| A | NO `M_ClasifPlastico` |
| B | NO `M_ClasifAluminio` |

```
[ ClasifPlastico ]──┐
                    ├──( ) M_Clasificando
[ ClasifAluminio ]──┘
```

---

## NW5 — Lámpara RUN → `Q_LamparaRun`

1. NO `M_SistemaOn`
2. NC `DB_HMI.Emergencia`
3. `( ) Q_LamparaRun`

```
[ SistemaOn ]──[/ Emergencia ]──( ) Q_LamparaRun
```

---

## NW6 — Lámpara emergencia → `Q_LamparaEmergencia`

1. NO `DB_HMI.Emergencia`
2. `( ) Q_LamparaEmergencia`

```
[ Emergencia ]──( ) Q_LamparaEmergencia
```

---

# FC_Secuencia

## NW1 — Banda → `Q_Banda`

**Una sola bobina** `Q_Banda`. Dos ramas (AUTO // MANUAL).

### Rama AUTO (serie)
1. NO `M_SistemaOn`
2. NO `M_ModoAuto`
3. NC `DB_HMI.Emergencia`
4. NC `M_Alarma`
5. NC `M_Clasificando`

### Rama MANUAL (serie)
1. NO `M_SistemaOn`
2. NC `M_ModoAuto`
3. NO `DB_HMI.ManualBanda`

```
AUTO:
[ SistemaOn ]──[ ModoAuto ]──[/ Emergencia ]──[/ Alarma ]──[/ Clasificando ]──┐
                                                                              ├──( ) Q_Banda
MANUAL:                                                                       │
[ SistemaOn ]──[/ ModoAuto ]──[ ManualBanda ]─────────────────────────────────┘
```

---

## NW2 — P1 retenedor → `Q_Piston1`

Sujeta la pieza si hay pieza o si está clasificando. **Una sola bobina** `Q_Piston1`.

### Rama AUTO-A
1. NO `M_SistemaOn`
2. NO `M_ModoAuto`
3. NC `DB_HMI.Emergencia`
4. NC `M_Alarma`
5. NO `I_SensorPieza`

### Rama AUTO-B (paralelo parcial con AUTO-A en el sensor)
Misma cabecera (pasos 1–4), pero en vez de pieza:
5. NO `M_Clasificando`

En TIA: después de `|/ M_Alarma` abre **dos ramas** — una con `I_SensorPieza` y otra con `M_Clasificando` — y esas dos se juntan otra vez antes de la bobina…  
**Más fácil:** haz **tres ramas completas** a la misma bobina:

| Rama | Contactos en serie |
|---|---|
| AUTO pieza | `M_SistemaOn` · `M_ModoAuto` · `/Emergencia` · `/Alarma` · `I_SensorPieza` |
| AUTO clasif | `M_SistemaOn` · `M_ModoAuto` · `/Emergencia` · `/Alarma` · `M_Clasificando` |
| MANUAL | `M_SistemaOn` · `/ModoAuto` · `DB_HMI.ManualPiston1` |

```
[ SistemaOn ]──[ ModoAuto ]──[/ Emerg ]──[/ Alarma ]──[ SensorPieza ]──┐
[ SistemaOn ]──[ ModoAuto ]──[/ Emerg ]──[/ Alarma ]──[ Clasificando ]──┼──( ) Q_Piston1
[ SistemaOn ]──[/ ModoAuto ]──[ ManualPiston1 ]────────────────────────┘
```

---

## NW3 — Latch aluminio → Set `M_ClasifAluminio`

Serie → bobina Set:

1. NO `M_SistemaOn`
2. NO `M_ModoAuto`
3. NO `I_SensorPieza`
4. NO `I_BasculaLista`
5. NO `I_SensorAluminio`
6. NC `I_SensorPlastico`
7. NC `M_ClasifPlastico`
8. `(S) M_ClasifAluminio`

```
[ On ]─[ Auto ]─[ Pieza ]─[ Báscula ]─[ Aluminio ]─[/ Plástico ]─[/ ClasifPlastico ]─(S) M_ClasifAluminio
```

---

## NW4 — Latch plástico → Set `M_ClasifPlastico`

Serie → bobina Set:

1. NO `M_SistemaOn`
2. NO `M_ModoAuto`
3. NO `I_SensorPieza`
4. NO `I_BasculaLista`
5. NO `I_SensorPlastico`
6. NC `I_SensorAluminio`
7. NC `M_ClasifAluminio`
8. `(S) M_ClasifPlastico`

```
[ On ]─[ Auto ]─[ Pieza ]─[ Báscula ]─[ Plástico ]─[/ Aluminio ]─[/ ClasifAluminio ]─(S) M_ClasifPlastico
```

---

## NW5 — P3 aluminio → `Q_Piston3`

**Una bobina.** `ManualPiston` (DB_HMI 0.7) = manual de P3.

| Rama | Contactos en serie |
|---|---|
| AUTO | `M_ClasifAluminio` · `/I_Piston3Extendido` |
| MANUAL | `M_SistemaOn` · `/M_ModoAuto` · `DB_HMI.ManualPiston` |

```
[ ClasifAluminio ]──[/ Piston3Extendido ]──┐
                                           ├──( ) Q_Piston3
[ SistemaOn ]──[/ ModoAuto ]──[ ManualPiston ]─┘
```

---

## NW6 — P2 plástico → `Q_Piston2`

**Una bobina.**

| Rama | Contactos en serie |
|---|---|
| AUTO | `M_ClasifPlastico` · `/I_Piston2Extendido` |
| MANUAL | `M_SistemaOn` · `/M_ModoAuto` · `DB_HMI.ManualPiston2` |

```
[ ClasifPlastico ]──[/ Piston2Extendido ]──┐
                                           ├──( ) Q_Piston2
[ SistemaOn ]──[/ ModoAuto ]──[ ManualPiston2 ]─┘
```

---

## NW7 — TON retardo P3 (aluminio)

1. NO `M_ClasifAluminio`
2. NO `I_Piston3Extendido`
3. Caja **TON** instancia `T_RetardoPiston3`, PT = `T#500ms`

```
[ ClasifAluminio ]──[ Piston3Extendido ]──[ TON T_RetardoPiston3  PT:=T#500ms ]
```

---

## NW8 — Fin aluminio (Reset + conteo)

### NW8a — LAD
1. NO `T_RetardoPiston3.Q`
2. `(R) M_ClasifAluminio`

```
[ T_RetardoPiston3.Q ]──(R) M_ClasifAluminio
```

### NW8b — SCL (network aparte o mismo FC en SCL)
```scl
IF T_RetardoPiston3.Q THEN
    DatosEstacion.ContAluminio := DatosEstacion.ContAluminio + 1;
    DatosEstacion.PesoAluminioKg := DatosEstacion.PesoAluminioKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 2;
END_IF;
```

---

## NW9 — TON retardo P2 (plástico)

1. NO `M_ClasifPlastico`
2. NO `I_Piston2Extendido`
3. Caja **TON** instancia `T_RetardoPiston2`, PT = `T#500ms`

```
[ ClasifPlastico ]──[ Piston2Extendido ]──[ TON T_RetardoPiston2  PT:=T#500ms ]
```

---

## NW10 — Fin plástico (Reset + conteo)

### NW10a — LAD
1. NO `T_RetardoPiston2.Q`
2. `(R) M_ClasifPlastico`

```
[ T_RetardoPiston2.Q ]──(R) M_ClasifPlastico
```

### NW10b — SCL
```scl
IF T_RetardoPiston2.Q THEN
    DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
    DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 1;
END_IF;
```

---

## NW11 — Timeout P3 → alarma

Dos networks (o dos renglones):

**NW11a — arranca timer**
1. NO `M_ClasifAluminio`
2. `[TON] T_TimeoutPiston3` PT=`T#3s`

```
[ ClasifAluminio ]──[ TON T_TimeoutPiston3  PT:=T#3s ]
```

**NW11b — si vence y no llegó a 100%**
1. NO `T_TimeoutPiston3.Q`
2. NC `I_Piston3Extendido`
3. `(S) M_Alarma`

```
[ T_TimeoutPiston3.Q ]──[/ Piston3Extendido ]──(S) M_Alarma
```

---

## NW12 — Timeout P2 → alarma

**NW12a**
```
[ ClasifPlastico ]──[ TON T_TimeoutPiston2  PT:=T#3s ]
```

**NW12b**
```
[ T_TimeoutPiston2.Q ]──[/ Piston2Extendido ]──(S) M_Alarma
```

Contactos NW12b: NO `T_TimeoutPiston2.Q` · NC `I_Piston2Extendido` · `(S) M_Alarma`

---

## NW13 — Sensores contradictorios

1. NO `I_SensorPieza`
2. NO `I_SensorPlastico`
3. NO `I_SensorAluminio`
4. `(S) M_Alarma`

```
[ Pieza ]──[ Plástico ]──[ Aluminio ]──(S) M_Alarma
```

---

# FC_Alarmas

## NW1 — Lámpara alarma
```
[ M_Alarma ]──( ) Q_LamparaAlarma
```

## NW2 — Reset (web)
```
[ DB_HMI.ResetAlarma ]──(R) M_Alarma
```

## NW3 — Emergencia pone alarma
```
[ DB_HMI.Emergencia ]──(S) M_Alarma
```

---

# FC_EspejoWeb (SCL)

```scl
DatosEstacion.SistemaOn    := M_SistemaOn;
DatosEstacion.ModoAuto     := M_ModoAuto;
DatosEstacion.Emergencia   := DB_HMI.Emergencia;
DatosEstacion.Alarma       := M_Alarma;
DatosEstacion.BandaOn      := Q_Banda;
DatosEstacion.PistonOn     := Q_Piston1 OR Q_Piston2 OR Q_Piston3;
DatosEstacion.Piston1On    := Q_Piston1;
DatosEstacion.Piston2On    := Q_Piston2;
DatosEstacion.Piston3On    := Q_Piston3;
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
