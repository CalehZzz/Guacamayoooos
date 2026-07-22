# Guacamayos — Estación de clasificación + app (Siemens Youth Innovation Search 2026)

App web + puente al PLC Siemens (TIA Portal / PLCSIM) + guías para Automation Studio.

## Empieza aquí

1. [`docs/00_ARQUITECTURA.md`](docs/00_ARQUITECTURA.md) — visión completa del sistema  
2. [`docs/01_GUIA_TIA_PORTAL.md`](docs/01_GUIA_TIA_PORTAL.md) — desde “Create new project”  
3. [`docs/02_GUIA_AUTOMATION_STUDIO.md`](docs/02_GUIA_AUTOMATION_STUDIO.md) — electroneumática  
4. [`docs/03_CONEXION_WEB_PLC.md`](docs/03_CONEXION_WEB_PLC.md) — conectar la página al PLC  
5. [`tia/MAPA_IO_Y_DB.md`](tia/MAPA_IO_Y_DB.md) — tags y DB1  
6. [`tia/LOGICA_LAD.md`](tia/LOGICA_LAD.md) — **orden final de networks LAD** (usa esta para programar)  
7. [`docs/06_COMO_USAR_TON.md`](docs/06_COMO_USAR_TON.md) — TON IEC  
8. [`docs/05_FAQ_TIA.md`](docs/05_FAQ_TIA.md) — dudas frecuentes  

## App

- `index.html` — interfaz para el usuario en la estación (plástico + aluminio en vivo)
- `plc_simulador.py` — genera datos sin PLC (para probar la web)
- `plc_bridge.py` — lee el PLC virtual con snap7 y publica a Firestore
- `index.js` — Cloud Function auxiliar para roles admin

## Demo rápida sin TIA

```bash
pip install firebase-admin
# coloca serviceAccountKey.json en la raíz
# abre index.html en un servidor local, pulsa Conectar
python plc_simulador.py parque-central
```

## Demo con PLC virtual

```bash
pip install firebase-admin python-snap7
# PLCSIM RUN + NetToPLCSim Start Server
python plc_bridge.py parque-central --ip 127.0.0.1 --reset-on-start
```
