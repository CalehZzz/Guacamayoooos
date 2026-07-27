# LAD — las 4 FC críticas (dibújalas así en TIA)

Guía **paso a paso** para `FC_Modos`, `FC_Secuencia`, `FC_Alarmas` y `FC_EspejoWeb`.  
Los croquis **no se pegan** en TIA: inserta contactos, bobinas y TON y escribe el tag en cada `???`.

| Símbolo | En TIA |
|---|---|
| `\| X \|` | Contacto normalmente abierto (NO) |
| `\|/ X \|` | Contacto normalmente cerrado (NC) |
| `( X )` | Bobina normal |
| `(S X)` | Set coil |
| `(R X)` | Reset coil |
| `(P X)` | Positive edge coil (flanco) |
| `[TON]` | Caja TON (IEC_TIMER) |

**Regla única:** `DB_HMI.*` = web · `M_Sensor*` / `M_Banda` / `M_Piston` = Automation Studio · `M_SistemaOn` etc. = lógica interna.

---

## Antes de dibujar

1. Crea las FC en LAD: `FC_Modos`, `FC_Secuencia`, `FC_Alarmas`, `FC_EspejoWeb`.
2. Crea los tags según `TABLA_TAGS_DESDE_CERO.md` (grupos A y B en `%M`, DB1 y DB3).
3. En **Bit logic** localiza: Coil, Set, Reset, Positive edge coil.
4. Instancias TON: `T_RetardoPiston`, `T_TimeoutPiston` (tipo `TON_TIME`, PT en la caja).

---

# 1) FC_Modos — 5 networks

## NW1 — START → Set `M_SistemaOn`

**Qué hace:** Si la web pulsa START (y no hay STOP ni emergencia), el sistema queda encendido.

**Pasos en TIA:**
1. Inserta **3 contactos en serie** (misma línea horizontal):
   - `DB_HMI.Start` — NO
   - `DB_HMI.Stop` — **NC** (`|/|`)
   - `DB_HMI.Emergencia` — **NC**
2. Al final: bobina **Set (S)** → tag `M_SistemaOn`

```
     DB_HMI          DB_HMI           DB_HMI
---|    .Start    |---|/   .Stop    |---|/ .Emergencia |----(S M_SistemaOn)
```

---

## NW2 — STOP / EMERGENCIA → Reset `M_SistemaOn`

**Qué hace:** STOP o emergencia apagan el latch.

**Pasos en TIA:**
1. Rama superior: contacto NO `DB_HMI.Stop`
2. Rama inferior (paralelo): contacto NO `DB_HMI.Emergencia`
3. Las dos ramas convergen en una sola bobina **Reset (R)** → `M_SistemaOn`

```
---| DB_HMI.Stop       |----+----(R M_SistemaOn)
---| DB_HMI.Emergencia |----+
```

> En TIA: dibuja la primera línea hasta la bobina; luego **añade rama paralela** debajo y conecta ambas al mismo Reset.

---

## NW3 — Modo AUTO

**Pasos:** Un contacto NO `DB_HMI.ModoAuto` → bobina **normal** `( M_ModoAuto )`

```
---| DB_HMI.ModoAuto |----( M_ModoAuto )
```

---

## NW4 — Lámpara RUN

```
---| M_SistemaOn |---|/ DB_HMI.Emergencia |----( M_LamparaRun )
```

---

## NW5 — Lámpara emergencia

```
---| DB_HMI.Emergencia |----( M_LamparaEmergencia )
```

---

# 2) FC_Secuencia — 9 networks

## NW1 — Banda AUTO // MANUAL → `M_Banda`

**Qué hace:** En AUTO la banda corre si el sistema está ON y no hay alarma/clasificación. En MANUAL obedece `DB_HMI.ManualBanda`.

**Pasos en TIA:**
1. **Rama AUTO** (arriba), contactos en serie:
   - `M_SistemaOn`
   - `M_ModoAuto`
   - `DB_HMI.Emergencia` — NC
   - `M_Alarma` — NC
   - `M_Clasificando` — NC
2. **Rama MANUAL** (abajo, paralelo):
   - `M_SistemaOn`
   - `M_ModoAuto` — **NC** (`|/|`)
   - `DB_HMI.ManualBanda` — NO
3. Una sola bobina **normal** a la derecha: `( M_Banda )`

```
  AUTO:
---| M_SistemaOn |---| M_ModoAuto |---|/ DB_HMI.Emergencia |---|/ M_Alarma |---|/ M_Clasificando |--+
                                                                                                        |
  MANUAL:                                                                                               +----( M_Banda )
---| M_SistemaOn |---|/ M_ModoAuto |---| DB_HMI.ManualBanda |------------------------------------------+
```

---

## NW2 — Pulso plástico (bobina P)

**Importante:** Los **6 contactos van en la misma línea** (serie), no en paralelo.

**Pasos:**
1. En serie: `M_SistemaOn`, `M_ModoAuto`, `M_SensorPieza`, `M_BasculaLista`, `M_SensorPlastico`
2. Último contacto: `M_SensorAluminio` — **NC**
3. Bobina **Positive edge (P)**:
   - Resultado: `M_PulsePlastico`
   - Memoria de flanco (si TIA pide dos campos): `M_EdgePlastico`

