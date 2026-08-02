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

Comandos desde la web. En PLC real **no** uses los bits de sim sensor (1.0–1.5) como fuente de proceso: los sensores son `I_*`.

| Offset | Nombre | Tipo | Uso real |
|---|---|---|---|
| 0.0 | `Start` | Bool | Arranque |
| 0.1 | `Stop` | Bool | Paro |
| 0.2 | `Emergencia` | Bool | Emergencia |
| 0.3 | `ResetAlarma` | Bool | Reset alarma |
| 0.4 | `ModoAuto` | Bool | Modo auto |
| 0.5 | `FinSesion` | Bool | Fin sesión |
| 0.6 | `ManualBanda` | Bool | Manual banda |
| 0.7 | `ManualPiston` | Bool | Manual **P3 aluminio** |
| 1.0–1.5 | `BasculaLista`…`PistonExtendido` | Bool | **No usar en LAD real** (solo demo) |
| 1.6 | `ManualPiston1` | Bool | Manual **P1 retenedor** |
| 1.7 | `ManualPiston2` | Bool | Manual **P2 plástico** |
| 2.0 | `PesoActualKg` | Real | Peso desde HMI / báscula→PC→web |

Tamaño escritura bridge: **6 bytes**.
