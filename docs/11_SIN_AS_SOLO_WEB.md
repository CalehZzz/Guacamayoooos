# Sin Automation Studio — solo Web ↔ TIA (3 pistones)

```
Página SIBU (HMI virtual KTP700 + simulación gráfica)
        ↕ Firestore  (estación elegida)
   plc_bridge.py (snap7)
        ↕
   PLC 1511C (PLCSIM Advanced)
   · M_Banda · M_Piston1 · M_Piston2 · M_Piston3
   · sensores sim en DB_HMI (simple efecto)
```

**Eliminado:** Automation Studio, KEPServer, mapeo `%M2.x` hacia AS.

Networks LAD: `tia/NETWORKS_WEB_ONLY.md` · Tags: `tia/TABLA_TAGS_DESDE_CERO.md`.

---

## Regla única

| Rol | Tags | Quién escribe |
|---|---|---|
| Comandos + sensores simulados | `DB_HMI.*` (DB3, ≥7 bytes) | Web → bridge |
| Lógica / actuadores | `M_SistemaOn`, `M_Banda`, `M_Piston1/2/3`… | PLC |
| Estado a la web | `DatosEstacion` (DB1, 22 bytes) | PLC → bridge → web |

```
  Entrada sim → báscula → banda → P1 retenedor
                                   ├─ plástico → P2
                                   └─ aluminio → P3
```

Cilindros **simple efecto**: 1 sensor `PistonNExtendido` por pistón (en `DB_HMI`).

---

## Cambio en TIA (FC_Secuencia)

| Antes (1 pistón / AS) | Ahora (3 pistones · web) |
|---|---|
| `M_Sensor*` / `I_*` | `DB_HMI.Sensor*` / `BasculaLista` |
| `M_Piston` / `Q_Piston` | `M_Piston1` · `M_Piston2` · `M_Piston3` |
| `M_PistonExtendido` | `DB_HMI.Piston1/2/3Extendido` |
| Un solo TON | `T_RetardoPiston2/3` + `T_TimeoutPiston2/3` |

**No tocar la idea de:** `DB_HMI.Start/Stop/…`, `M_SistemaOn`, `DatosEstacion`.

Después: compilar → Download → RUN.

---

## Controles en la HMI virtual

| Botón HMI | Campos DB_HMI |
|---|---|
| START / STOP / Emergencia | `.Start` `.Stop` `.Emergencia` |
| AUTO | `.ModoAuto` |
| Marcha / Parada banda | `.ManualBanda` (+ modo manual) |
| Extender / Retractar P1–P3 | `.ManualPiston1` / `.ManualPiston2` / `.ManualPiston` |
| Sim plástico / aluminio | Pieza + material + Báscula |
| Sim FC 100% P1/P2/P3 | `.Piston1/2/3Extendido` |
| Peso | `.PesoActualKg` |

Feedback AUTO (solo sim): ~450 ms después de ver el pistón ON en `DatosEstacion`, la web escribe el bit `*Extendido`.

---

## Acceso desde la estación

1. App → elegir estación → **Conectar**
2. En la vista en vivo → **Abrir HMI**
3. La HMI usa `hmi_comandos/{idEstacion}` y `sesiones_activas/{idEstacion}`

---

## Bridge

```powershell
py plc_bridge.py parque-central --ip 192.168.0.1 --db 1 --db-hmi 3
```
