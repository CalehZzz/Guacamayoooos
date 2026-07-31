# Sin Automation Studio — solo Web ↔ TIA

```
Página SIBU (HMI + simulación gráfica)
        ↕ Firestore
   plc_bridge.py (snap7)
        ↕
   PLC 1511C (PLCSIM Advanced)
```

**Eliminado:** Automation Studio, KEPServer, mapeo `%M2.x` hacia AS.

Networks LAD detalladas: `tia/NETWORKS_WEB_ONLY.md`.

---

## Regla única

| Rol | Tags | Quién escribe |
|---|---|---|
| Comandos + sensores simulados | `DB_HMI.*` (DB3) | Web → bridge |
| Lógica / actuadores internos | `M_SistemaOn`, `M_Banda`, `M_Piston`… | PLC |
| Estado a la web | `DatosEstacion` (DB1) | PLC → bridge → web |

---

## Cambio obligatorio en TIA (FC_Secuencia)

Sustituye contactos:

| Antes (AS) | Ahora (web) |
|---|---|
| `M_SensorPieza` | `DB_HMI.SensorPieza` |
| `M_SensorPlastico` | `DB_HMI.SensorPlastico` |
| `M_SensorAluminio` | `DB_HMI.SensorAluminio` |
| `M_BasculaLista` | `DB_HMI.BasculaLista` |
| `M_PistonExtendido` | `DB_HMI.PistonExtendido` |
| `M_PistonRetractado` | `DB_HMI.PistonRetractado` |

**No tocar:** `DB_HMI.Start/Stop/…`, `M_SistemaOn`, `M_Banda`, `M_Piston`, `DatosEstacion`, timers.

Después: compilar → Download → RUN.

---

## Tags que puedes dejar de usar

`M_SensorPieza`, `M_SensorPlastico`, `M_SensorAluminio`, `M_BasculaLista`,  
`M_PistonRetractado`, `M_PistonExtendido` (versión `%M`) — ya no hacen falta sin AS.

Sigue usando **`M_Banda`** y **`M_Piston`** (internos; la web los anima vía `DatosEstacion`).

---

## Controles en la web (DB_HMI)

| Botón HMI | Campos |
|---|---|
| START / STOP / Emergencia | `.Start` `.Stop` `.Emergencia` |
| AUTO | `.ModoAuto` |
| Sim plástico | Pieza + Plástico + Báscula |
| Sim aluminio | Pieza + Aluminio + Báscula |
| Pistón 100% | `.PistonExtendido=1` |
| Limpiar | sensores sim = 0 |
| Manual banda/pistón | `.ManualBanda` / `.ManualPiston` |
| Peso | `.PesoActualKg` |

---

## Bridge (igual)

```powershell
py plc_bridge.py parque-central --ip 192.168.0.1 --db 1 --db-hmi 3
```
