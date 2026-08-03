# Sin AS — solo Web ↔ TIA (plástico / latas / vidrio)

```
Estación (app) → Abrir HMI
        ↕ Firestore
   plc_bridge.py
        ↕
   PLC 1511C (PLCSIM) · M_Piston1/2/3
```

| Pistón | Material |
|---|---|
| P1 | Plástico |
| P2 | Latas (aluminio) |
| P3 | Vidrio |

Tags: `tia/TABLA_TAGS_DESDE_CERO.md` · Networks: `tia/NETWORKS_WEB_ONLY.md` · DB: `tia/MAPA_DB_HMI.md`

HMI **solo** desde la vista de estación (no hay icono en la barra superior).

Bridge:
```powershell
py plc_bridge.py parque-central --ip 192.168.0.1 --db 1 --db-hmi 3
```
