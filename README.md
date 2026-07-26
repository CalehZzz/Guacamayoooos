# Guacamayos — Estación de clasificación + app (Siemens Youth Innovation Search 2026)

App web + puente al PLC Siemens (TIA Portal / PLCSIM) + guías para Automation Studio.

## Empieza aquí (stack actual)

**Lee primero:** [`docs/10_ARQUITECTURA_FINAL.md`](docs/10_ARQUITECTURA_FINAL.md)  
TIA V20 · CPU **1511C-1 PN** · PLCSIM Advanced **V7** · AS **10** · KEPServerEX **6** · HMI virtual en la web.

1. [`docs/10_ARQUITECTURA_FINAL.md`](docs/10_ARQUITECTURA_FINAL.md) — diagramas finales + recomendación HMI web  
2. [`tia/TABLA_TAGS_DESDE_CERO.md`](tia/TABLA_TAGS_DESDE_CERO.md) — **todas las tags a crear (desde cero)**  
3. [`tia/MAPA_DB_HMI.md`](tia/MAPA_DB_HMI.md) — DB de comandos desde la web  
4. [`tia/MAPA_IO_Y_DB.md`](tia/MAPA_IO_Y_DB.md) — DatosEstacion  
5. [`tia/LOGICA_LAD_SIM.md`](tia/LOGICA_LAD_SIM.md) — networks (`DB_HMI.*`)  
5. [`automation_studio/COMPONENTES.md`](automation_studio/COMPONENTES.md) — AS 10  
6. Resto de guías en [`docs/`](docs/)  

### Bridge con PLCSIM Advanced

```bash
pip install firebase-admin python-snap7
python plc_bridge.py parque-central --ip 192.168.0.1 --db 1 --db-hmi 3
```

En la app: icono **🖥️** = HMI virtual (operador). **🏠** = usuario que acumula reciclaje.

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
