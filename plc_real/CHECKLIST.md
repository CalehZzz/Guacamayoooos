# Checklist — PLC real 1214C + web

## Hardware / TIA
- [ ] Proyecto **nuevo** con CPU 1214C (no el de 1511C)
- [ ] IP estática anotada (ej. `192.168.0.10`)
- [ ] PUT/GET habilitado + download hardware
- [ ] `DatosEstacion` DB1 Optimized OFF
- [ ] `DB_HMI` DB3 Optimized OFF (mín. 6 bytes, `PesoActualKg` Real @ 2.0)
- [ ] Tag table según `TABLA_IO_1214C.md`
- [ ] FCs según `NETWORKS_LAD.md`
- [ ] Download software + CPU RUN
- [ ] Online: forzando `Q_Banda` se oye/ve el contactor

## PC / red
- [ ] PC en la misma subnet que el PLC
- [ ] Firewall permite TCP **102**
- [ ] `serviceAccountKey.json` en la carpeta del bridge
- [ ] `py -m pip install firebase-admin python-snap7`

## Bridge
```powershell
py plc_real/plc_bridge_real.py
# o edita IP dentro del script / pásala así:
py plc_real/plc_bridge_real.py --ip 192.168.0.10
```

Estación Firestore: **`colegio-don-bosco-real`**

## Web
- [ ] Apartado **PLC real** en la app
- [ ] Acceso con Google
- [ ] Conectar a estación real / panel HMI real (sin sim de sensores AS)

## Prueba
1. START desde web → `M_SistemaOn` / `Q_LamparaRun`
2. Pieza + plástico físicos → contador plástico en web
3. Pieza + aluminio → `Q_Piston` → sensor 100% → contador aluminio
4. Emergencia web o seta → paro
