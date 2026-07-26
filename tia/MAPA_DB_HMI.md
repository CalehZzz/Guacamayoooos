# DB_HMI — comandos desde HMI web (CPU 1511C)

Crea un Data Block global **`DB_HMI`**, número sugerido **DB3**, **Optimized access = OFF**.

| Offset | Nombre | Tipo | Control web |
|---|---|---|---|
| 0.0 | `Start` | Bool | START |
| 0.1 | `Stop` | Bool | STOP |
| 0.2 | `Emergencia` | Bool | EMERGENCIA |
| 0.3 | `ResetAlarma` | Bool | Reset alarma |
| 0.4 | `ModoAuto` | Bool | Switch Auto |
| 0.5 | `FinSesion` | Bool | Fin sesión |
| 0.6 | `ManualBanda` | Bool | Banda manual |
| 0.7 | `ManualPiston` | Bool | Pistón manual |
| 1.0 | `BasculaLista` | Bool | Sim báscula |
| 1.1 | `SensorPieza` | Bool | Sim pieza |
| 1.2 | `SensorPlastico` | Bool | Sim plástico |
| 1.3 | `SensorAluminio` | Bool | Sim aluminio |
| 1.4 | `PistonRetractado` | Bool | Sim retractado |
| 1.5 | `PistonExtendido` | Bool | Sim extendido |
| 4.0 | `PesoActualKg` | Real | Peso actual (alineado) |

Tamaño a escribir desde Python: **8 bytes**.

Firestore: `hmi_comandos/{estacionId}`

En LAD usa `DB_HMI.Start` (etc.) en lugar de `I_` / `M_HMI_`.
