# Qué hacer AHORA (estás en Create new project)

Haz esto hoy, en este orden. No intentes conectar la web todavía.

---

## En TIA Portal V20 (pantalla Create new project)

1. **Project name:** `Guacamayos_Clasificacion`
2. Click **Create**
3. **Add new device** → Controllers → S7-1200 → **CPU 1214C DC/DC/DC** → Add
4. (Opcional hoy) Add new device → HMI → **KTP700 Basic** → enlázala al PLC
5. Abre `tia/MAPA_IO_Y_DB.md` y crea la tag table + el DB `DatosEstacion` (Optimized OFF)
6. Crea los FC vacíos: `FC_Modos`, `FC_Secuencia`, `FC_Alarmas`, `FC_EspejoWeb`
7. Sigue `tia/LOGICA_LAD.md` red por red
8. **Start simulation** → RUN → prueba Start + una pieza plástica + una de aluminio

Guía completa: `docs/01_GUIA_TIA_PORTAL.md`

---

## En Automation Studio (pantalla de inicio)

1. **New project** → `Guacamayos_ElectroNeumatica`
2. Armar circuito: aire + electroválvula 5/2 + cilindro + 2 sensores de posición
3. Simular: bobina ON → extiende → sensor → bobina OFF → retorna
4. Añadir símbolos de sensor plástico / aluminio / pieza (pulsadores)

Guía completa: `docs/02_GUIA_AUTOMATION_STUDIO.md`

---

## En la app (cuando quieras ver la UI nueva)

1. Abre `index.html` con un servidor local
2. Con Firebase + `serviceAccountKey.json`:
   ```bash
   python plc_simulador.py parque-central
   ```
3. Cuando el PLC ya tenga el DB y NetToPLCSim:
   ```bash
   python plc_bridge.py parque-central --ip 127.0.0.1 --reset-on-start
   ```

Guía: `docs/03_CONEXION_WEB_PLC.md`

---

## Recuerda el diseño físico

```
Báscula → Banda → [Sensor material + Pistón] → Contenedores
                      │
                      ├ plástico: no empuja / va a A
                      └ aluminio: pistón empuja a B
```

Solo **botellas plásticas** y **latas**.
Cualquier persona en la estación abre Guacamayos → **Conectar** → ve el acumulado.
