# Contrato web — mismos offsets que el demo

Para que `plc_bridge.py` / `plc_bridge_real.py` funcionen sin cambios de offsets.

**Optimized block access = OFF** en ambos DB.

---

## `DatosEstacion` — DB **1**

| Offset | Nombre | Tipo |
|---|---|---|
| 0.0 | `ContPlastico` | Int |
| 2.0 | `ContAluminio` | Int |
| 4.0 | `PesoPlasticoKg` | Real |
| 8.0 | `PesoAluminioKg` | Real |
| 12.0 | `PesoActualKg` | Real |
| 16.0 | `SesionActiva` | Bool |
| 16.1 | `FinSesion` | Bool |
| 16.2 | `SistemaOn` | Bool |
| 16.3 | `ModoAuto` | Bool |
| 16.4 | `Emergencia` | Bool |
| 16.5 | `Alarma` | Bool |
| 16.6 | `BandaOn` | Bool |
| 16.7 | `PistonOn` | Bool |
| 18.0 | `EstadoMaquina` | Int |
| 20.0 | `UltimoMaterial` | Int |

Tamaño legible bridge: **22 bytes**.

En `FC_EspejoWeb`:
```scl
DatosEstacion.BandaOn  := Q_Banda;
DatosEstacion.PistonOn := Q_Piston;
DatosEstacion.PesoActualKg := DB_HMI.PesoActualKg;
```

---

## `DB_HMI` — DB **3**

Comandos desde la web (jurado / operador remoto).  
En PLC real **no** uses los bits de sim sensor como fuente principal (los sensores son `I_*`).

| Offset | Nombre | Tipo | Uso real |
|---|---|---|---|
| 0.0 | `Start` | Bool | Arranque remoto |
| 0.1 | `Stop` | Bool | Paro remoto |
| 0.2 | `Emergencia` | Bool | Emergencia remota |
| 0.3 | `ResetAlarma` | Bool | Reset remoto |
| 0.4 | `ModoAuto` | Bool | Modo |
| 0.5 | `FinSesion` | Bool | Fin sesión web |
| 0.6 | `ManualBanda` | Bool | Manual remoto |
| 0.7 | `ManualPiston` | Bool | Manual remoto |
| 1.0–1.5 | `BasculaLista`…`PistonExtendido` | Bool | **Reservados / no usar en LAD real** (solo demo) |
| 2.0 | `PesoActualKg` | Real | Peso (HMI o báscula→PC→web) |

Tamaño escritura bridge: **6 bytes**.
