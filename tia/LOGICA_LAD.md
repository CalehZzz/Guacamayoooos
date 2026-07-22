# Lógica LAD — redes sugeridas (cópialas en TIA)

No es un archivo importable: son las redes que debes **dibujar** en lenguaje de contactos (LAD). Usa los nombres simbólicos del mapa I/O.

## Cómo leer estos dibujos (muy importante)

El texto tipo:

```
--| I_Start |----|/| I_Stop |----( S  M_SistemaOn )---
```

**NO se escribe en TIA.** Es solo un croquis. En el editor LAD haces esto:

| Dibujo en esta guía | Qué insertar en TIA |
|---|---|
| `\| I_Start \|` | Contacto **normalmente abierto** → operand = tag `I_Start` |
| `\|/\|\ I_Stop \|` | Contacto **normalmente cerrado** → operand = tag `I_Stop` |
| `(   M_xxx )` | Bobina normal → tag `M_xxx` |
| `( S  M_xxx )` | Bobina **Set** → tag `M_xxx` |
| `( R  M_xxx )` | Bobina **Reset** → tag `M_xxx` |
| `[TON T_RetardoPiston …]` | Instrucción **TON** desde la paleta (no escribas la palabra TON a mano en un contacto) |

Sobre las letras del nombre (`I_`, `Q_`, `M_`, `T_`):

- Son parte del **nombre del tag** que tú creaste (`I_Start`, `M_SistemaOn`…).
- En el contacto/bobina escribes **solo el nombre completo del tag**, o arrastras el tag desde la lista.
- **No** escribas `%I I_Start` ni `I I_Start`. Si el tag existe, TIA acepta `I_Start` o su dirección `%I0.0`.

---

## FC_Modos

### Network 1 — Latch sistema ON
```
--| I_Start |----|/| I_Stop |----|/| I_Emergencia |----( S  M_SistemaOn )---
```

### Network 2 — Reset sistema
```
--| I_Stop |----+----( R  M_SistemaOn )---
--| I_Emergencia |--+
```

### Network 3 — Modo auto (desde entrada o HMI)
```
--| I_ModoAuto |----(   M_ModoAuto )---
```
(Si el modo lo maneja solo la HMI, enlaza el botón HMI directo a `M_ModoAuto` y omite esta red.)

### Network 4 — Lámpara run
```
--| M_SistemaOn |----|/| I_Emergencia |----(   Q_LamparaRun )---
```

### Network 5 — Lámpara emergencia
```
--| I_Emergencia |----(   Q_LamparaEmergencia )---
```

---

## FC_Secuencia (modo automático simplificado)

Idea: banda corre en auto; al detectar pieza + báscula lista + sensor material, cuenta y (si aluminio) activa pistón con temporizador.

### Network 1 — Banda en automático
```
--| M_SistemaOn |----| M_ModoAuto |----|/| I_Emergencia |----|/| M_Alarma |
        ----|/| M_Clasificando |----(   Q_Banda )---
```

### Network 2 — Detectar pieza válida (plástico)
```
--| M_SistemaOn |----| M_ModoAuto |----| I_SensorPieza |----| I_BasculaLista |
        ----| I_SensorPlastico |----|/| I_SensorAluminio |
        ----[ P  M_PulsePlastico ]---   // flanco positivo (o usa contactos one-shot)
```

### Network 3 — Contar plástico + sumar peso
En SCL (más fácil para sumar Real) dentro de un Network SCL, o usa ADD:
```
IF M_PulsePlastico THEN
  DatosEstacion.ContPlastico := DatosEstacion.ContPlastico + 1;
  DatosEstacion.PesoPlasticoKg := DatosEstacion.PesoPlasticoKg + DatosEstacion.PesoActualKg;
  DatosEstacion.UltimoMaterial := 1;
END_IF;
```

