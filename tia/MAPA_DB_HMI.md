# DB_HMI — comandos desde HMI web (sim 1511C · 3 pistones)

Crea un Data Block global **`DB_HMI`**, número sugerido **DB3**, **Optimized access = OFF**.

Mismo contrato que el PLC real (`plc_real/DB_CONTRATO_WEB.md`).  
En **simulación** (solo HMI virtual) los sensores de proceso también viven aquí; en el 1214C real esos bits 1.0–1.5 / 6.0 se ignoran y se leen `I_*`.

---

## Layout (Optimized OFF)

| Offset | Nombre | Tipo | Control web 🖥️ |
|---|---|---|---|
| 0.0 | `Start` | Bool | START |
| 0.1 | `Stop` | Bool | STOP |
| 0.2 | `Emergencia` | Bool | EMERGENCIA |
| 0.3 | `ResetAlarma` | Bool | Reset alarma |
| 0.4 | `ModoAuto` | Bool | Switch Auto |
| 0.5 | `FinSesion` | Bool | Fin sesión |
| 0.6 | `ManualBanda` | Bool | Banda manual |
| 0.7 | `ManualPiston` | Bool | Manual **P3 aluminio** |
| 1.0 | `BasculaLista` | Bool | Sim báscula |
| 1.1 | `SensorPieza` | Bool | Sim pieza |
| 1.2 | `SensorPlastico` | Bool | Sim plástico |
| 1.3 | `SensorAluminio` | Bool | Sim aluminio |
| 1.4 | `Piston1Extendido` | Bool | Sim final de carrera **P1** (simple efecto) |
| 1.5 | `Piston2Extendido` | Bool | Sim final de carrera **P2** |
| 1.6 | `ManualPiston1` | Bool | Manual **P1 retenedor** |
| 1.7 | `ManualPiston2` | Bool | Manual **P2 plástico** |
| 2.0 | `PesoActualKg` | **Real** | Peso kg (0.04, 0.02…) |
| 6.0 | `Piston3Extendido` | Bool | Sim final de carrera **P3** |

Tamaño mínimo del DB: **7 bytes** (bools + Real + `Piston3Extendido`). El bridge escribe 7 bytes.

> Cilindros de **simple efecto**: un solo sensor por pistón (`*Extendido`).  
> `1` = extendido · `0` = retractado / en camino (el resorte mete el vástago al apagar la Q/`M_PistonN`).

### ¿Por qué Real y no Int?
- El peso es fraccionario: `0.045 kg`.
- `Real` = IEEE float 32 bit en el PLC.

Firestore: `hmi_comandos/{estacionId}`

En LAD (sim web-only) usa `DB_HMI.Start`, `DB_HMI.Piston2Extendido`, etc.
