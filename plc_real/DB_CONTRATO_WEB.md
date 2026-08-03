# Contrato web — mismos offsets que el demo (+ detalle 3 pistones)

Para que `plc_bridge.py` / `plc_bridge_real.py` funcionen sin romper el tamaño de 22 bytes.

**Optimized block access = OFF** en ambos DB.

En PLC real el operador es **100 % web**: todo comando entra por `DB_HMI` (no hay pulsadores físicos).

---

## `DatosEstacion` — DB **1**

| Offset | Nombre | Tipo | Notas |
|---|---|---|---|
| 0.0 | `ContPlastico` | Int | |
| 2.0 | `ContAluminio` | Int | |
| 4.0 | `PesoPlasticoKg` | Real | |
| 8.0 | `PesoAluminioKg` | Real | |
| 12.0 | `PesoActualKg` | Real | |
| 16.0 | `SesionActiva` | Bool | |
| 16.1 | `FinSesion` | Bool | |
| 16.2 | `SistemaOn` | Bool | |
| 16.3 | `ModoAuto` | Bool | |
| 16.4 | `Emergencia` | Bool | |
| 16.5 | `Alarma` | Bool | |
| 16.6 | `BandaOn` | Bool | |
| 16.7 | `PistonOn` | Bool | **OR** de P1/P2/P3 (compat web/demo) |
| 17.0 | `Piston1On` | Bool | Retenedor `Q_Piston1` |
| 17.1 | `Piston2On` | Bool | Plástico `Q_Piston2` |
| 17.2 | `Piston3On` | Bool | Aluminio `Q_Piston3` |
| 18.0 | `EstadoMaquina` | Int | |
| 20.0 | `UltimoMaterial` | Int | |

Tamaño legible bridge: **22 bytes** (byte 17 era padding; ahora lleva el detalle de pistones).

En `FC_EspejoWeb`:
```scl
DatosEstacion.BandaOn   := Q_Banda;
DatosEstacion.PistonOn  := Q_Piston1 OR Q_Piston2 OR Q_Piston3;
DatosEstacion.Piston1On := Q_Piston1;
DatosEstacion.Piston2On := Q_Piston2;
DatosEstacion.Piston3On := Q_Piston3;
DatosEstacion.PesoActualKg := DB_HMI.PesoActualKg;
```

---

## `DB_HMI` — DB **3** (único mando del operador)

Crea **todos** estos campos en TIA (mismo layout que el demo). Así el bridge escribe siempre los mismos 6 bytes.

### Byte 0 — comandos de operador (sí se usan en LAD real)

| Offset | Nombre | Tipo | Uso en PLC real |
|---|---|---|---|
| 0.0 | `Start` | Bool | Arranque |
| 0.1 | `Stop` | Bool | Paro |
| 0.2 | `Emergencia` | Bool | Emergencia |
| 0.3 | `ResetAlarma` | Bool | Reset alarma |
| 0.4 | `ModoAuto` | Bool | Modo auto |
| 0.5 | `FinSesion` | Bool | Fin sesión |
| 0.6 | `ManualBanda` | Bool | Manual banda |
| 0.7 | `ManualPiston` | Bool | Manual **P3 aluminio** |

### Byte 1 — bit a bit (no te saltes ninguno)

| Offset | Nombre | Tipo | Uso en PLC real |
|---|---|---|---|
| 1.0 | `BasculaLista` | Bool | **Sim:** báscula · **Real:** ignorar → `I_BasculaLista` |
| 1.1 | `SensorPieza` | Bool | **Sim:** pieza · **Real:** ignorar → `I_SensorPieza` |
| 1.2 | `SensorPlastico` | Bool | **Sim:** plástico · **Real:** ignorar → `I_SensorPlastico` |
| 1.3 | `SensorAluminio` | Bool | **Sim:** aluminio · **Real:** ignorar → `I_SensorAluminio` |
| 1.4 | `Piston1Extendido` | Bool | **Sim:** FC P1 (simple efecto) · **Real:** ignorar → `I_Piston1Extendido` |
| 1.5 | `Piston2Extendido` | Bool | **Sim:** FC P2 · **Real:** ignorar → `I_Piston2Extendido` |
| 1.6 | `ManualPiston1` | Bool | **Sí** — manual **P1 retenedor** |
| 1.7 | `ManualPiston2` | Bool | **Sí** — manual **P2 plástico** |

### Desde offset 2 — peso + FC P3 sim

| Offset | Nombre | Tipo | Uso |
|---|---|---|---|
| 2.0 | `PesoActualKg` | Real | Peso desde HMI |
| 6.0 | `Piston3Extendido` | Bool | **Sim:** FC P3 · **Real:** ignorar → `I_Piston3Extendido` |

Tamaño escritura bridge: **7 bytes**.

¿Por qué 1.0–1.5 y 6.0 si el real no los lee?  
Porque el **mismo DB** lo usa la demo (1511C, solo HMI) para simular sensores. En el 1214C los creas igual (mismo contrato), pero el LAD real lee los `I_*`.

Cilindros **simple efecto**: un sensor de extendido por pistón (sin `*Retractado`).