# Programa LAD — versión final (cópiala así)

Lista **definitiva** de networks. Variables = las originales del mapa (`Q_Banda`, `Q_Piston`, etc.).  
Banda y pistón ya van **juntas** (auto // manual) en **una sola** network cada una → no hay doble bobina.

> Los croquis **no se pegan** en TIA. Inserta contactos/bobinas/TON y pon el tag.

| Croquis | En TIA |
|---|---|
| `\| X \|` | Contacto abierto |
| `\|/ X \|` | Contacto cerrado |
| `( X )` | Bobina |
| `(S X)` / `(R X)` | Set / Reset |
| `(P X)` | Flanco positivo |
| `[TON]` | Caja TON |

---

## Estructura del proyecto

```
OB1
 ├─ NW1 Call FC_Modos
 ├─ NW2 Call FC_Secuencia
 ├─ NW3 Call FC_Alarmas
 └─ NW4 Call FC_EspejoWeb

FC_Modos      → 5 networks
FC_Secuencia  → 9 networks
FC_Alarmas    → 3 networks
FC_EspejoWeb  → 1 network SCL
```

DB que sí usas: `DatosEstacion` + instancias de `T_RetardoPiston` y `T_TimeoutPiston`.

---

# OB1

| NW | Contenido |
|---|---|
| 1 | Call `FC_Modos` |
| 2 | Call `FC_Secuencia` |
| 3 | Call `FC_Alarmas` |
| 4 | Call `FC_EspejoWeb` |

---

# FC_Modos

## NW1 — Start (Set sistema)
```
---| I_Start |-----|/ I_Stop |-----|/ I_Emergencia |-----(S M_SistemaOn)
```

## NW2 — Stop / Emergencia (Reset) — paralelo
```
---| I_Stop       |----+-----(R M_SistemaOn)
                       |
---| I_Emergencia |----+
```

## NW3 — Modo auto
```
---| I_ModoAuto |-----( M_ModoAuto )
```

## NW4 — Lámpara RUN
```
---| M_SistemaOn |-----|/ I_Emergencia |-----( Q_LamparaRun )
```

## NW5 — Lámpara emergencia
```
---| I_Emergencia |-----( Q_LamparaEmergencia )
```

---

# FC_Secuencia

## NW1 — Banda (AUTO // MANUAL) → una sola bobina `Q_Banda`
```
  AUTO:
---| M_SistemaOn |---| M_ModoAuto |---|/ I_Emergencia |---|/ M_Alarma |---|/ M_Clasificando |--+
                                                                                              |
  MANUAL:                                                                                     +----( Q_Banda )
---| M_SistemaOn |---|/ M_ModoAuto |---| I_ManualBanda |--------------------------------------+
```

En TIA: una network, **dos ramas en paralelo**, una sola bobina `( Q_Banda )` a la derecha.

---

## NW2 — Pulso plástico
```
---| M_SistemaOn |---| M_ModoAuto |---| I_SensorPieza |---| I_BasculaLista |
---| I_SensorPlastico |---|/ I_SensorAluminio |-----(P M_PulsePlastico)
```

---

## NW3 — Contar plástico (SCL)
```scl
IF M_PulsePlastico THEN
    DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
    DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 1;
END_IF;
```

---

## NW4 — Detectar aluminio → Set clasificando
```
---| M_SistemaOn |---| M_ModoAuto |---| I_SensorPieza |---| I_BasculaLista |
---| I_SensorAluminio |---|/ I_SensorPlastico |-----(S M_Clasificando)
```

---

## NW5 — Pistón (AUTO // MANUAL) → una sola bobina `Q_Piston`
```
  AUTO:
---| M_Clasificando |---|/ I_PistonExtendido |--+
                                               |
  MANUAL:                                      +----( Q_Piston )
---| M_SistemaOn |---|/ M_ModoAuto |---| I_ManualPiston |--+
```

---

## NW6 — TON retardo pistón
```
---| M_Clasificando |---| I_PistonExtendido |----[ TON ]

Arriba: T_RetardoPiston
PT:     T#500ms
```

---

## NW7 — Timer OK → Reset clasificando + contar aluminio

**7a LAD:**
```
---| T_RetardoPiston.Q |-----(R M_Clasificando)
```

**7b SCL** (otra network, o la misma si mezclas):
```scl
IF T_RetardoPiston.Q THEN
    DatosEstacion.ContAluminio := DatosEstacion.ContAluminio + 1;
    DatosEstacion.PesoAluminioKg := DatosEstacion.PesoAluminioKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 2;
END_IF;
```

---

## NW8 — TON timeout + alarma pistón

**8a TON:**
```
---| M_Clasificando |----[ TON ]

Arriba: T_TimeoutPiston
PT:     T#3s
```

**8b alarma:**
```
---| T_TimeoutPiston.Q |---|/ I_PistonExtendido |-----(S M_Alarma)
```

(Puedes dejar 8a y 8b como dos networks seguidas.)

---

## NW9 — Sensores contradictorios
```
---| I_SensorPieza |---| I_SensorPlastico |---| I_SensorAluminio |-----(S M_Alarma)
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
---| I_Emergencia |-----(S M_Alarma)
```

---

# FC_EspejoWeb (1 network SCL)

```scl
DatosEstacion.SistemaOn  := M_SistemaOn;
DatosEstacion.ModoAuto   := M_ModoAuto;
DatosEstacion.Emergencia := I_Emergencia;
DatosEstacion.Alarma     := M_Alarma;
DatosEstacion.BandaOn    := Q_Banda;
DatosEstacion.PistonOn   := Q_Piston;
DatosEstacion.FinSesion  := I_FinSesion;

IF I_Emergencia THEN
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

# Checklist rápido

**FC_Modos:** NW1…NW5  
**FC_Secuencia:**
- [ ] NW1 `Q_Banda` (auto//manual juntos)
- [ ] NW2 `M_PulsePlastico`
- [ ] NW3 SCL plástico
- [ ] NW4 Set `M_Clasificando`
- [ ] NW5 `Q_Piston` (auto//manual juntos)
- [ ] NW6 `T_RetardoPiston`
- [ ] NW7 Reset + SCL aluminio
- [ ] NW8 `T_TimeoutPiston` + alarma
- [ ] NW9 sensores contradictorios  

**FC_Alarmas:** 3 · **EspejoWeb:** 1 SCL  

Luego: **Compile** (`Ctrl+B`).