### Network 4 — Detectar aluminio
```
--| M_SistemaOn |----| M_ModoAuto |----| I_SensorPieza |----| I_BasculaLista |
        ----| I_SensorAluminio |----|/| I_SensorPlastico |
        ----( S  M_Clasificando )---
```

### Network 5 — Extender pistón mientras clasifica aluminio
```
--| M_Clasificando |----|/| I_PistonExtendido |----(   Q_Piston )---
```

### Network 6 — Al llegar extendido: contar y pedir retraer
```
--| M_Clasificando |----| I_PistonExtendido |----[TON T_RetardoPiston, PT=T#0.5s]
```
Cuando `T_RetardoPiston.Q`:
```
  DatosEstacion.ContAluminio := DatosEstacion.ContAluminio + 1;
  DatosEstacion.PesoAluminioKg := DatosEstacion.PesoAluminioKg + DatosEstacion.PesoActualKg;
  DatosEstacion.UltimoMaterial := 2;
  RESET M_Clasificando;  // Q_Piston cae → cilindro retorna por muelle / válvula
```

### Network 7 — Timeout pistón (alarma)
```
--| M_Clasificando |----[TON T_TimeoutPiston, PT=T#3s]
--| T_TimeoutPiston.Q |----|/| I_PistonExtendido |----( S  M_Alarma )---
```

### Network 8 — Sensores contradictorios
```
--| I_SensorPieza |----| I_SensorPlastico |----| I_SensorAluminio |----( S  M_Alarma )---
```

### Network 9 — Banda / pistón en MANUAL
```
--| M_SistemaOn |----|/| M_ModoAuto |----| I_ManualBanda |----(   Q_Banda )---
--| M_SistemaOn |----|/| M_ModoAuto |----| I_ManualPiston |----(   Q_Piston )---
```
> Si también tienes la red de banda automática, combina con contactos en paralelo (OR) para no pelear salidas: una sola bobina `Q_Banda` alimentada por (auto OR manual).

---

## FC_Alarmas

### Network 1 — Lámpara alarma
```
--| M_Alarma |----(   Q_LamparaAlarma )---
```

### Network 2 — Reset alarma (botón HMI `M_ResetAlarma`)
```
--| M_ResetAlarma |----( R  M_Alarma )---
```

### Network 3 — Emergencia también prende alarma
```
--| I_Emergencia |----( S  M_Alarma )---
```

---

## FC_EspejoWeb

Copia estados al DB (puedes hacerlo todo en un Network SCL):

```scl
DatosEstacion.SistemaOn   := M_SistemaOn;
DatosEstacion.ModoAuto    := M_ModoAuto;
DatosEstacion.Emergencia  := I_Emergencia;
DatosEstacion.Alarma      := M_Alarma;
DatosEstacion.BandaOn     := Q_Banda;
DatosEstacion.PistonOn    := Q_Piston;
DatosEstacion.FinSesion   := I_FinSesion;

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

Para **peso de prueba** sin báscula real, en HMI escribe valores a `DatosEstacion.PesoActualKg` (0.04 plástico, 0.02 aluminio) antes de simular la pieza.

---

## Orden de prueba en PLCSIM (una pieza plástica)

1. `I_Emergencia=0`, `I_Stop=0`, `M_ModoAuto=1`
2. Pulso `I_Start` → `M_SistemaOn=1`, `Q_Banda=1`
3. Escribe `PesoActualKg=0.045`
4. `I_BasculaLista=1`, `I_SensorPieza=1`, `I_SensorPlastico=1`, `I_SensorAluminio=0`
5. Verifica `ContPlastico` sube y `PesoPlasticoKg` aumenta
6. Baja sensores a 0

## Una pieza aluminio

1. `PesoActualKg=0.02`
2. `I_SensorPieza=1`, `I_BasculaLista=1`, `I_SensorAluminio=1`, `I_SensorPlastico=0`
3. Debe activarse `Q_Piston`
4. Simula `I_PistonExtendido=1` → tras el TON cuenta y libera pistón
5. `I_PistonRetractado=1`
