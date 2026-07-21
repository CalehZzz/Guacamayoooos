# Guía paso a paso — TIA Portal V20 (desde cero)

Estás en **Create new project**. Sigue esto en orden. No necesitas hardware físico: usarás **PLCSIM**.

---

## Parte A — Crear el proyecto y el PLC

### A1. Crear proyecto
1. En la pantalla de inicio: **Create new project**.
2. **Project name:** `Guacamayos_Clasificacion`
3. **Path:** déjalo por defecto o elige una carpeta fácil de encontrar.
4. Click **Create**.

### A2. Agregar el PLC
1. En Project view: **Add new device**.
2. Controllers → **SIMATIC S7-1200** → CPU → **CPU 1214C DC/DC/DC**  
   (si tu laboratorio usa otro modelo S7-1200, elige ese; la lógica es igual).
3. Firmware: el que te aparezca por defecto (ej. V4.5 / V4.6) está bien para simulación.
4. Click **Add**.

### A3. (Recomendado) Agregar HMI
1. Otra vez **Add new device**.
2. HMI → SIMATIC Comfort / Basic → elige una **KTP700 Basic** o similar (lo que tengas licencia).
3. En el asistente, **conecta la HMI al PLC** por PROFINET (deja IP por defecto).
4. Finish.

---

## Parte B — Crear tags (nombres)

1. Project tree → tu PLC → **PLC tags** → **Show all tags** (o Add new tag table `IO_Estacion`).
2. Crea **exactamente** los tags de `tia/MAPA_IO_Y_DB.md` (entradas, salidas y memorias).

Tip: usa nombres con prefijo `I_`, `Q_`, `M_` para no perderte.

---

## Parte C — Crear el Data Block `DatosEstacion`

1. Program blocks → Add new block → **Data block**.
2. Name: `DatosEstacion`.
3. Abre propiedades del DB → **Attributes** → **Optimized block access = OFF**.
4. Inserta los campos del mapa (ContPlastico, ContAluminio, pesos Real, bits de estado, etc.).
5. Compile (Ctrl+B).

---

## Parte D — Programa PLC (bloques)

Vas a crear estos bloques:

| Bloque | Tipo | Función |
|---|---|---|
| `OB1` | Organization block | Llama a los FC en cada ciclo |
| `FC_Modos` | Function | Start/Stop, emergencia, modo manual/auto |
| `FC_Secuencia` | Function | Banda + detección + pistón + conteo |
| `FC_Alarmas` | Function | Alarmas básicas |
| `FC_EspejoWeb` | Function | Copia estados al DB para la app |

### D1. Lógica de modos (`FC_Modos`) — requisitos del reto

**Arranque / paro (latch):**
- Si `I_Start` Y NO `I_Emergencia` Y NO `I_Stop` → set `M_SistemaOn`.
- Si `I_Stop` O `I_Emergencia` → reset `M_SistemaOn`.
- Si emergencia → forzar `Q_Banda=0`, `Q_Piston=0`, `M_Alarma` o flag emergencia.

**Modo:**
- `M_ModoAuto` = valor del selector HMI / `I_ModoAuto`.

### D2. Secuencia automática (`FC_Secuencia`)

Estados sugeridos (puedes hacerlo con bits o un Int `EstadoMaquina`):

0. **IDLE** — sistema off o esperando.
1. **RUNNING** — banda ON mientras sistema ON y modo auto y no emergencia.
2. **PESANDO** — pieza detectada en báscula → espera `I_BasculaLista` → guarda `PesoActualKg`.
3. **CLASIFICANDO** — lee sensores:
   - Plástico → suma contador/peso plástico; pistón OFF.
   - Aluminio → pistón ON hasta `I_PistonExtendido`, luego OFF hasta `I_PistonRetractado`; suma aluminio.
4. **ALARMA** — sensores contradictorios o timeout de pistón (usa **temporizador TON**).

**Contadores:** usa `ContPlastico` / `ContAluminio` del DB (o bloques CTU y luego copia al DB).

**Temporizadores (obligatorio del reto):**
- `TON` tiempo mínimo de banda entre piezas.
- `TON` timeout si el pistón no llega a extendido en X segundos → alarma.

