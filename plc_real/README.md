# SIBU — PLC real (S7-1200 CPU 1214C AC/DC/Rly · 3 pistones)

Proyecto **aparte** del de simulación (1511C + PLCSIM).  
No reutilices el hardware config del 1511C: crea un proyecto TIA nuevo con CPU **1214C**.

**Actuadores neumáticos (real):** 3 cilindros — P1 retenedor · P2 plástico · P3 aluminio.

```
Página SIBU (apartado PLC real)
        ↕ Firestore  (estación: colegio-don-bosco-real)
   plc_bridge.py / plc_bridge_real.py
        ↕ snap7  (IP del 1214C en la red)
   CPU 1214C AC/DC/Rly  + I/O físicos (banda + 3 pistones)
```

| Modo | Carpeta | CPU | Sensores / actuadores |
|---|---|---|---|
| Demo / sim | `tia/` + HMI 🖥️ | 1511C PLCSIM | 1 pistón simulado (`DB_HMI`) |
| **PLC real** | **`plc_real/`** | **1214C** | **3 pistones** `%I`/`%Q` + HMI web |

---

## Archivos

| Archivo | Contenido |
|---|---|
| `00_PROYECTO_TIA.md` | Crear proyecto desde cero en TIA V20 |
| `TABLA_IO_1214C.md` | Asignación `%I` / `%Q` / `%M` / DBs |
| `NETWORKS_LAD.md` | Networks FC (bloques) |
| `DB_CONTRATO_WEB.md` | `DatosEstacion` + `DB_HMI` (mismo contrato web) |
| `plc_bridge_real.py` | Bridge con defaults para PLC real |
| `CHECKLIST.md` | PUT/GET, red, prueba |

---

## Bridge (desde esta carpeta o la raíz)

```powershell
py plc_real/plc_bridge_real.py
```

o:

```powershell
py plc_bridge.py colegio-don-bosco-real --ip 192.168.0.10 --db 1 --db-hmi 3
```

Sustituye `192.168.0.10` por la IP del 1214C.
