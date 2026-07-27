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
| 2.0* | `PesoActualKg` | **Real** | Peso en kg con decimales (0.04, 0.02…) |

\*En muchos 1511C con Optimized OFF, TIA coloca el Real en **2.0** (justo después de los bools del byte 1).  
Si en **tu** compile sale otro offset, **manda el de TIA** (no el de esta tabla).

Tamaño mínimo del DB: **6 bytes** (bools + Real). El bridge escribe 6 bytes.

Si `plc_probe` dice `DB3: OK hasta 4 bytes`, falta `PesoActualKg` (Real) u otros campos: agrégalos, compila y Download otra vez.

### ¿Por qué Real y no Int?
- El peso es fraccionario: `0.045 kg`, no solo enteros.
- `Real` = punto flotante (32 bit) en el PLC.
- Si usaras `Int`, tendrías que guardar gramos (`45`) y convertir; más lío para báscula/AI.

Firestore: `hmi_comandos/{estacionId}`

En LAD usa `DB_HMI.Start` (etc.) en lugar de `I_` / `M_HMI_`.