### D3. Modo manual
Si `M_ModoAuto = 0` y `M_SistemaOn = 1`:
- `Q_Banda` = `I_ManualBanda` (o botón HMI).
- `Q_Piston` = `I_ManualPiston` (o botón HMI).
- No ejecutes la secuencia automática.

### D4. Espejo hacia la web (`FC_EspejoWeb`)
Cada ciclo copia:
- `DatosEstacion.SistemaOn` ← `M_SistemaOn`
- `DatosEstacion.ModoAuto` ← `M_ModoAuto`
- `DatosEstacion.Emergencia` ← `I_Emergencia`
- `DatosEstacion.Alarma` ← `M_Alarma`
- `DatosEstacion.BandaOn` ← `Q_Banda`
- `DatosEstacion.PistonOn` ← `Q_Piston`
- `DatosEstacion.EstadoMaquina` ← estado actual
- `DatosEstacion.FinSesion` ← `I_FinSesion` (o botón HMI)

### D5. OB1
En Network 1–4 llama en orden:
1. `FC_Modos`
2. `FC_Secuencia`
3. `FC_Alarmas`
4. `FC_EspejoWeb`

Detalle de redes en lenguaje de contactos: ver `tia/LOGICA_LAD.md`.

---

## Parte E — HMI (requisito del reto)

Crea **2 pantallas**:

### Pantalla 1 — Operación
- Botones: **START**, **STOP**, **E-STOP reset** (si aplica)
- Selector: **Manual / Automático**
- Indicadores: Banda, Pistón, Sistema ON, Emergencia, Alarma
- Contadores: plástico, aluminio
- Pesos acumulados + peso actual
- Botón **Fin de sesión** (escribe `DatosEstacion.FinSesion`)
- Botón **Reset contadores** (solo con sistema en STOP)

### Pantalla 2 — Diagnóstico / Alarmas
- Lista de alarmas (texto):
  - Emergencia activa
  - Timeout pistón
  - Sensores contradictorios
  - Báscula no lista (opcional)

Conecta cada objeto HMI al tag/DB correspondiente (drag & drop desde detalle del PLC).

---

## Parte F — Simular con PLCSIM

1. Selecciona el PLC en el árbol.
2. Toolbar: **Start simulation** (icono de PLC con play)  
   o clic derecho en la CPU → **Start simulation**.
3. Acepta compilar + descargar.
4. En PLCSIM pon la CPU en **RUN**.
5. Abre una **Watch table** / sim table y fuerza:
   - `I_Start` = 1 (pulso)
   - `I_ModoAuto` = 1
   - Luego simula una pieza: `I_BasculaLista`, `I_SensorPieza`, `I_SensorPlastico` o `I_SensorAluminio`
6. Observa `Q_Banda`, `Q_Piston` y los contadores del DB.

Si también tienes HMI: descarga la HMI a **Simulation** (WinCC Runtime Simulation) y opera desde ahí.

---

## Parte G — Dejar el PLC “visible” para Python (snap7)

Para que `plc_bridge.py` lea el DB:

### Opción recomendada en laboratorio: **NetToPLCSim** + PLCSIM
1. Descarga **NetToPLCSim** (herramienta gratuita de la comunidad Siemens).
2. Corre PLCSIM con tu proyecto en RUN.
3. Abre NetToPLCSim como Administrador.
4. Add → selecciona tu PLC simulado → OK.
5. Start server.
6. En TIA: propiedades CPU → Protection & Security → habilita **PUT/GET** communication (permitir acceso desde partners remotos).
7. En el bridge Python usa IP `127.0.0.1`, rack 0, slot 1.

### Si tienes **PLCSIM Advanced**
1. Crea una instancia con IP virtual (ej. `192.168.0.1`).
2. Conecta TIA a esa IP.
3. El bridge apunta a esa misma IP.

Sin NetToPLCSim / PLCSIM Advanced, la app puede seguir funcionando con `plc_simulador.py` (simulación por software) mientras terminas la lógica en TIA.

---

## Checklist del PDF (PLC + HMI)

- [ ] Arranque y paro
- [ ] Paro de emergencia
- [ ] Modo manual
- [ ] Modo automático
- [ ] Temporizadores
- [ ] Contadores
- [ ] Secuencia automática
- [ ] Actuador neumático (pistón)
- [ ] Alarmas básicas
- [ ] HMI: start/stop, modo, sensores/actuadores, contadores, alarmas
