# Programa LAD — orden final de networks

Esta es la **lista ordenada** de cómo debe quedar tu programa.
Cada network = una red en TIA. Síguelas **de arriba hacia abajo**.

> Los dibujos `---| |----( )---` **no se pegan** en TIA.  
> Inserta contactos/bobinas/TON con la barra LAD y pon el **nombre del tag**.

Leyenda rápida:

| Símbolo en el croquis | En TIA |
|---|---|
| `\| X \|` | Contacto abierto → tag `X` |
| `\|/ X \|` | Contacto cerrado → tag `X` |
| `( X )` | Bobina normal |
| `(S X)` | Bobina Set |
| `(R X)` | Bobina Reset |
| `TON` | Caja TON (instancia arriba + PT) |

---

## 0) Vista general (así se organiza el proyecto)

```
OB1
 ├─ Network 1 → Call FC_Modos
 ├─ Network 2 → Call FC_Secuencia
 ├─ Network 3 → Call FC_Alarmas
 └─ Network 4 → Call FC_EspejoWeb

FC_Modos        → 5 networks   (arranque / paro / emergencia / modo)
FC_Secuencia    → 10 networks  (banda, clasificar, TON, manual)
FC_Alarmas      → 3 networks
FC_EspejoWeb    → 1 network SCL (copia al DB para la web)

DB globales que SÍ usas:
  • DatosEstacion
  • (los DB de instancia de tus TON: T_RetardoPiston, T_TimeoutPiston)
```

---

## 1) OB1 — solo llamadas

| # | Qué poner |
|---|---|
| NW1 | Call `FC_Modos` |
| NW2 | Call `FC_Secuencia` |
| NW3 | Call `FC_Alarmas` |
| NW4 | Call `FC_EspejoWeb` |

---

## 2) FC_Modos

### NW1 — Arrancar sistema (Set)
**Objetivo:** al pulsar Start, enciende el sistema.

```
---| I_Start |-----|/ I_Stop |-----|/ I_Emergencia |-----(S M_SistemaOn)
```

| Elemento | Tag |
|---|---|
| Contacto abierto | `I_Start` |
| Contacto cerrado | `I_Stop` |
| Contacto cerrado | `I_Emergencia` |
| Bobina Set | `M_SistemaOn` |

---

### NW2 — Parar sistema (Reset) — dos caminos en paralelo
**Objetivo:** Stop **o** Emergencia apagan el sistema.

```
---| I_Stop       |-----+-----(R M_SistemaOn)
                        |
---| I_Emergencia |-----+
```

Cómo hacerlo en TIA: un contacto `I_Stop` hacia la bobina Reset; debajo, otro riel/branch con `I_Emergencia` que llega a **la misma** bobina `(R M_SistemaOn)`.

---

### NW3 — Copiar modo automático
```
---| I_ModoAuto |-----( M_ModoAuto )
```

---

### NW4 — Lámpara RUN
```
---| M_SistemaOn |-----|/ I_Emergencia |-----( Q_LamparaRun )
```

---

### NW5 — Lámpara emergencia
```
---| I_Emergencia |-----( Q_LamparaEmergencia )
```

---

## 3) FC_Secuencia

### NW1 — Pedido de banda (guarda en memoria, evita pelear la salida)
**Objetivo:** calcular si la banda debe ir ON (auto **o** manual).

Primero crea estos tags Bool si no existen:
- `M_CmdBanda`
- `M_CmdPiston`

```
        (rama AUTO)
---| M_SistemaOn |---| M_ModoAuto |---|/ I_Emergencia |---|/ M_Alarma |---|/ M_Clasificando |--+
                                                                                              |
        (rama MANUAL)                                                                         +----( M_CmdBanda )
---| M_SistemaOn |---|/ M_ModoAuto |---| I_ManualBanda |--------------------------------------+
```

En TIA: dos ramas en paralelo que terminan en **una sola** bobina `M_CmdBanda`.

---

### NW2 — Salida física banda
```
---| M_CmdBanda |-----( Q_Banda )
```

---

### NW3 — Detectar plástico (flanco → pulso)
**Objetivo:** marcar un pulso cuando hay botella válida.

```
---| M_SistemaOn |---| M_ModoAuto |---| I_SensorPieza |---| I_BasculaLista |
---| I_SensorPlastico |---|/ I_SensorAluminio |-----(P M_PulsePlastico)
```

`(P …)` = bobina de **flanco positivo** (Positive edge coil) en TIA.  
Si no la encuentras: Instructions → Bit logic → **P coil** / Positive edge.

---

### NW4 — Contar plástico + sumar peso (SCL)
Cambia el lenguaje de **esta network** a **SCL** (o inserta un bloque SCL).

```scl
IF M_PulsePlastico THEN
    DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
    DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 1;
END_IF;
```

---

### NW5 — Detectar aluminio → empezar clasificación
```
---| M_SistemaOn |---| M_ModoAuto |---| I_SensorPieza |---| I_BasculaLista |
---| I_SensorAluminio |---|/ I_SensorPlastico |-----(S M_Clasificando)
```

---