```
---| M_SistemaOn |---| M_ModoAuto |---| M_SensorPieza |---| M_BasculaLista |
---| M_SensorPlastico |---|/ M_SensorAluminio |----(P M_PulsePlastico)
                                                      mem: M_EdgePlastico
```

---

## NW3 — Contar plástico (SCL, no LAD)

Cambia el lenguaje de esta network a **SCL** (clic derecho → Change language):

```scl
IF M_PulsePlastico THEN
    DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
    DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 1;
END_IF;
```

---

## NW4 — Aluminio → Set `M_Clasificando`

```
---| M_SistemaOn |---| M_ModoAuto |---| M_SensorPieza |---| M_BasculaLista |
---| M_SensorAluminio |---|/ M_SensorPlastico |----(S M_Clasificando)
```

---

## NW5 — Pistón AUTO // MANUAL → `M_Piston`

Igual estructura que NW1 de banda:

```
  AUTO:
---| M_Clasificando |---|/ M_PistonExtendido |--+
                                                |
  MANUAL:                                       +----( M_Piston )
---| M_SistemaOn |---|/ M_ModoAuto |---| DB_HMI.ManualPiston |--+
```

---

## NW6 — TON retardo pistón

**Pasos:**
1. Contactos en serie: `M_Clasificando`, `M_PistonExtendido`
2. Inserta caja **TON** → instancia `T_RetardoPiston`
3. En `PT` del TON: `T#500ms`

```
---| M_Clasificando |---| M_PistonExtendido |----[ TON T_RetardoPiston  PT:=T#500ms ]
```

---

## NW7 — Fin clasificación + contar aluminio

**Parte LAD:**
```
---| T_RetardoPiston.Q |----(R M_Clasificando)
```

**Parte SCL** (misma FC, network aparte o debajo en SCL):

```scl
IF T_RetardoPiston.Q THEN
    DatosEstacion.ContAluminio := DatosEstacion.ContAluminio + 1;
    DatosEstacion.PesoAluminioKg := DatosEstacion.PesoAluminioKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 2;
END_IF;
```

---

## NW8 — Timeout pistón → alarma

**Network A — arranque TON:**
```
---| M_Clasificando |----[ TON T_TimeoutPiston  PT:=T#3s ]
```

**Network B — alarma si no extendió:**
```
---| T_TimeoutPiston.Q |---|/ M_PistonExtendido |----(S M_Alarma)
```

---

## NW9 — Sensores contradictorios

```
---| M_SensorPieza |---| M_SensorPlastico |---| M_SensorAluminio |----(S M_Alarma)
```

---

# 3) FC_Alarmas — 3 networks

## NW1 — Lámpara alarma

```
---| M_Alarma |----( M_LamparaAlarma )
```

## NW2 — Reset desde web

```
---| DB_HMI.ResetAlarma |----(R M_Alarma)
```

## NW3 — Emergencia fuerza alarma

```
---| DB_HMI.Emergencia |----(S M_Alarma)
```

---

# 4) FC_EspejoWeb — 1 network SCL

Cambia toda la FC a **SCL** (o una sola network SCL):

```scl
DatosEstacion.SistemaOn    := M_SistemaOn;
DatosEstacion.ModoAuto     := M_ModoAuto;
DatosEstacion.Emergencia   := DB_HMI.Emergencia;
DatosEstacion.Alarma       := M_Alarma;
DatosEstacion.BandaOn      := M_Banda;
DatosEstacion.PistonOn     := M_Piston;
DatosEstacion.FinSesion    := DB_HMI.FinSesion;
DatosEstacion.PesoActualKg := DB_HMI.PesoActualKg;

IF DB_HMI.Emergencia THEN
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

# OB1 — llamadas (4 networks)

| NW | Instrucción |
|---|---|
| 1 | `CALL FC_Modos` |
| 2 | `CALL FC_Secuencia` |
| 3 | `CALL FC_Alarmas` |
| 4 | `CALL FC_EspejoWeb` |

En TIA: **Instructions → Program control → CALL** → elige la FC.

---

## Checklist visual rápido

| ¿Dónde? | Tag correcto | Tag incorrecto |
|---|---|---|
| Botón START web | `DB_HMI.Start` | `M_SensorPieza`, `I_Start` |
| Sensor pieza AS | `M_SensorPieza` | `DB_HMI.SensorPieza` (solo demo) |
| Salida banda | `M_Banda` | `Q_Banda`, `%Q0.0` |
| Salida pistón | `M_Piston` | `Q_Piston` |
| Estado a web | `DatosEstacion.*` | escribir directo en Firestore |

---

## Errores que ya vimos

| Error | Solución |
|---|---|
| Doble bobina en `M_Banda` | Solo NW1 de FC_Secuencia; no otra network con `( M_Banda )` |
| Contactos en paralelo en NW2 plástico | Los 6 van **en serie** en una línea |
| `S M_SistemaOn` como nombre de tag | El tag es `M_SistemaOn`; la bobina es tipo **Set** |
| Sensores no cambian en AS | Ver `KEPSERVER_AS_MAPEO.md` — KEP debe mapear `%M2.x` |
