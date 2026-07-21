# Conexión App Web ↔ PLC virtual

## Idea en una frase

La app **no habla con el PLC directo**. Un script Python en tu PC lee el PLC (PLCSIM) y publica los datos en Firestore; la página solo escucha.

```
PLCSIM (TIA)  --snap7-->  plc_bridge.py  --Firebase-->  index.html (usuarios)
```

Si aún no tienes NetToPLCSim / PLCSIM Advanced, usa `plc_simulador.py` para desarrollar la web mientras programas el PLC.

---

## Archivos

| Archivo | Para qué |
|---|---|
| `index.html` | App Guacamayos (usuarios en la estación) |
| `plc_bridge.py` | Lee DB1 real del PLC vía snap7 y publica a Firestore |
| `plc_simulador.py` | Igual que el bridge pero genera datos falsos (sin PLC) |
| `tia/MAPA_IO_Y_DB.md` | Offsets del DB que el bridge espera |

---

## Paso 1 — Firebase (si aún no)

1. Proyecto Firebase `guacamayos-...` (ya está referenciado en `index.html`).
2. Auth email/Google habilitado.
3. Firestore en modo prueba o con reglas que permitan lecturas/escrituras de sesiones.
4. Cuenta de servicio: Consola → Project settings → Service accounts → Generate new private key.
5. Guarda el JSON como `serviceAccountKey.json` **en la carpeta del repo** (no lo subas a git).

---

## Paso 2 — Probar la web SIN PLC

```bash
pip install firebase-admin
# Abre index.html con Live Server / GitHub Pages / cualquier servidor local
# En la app: Conectar a una estación
python plc_simulador.py parque-central
```

Deberías ver subir plástico/aluminio en vivo.

---

## Paso 3 — Conectar al PLC virtual

### 3.1 En TIA
- DB `DatosEstacion` con **Optimized access OFF**
- CPU Protection: permitir **PUT/GET**
- Programa descargado en PLCSIM en **RUN**
- Contadores y bits espejo funcionando (ver guía TIA)

### 3.2 NetToPLCSim
1. Ejecutar como Administrador
2. Add → tu PLC simulado
3. Start Server
4. IP local típica para el bridge: `127.0.0.1`

### 3.3 Bridge real

```bash
pip install firebase-admin python-snap7
python plc_bridge.py parque-central --ip 127.0.0.1 --rack 0 --slot 1 --db 1
```

Opciones útiles:
```bash
python plc_bridge.py parque-central --ip 127.0.0.1 --dry-run
# dry-run: solo imprime lo leído, no escribe Firebase
```

---

## Paso 4 — Flujo de usuario en la estación

1. Operador pone el sistema en AUTO desde la **HMI** (TIA).
2. Visitante abre **Guacamayos** en el celular.
3. Pulsa **Conectar** en la estación.
4. La web crea `sesiones_activas/{id}` en ceros.
5. El bridge detecta sesión y empieza a publicar lecturas del PLC.
6. Cada botella/lata clasificada aumenta piezas/kg/$ en la web.
7. Al terminar: botón web **Finalizar**, o botón HMI/físico **Fin sesión** (`FinSesion=1`).
8. La web guarda el registro (si hay cuenta) y muestra el resumen.

---

## Paso 5 — Qué mirar en la UI nueva

En la vista en vivo verás un panel **Estado PLC**:
- Conectado / Desconectado
- Sistema ON
- Modo Auto/Manual
- Banda / Pistón
- Emergencia / Alarma
- Último material detectado

Eso es tu evidencia de innovación: supervisión remota tipo HMI + experiencia de usuario.

---

## Problemas frecuentes

| Síntoma | Qué revisar |
|---|---|
| `snap7` no conecta | NetToPLCSim corriendo, PLCSIM en RUN, IP/rack/slot |
| Lee ceros siempre | DB number, Optimized OFF, offsets, PUT/GET |
| Web no actualiza | Estación iniciada antes del bridge, Firebase rules, `serviceAccountKey.json` |
| Contadores no bajan al reconectar | El PLC debe resetear contadores al iniciar sesión (HMI Reset o bit desde bridge) |

### Reset de sesión (recomendación)
Cuando la web inicia sesión, el bridge puede escribir en el DB:
- `ContPlastico=0`, `ContAluminio=0`, pesos=0, `FinSesion=0`, `SesionActiva=1`

`plc_bridge.py` ya intenta ese reset al arrancar si usas `--reset-on-start`.

---

## Qué decir en la presentación (innovación)

> “Además de la HMI industrial, cualquier persona en la estación se conecta con su teléfono a Guacamayos, ve el pesaje y la clasificación en tiempo real leídos del PLC Siemens, y guarda su historial de reciclaje.”