### NW6 — Pedido de pistón (auto clasificando **o** manual)
```
        (rama AUTO: clasificando y aún no extendido)
---| M_Clasificando |---|/ I_PistonExtendido |--+
                                               |
        (rama MANUAL)                          +----( M_CmdPiston )
---| M_SistemaOn |---|/ M_ModoAuto |---| I_ManualPiston |--+
```

---

### NW7 — Salida física pistón
```
---| M_CmdPiston |-----( Q_Piston )
```

---

### NW8 — TON retardo con pistón extendido
**Objetivo:** cuando el pistón ya extendió, espera 0.5 s.

```
---| M_Clasificando |---| I_PistonExtendido |----[ TON ]

Arriba del TON:  T_RetardoPiston     ← instancia (su propio DB)
PT:              T#500ms
IN:              viene de los contactos de la izquierda
Q:               la usamos en NW9 como T_RetardoPiston.Q
```

Detalle del TON: `docs/06_COMO_USAR_TON.md`

---

### NW9 — Timer cumplió → contar aluminio y soltar clasificación
**Parte A (LAD):**
```
---| T_RetardoPiston.Q |-----(R M_Clasificando)
```

**Parte B (misma network en SCL, o NW9b SCL):**
```scl
IF T_RetardoPiston.Q THEN
    DatosEstacion.ContAluminio := DatosEstacion.ContAluminio + 1;
    DatosEstacion.PesoAluminioKg := DatosEstacion.PesoAluminioKg + DatosEstacion.PesoActualKg;
    DatosEstacion.UltimoMaterial := 2;
END_IF;
```

> Tip: si te complica mezclar LAD+SCL, deja NW9 solo el `(R M_Clasificando)` y crea **NW9b** solo SCL con el `IF` de arriba.

---

### NW10 — TON timeout + alarma de pistón
**NW10a — TON**
```
---| M_Clasificando |----[ TON ]

Arriba: T_TimeoutPiston
PT:     T#3s
```

**NW10b — si timeout y no extendió → alarma**
```
---| T_TimeoutPiston.Q |---|/ I_PistonExtendido |-----(S M_Alarma)
```

---

### NW11 — Sensores contradictorios → alarma
```
---| I_SensorPieza |---| I_SensorPlastico |---| I_SensorAluminio |-----(S M_Alarma)
```

---

## 4) FC_Alarmas

### NW1 — Lámpara alarma
```
---| M_Alarma |-----( Q_LamparaAlarma )
```

### NW2 — Reset alarma desde HMI/botón
```
---| M_ResetAlarma |-----(R M_Alarma)
```

### NW3 — Emergencia también pone alarma
```
---| I_Emergencia |-----(S M_Alarma)
```

---

## 5) FC_EspejoWeb — 1 sola network en SCL

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

## Checklist visual — ¿ya quedó ordenado?

### FC_Modos
- [ ] NW1 Set sistema
- [ ] NW2 Reset sistema (Stop // Emergencia)
- [ ] NW3 Modo auto
- [ ] NW4 Lámpara run
- [ ] NW5 Lámpara emergencia

### FC_Secuencia
- [ ] NW1 `M_CmdBanda` (auto // manual)
- [ ] NW2 `Q_Banda`
- [ ] NW3 pulso plástico
- [ ] NW4 SCL contar plástico
- [ ] NW5 Set clasificando (aluminio)
- [ ] NW6 `M_CmdPiston`
- [ ] NW7 `Q_Piston`
- [ ] NW8 TON `T_RetardoPiston`
- [ ] NW9 Reset clasificando + SCL contar aluminio
- [ ] NW10 TON timeout + alarma
- [ ] NW11 sensores contradictorios

### FC_Alarmas + EspejoWeb
- [ ] 3 networks de alarmas
- [ ] 1 SCL espejo web

---

## DB con nombres random que no usas

**No pasa nada grave** si existen: no afectan la lógica si ningún network los llama.  
Pero **sí conviene borrarlos** para no marearte.

### Cómo eliminarlos en TIA Portal
1. Project tree → tu PLC → **Program blocks**
2. Busca los DB raros (nombres largos/random, o `TON_DB`, `IEC_Timer…` viejos)
3. **Antes de borrar:** abre tus TON buenos (`T_RetardoPiston`, `T_TimeoutPiston`) y anota qué DB de instancia sí usan (el de arriba del bloque TON)
4. Clic derecho en el DB basura → **Delete**
5. Si TIA dice que tiene referencias: **no lo borres** (alguien lo usa)
6. Compile (`Ctrl+B`). Si queda un error “operand missing” en un TON, reasigna la instancia arriba del TON

### Qué NO borrar
- `DatosEstacion`
- El DB de instancia de `T_RetardoPiston`
- El DB de instancia de `T_TimeoutPiston`
- Tu Hardware / HMI

### Resumen
| Situación | ¿Problema? |
|---|---|
| DB random sin usar | No rompe el programa, solo ensucia |
| Lo borras y nadie lo referenciaba | Perfecto |
| Lo borras y un TON lo usaba | El TON queda en rojo → vuelve a crear instancia arriba del TON |
