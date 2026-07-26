# Tabla maestra de tags — proyecto desde cero (CPU 1511C-1 PN)

Todo lo que debes **crear** en TIA. No asumas que ya existe nada.

**Stack:** TIA V20 · 1511C · PLCSIM Advanced V7 · HMI = **web Guacamayos** (no KTP) · AS 10 + KEPServerEX 6

---

## Cómo está organizado

| Grupo | Para qué |
|---|---|
| **A. Entradas `%I`** | Señales desde Automation Studio / KEPServer (máquina) |
| **B. Salidas `%Q`** | Actuadores hacia AS / KEPServer |
| **C. Memorias `%M`** | Lógica interna del PLC (latches, pulsos) |
| **D. DB_HMI (DB3)** | Comandos de la **HMI web** (botones 🖥️) |
| **E. DatosEstacion (DB1)** | Espejo hacia la web (contadores, estado) |
| **F. Timers** | Instancias TON |

En el LAD: botones de operador leen **`DB_HMI.*`**.  
Sensores/actuadores de proceso leen/escriben **`I_*` / `Q_*`** (AS).  
Si en una prueba no tienes AS, puedes forzar `I_*` en PLCSIM o poner en paralelo `DB_HMI.SensorPieza` etc. (opcional).

---

## A) Entradas digitales (`PLC tags` → Bool)

Direcciones de ejemplo en el DI onboard del 1511C (ajusta si tu wiring/KEPServer usa otras).

| Nombre | Dirección | Tipo | Origen | Descripción |
|---|---|---|---|---|
| `I_SensorPieza` | `%I0.0` | Bool | AS / KEP | Pieza en zona de clasificación |
| `I_SensorPlastico` | `%I0.1` | Bool | AS / KEP | Material = plástico |
| `I_SensorAluminio` | `%I0.2` | Bool | AS / KEP | Material = aluminio |
| `I_BasculaLista` | `%I0.3` | Bool | AS / KEP / lógica | Peso estabilizado |
| `I_PistonRetractado` | `%I0.4` | Bool | AS (sensor 0%) | Cilindro en casa |
| `I_PistonExtendido` | `%I0.5` | Bool | AS (sensor 100%) | Cilindro afuera |

> Start/Stop/Emergencia/Modo **no** van aquí: van en **DB_HMI** (HMI web).

---

## B) Salidas digitales (`PLC tags` → Bool)

| Nombre | Dirección | Tipo | Destino | Descripción |
|---|---|---|---|---|
| `Q_Banda` | `%Q0.0` | Bool | AS / KEP | Marcha banda |
| `Q_Piston` | `%Q0.1` | Bool | AS (solenoide 5/2) | Extender pistón |
| `Q_LamparaRun` | `%Q0.2` | Bool | piloto / web espejo | Sistema en marcha |
| `Q_LamparaAlarma` | `%Q0.3` | Bool | piloto / web | Alarma |
| `Q_LamparaEmergencia` | `%Q0.4` | Bool | piloto / web | Emergencia |

---

## C) Memorias internas (`PLC tags` → Bool)

| Nombre | Dirección | Tipo | Descripción |
|---|---|---|---|
| `M_SistemaOn` | `%M0.0` | Bool | Latch sistema energizado |
| `M_ModoAuto` | `%M0.1` | Bool | Copia modo (o usa solo `DB_HMI.ModoAuto`) |
| `M_Alarma` | `%M0.2` | Bool | Alarma activa |
| `M_Clasificando` | `%M0.3` | Bool | Secuencia aluminio en curso |
| `M_PulsePlastico` | `%M0.4` | Bool | Pulso flanco plástico (resultado P) |
| `M_EdgePlastico` | `%M0.5` | Bool | Memoria de flanco de la bobina P (no usar en otra red) |

---

## D) Data block `DB_HMI` — número **3** · Optimized **OFF**

Comandos de la página (icono 🖥️). El bridge los escribe desde Firestore.

| Nombre en el DB | Tipo | Offset típico* | Botón / control en la web |
|---|---|---|---|
| `Start` | Bool | 0.0 | START |
| `Stop` | Bool | 0.1 | STOP |
| `Emergencia` | Bool | 0.2 | EMERGENCIA |
| `ResetAlarma` | Bool | 0.3 | Reset alarma |
| `ModoAuto` | Bool | 0.4 | Switch Auto/Manual |
| `FinSesion` | Bool | 0.5 | Fin sesión |
| `ManualBanda` | Bool | 0.6 | Banda manual (mantener) |
| `ManualPiston` | Bool | 0.7 | Pistón manual (mantener) |
| `BasculaLista` | Bool | 1.0 | Sim báscula (demo) |
| `SensorPieza` | Bool | 1.1 | Sim pieza (demo) |
| `SensorPlastico` | Bool | 1.2 | Sim plástico (demo) |
| `SensorAluminio` | Bool | 1.3 | Sim aluminio (demo) |
| `PistonRetractado` | Bool | 1.4 | Sim retractado (demo) |
| `PistonExtendido` | Bool | 1.5 | Sim extendido (demo) |
| `PesoActualKg` | **Real** | **2.0** (el que te dio TIA) | Campo peso actual |

\*Confirma offsets en tu compile; si difieren, manda el de TIA.

**En el LAD (operador):** usa `DB_HMI.Start`, `DB_HMI.Stop`, …  
**Sensores de proceso:** preferible `I_SensorPieza` (AS). Para demo sin AS puedes usar `DB_HMI.SensorPieza` **o** ambos en paralelo (OR).

---

## E) Data block `DatosEstacion` — número **1** · Optimized **OFF**

Lo lee el bridge y lo muestra la web (usuario + panel HMI).

| Nombre | Tipo | Offset típico | Descripción |
|---|---|---|---|
| `ContPlastico` | Int | 0.0 | Piezas plástico sesión |
| `ContAluminio` | Int | 2.0 | Piezas aluminio sesión |
| `PesoPlasticoKg` | Real | 4.0 | kg acumulados plástico |
| `PesoAluminioKg` | Real | 8.0 | kg acumulados aluminio |
| `PesoActualKg` | Real | 12.0 | último peso (espejo; también puedes copiar desde DB_HMI) |
| `SesionActiva` | Bool | 16.0 | sesión abierta |
| `FinSesion` | Bool | 16.1 | pedir cierre a la web |
| `SistemaOn` | Bool | 16.2 | espejo marcha |
| `ModoAuto` | Bool | 16.3 | espejo modo |
| `Emergencia` | Bool | 16.4 | espejo emergencia |
| `Alarma` | Bool | 16.5 | espejo alarma |
| `BandaOn` | Bool | 16.6 | espejo `Q_Banda` |
| `PistonOn` | Bool | 16.7 | espejo `Q_Piston` |
| `EstadoMaquina` | Int | 18.0 | 0 idle … 4 emergencia |
| `UltimoMaterial` | Int | 20.0 | 0 ninguno, 1 plástico, 2 aluminio |

Si al compilar un offset sale distinto (como el Real del HMI), **usa el de TIA**.

---

## F) Timers (instancias TON IEC)

No son tags de la tag table clásica: se crean al poner el bloque TON.

| Nombre instancia | Tipo | PT | Uso |
|---|---|---|---|
| `T_RetardoPiston` | TON (IEC) | `T#500ms` | Espera con pistón extendido antes de contar aluminio |
| `T_TimeoutPiston` | TON (IEC) | `T#3s` | Alarma si no llega a extendido |

Contactos: `T_RetardoPiston.Q` · `T_TimeoutPiston.Q`

---

## G) Analógica (opcional, báscula real/sim)

| Nombre | Dirección / tag | Tipo | Nota |
|---|---|---|---|
| `AI_BasculaRaw` | `%IW…` (canal AI del 1511C) | Int/Word | Solo si escalas desde AI |
| o solo | `DB_HMI.PesoActualKg` / `DatosEstacion.PesoActualKg` | Real | Suficiente para demo |

---

## Checklist de creación en TIA (orden)

1. [ ] Tag table: todas las **A + B + C**  
2. [ ] DB **`DatosEstacion`** nº **1**, Optimized OFF, campos **E**  
3. [ ] DB **`DB_HMI`** nº **3**, Optimized OFF, campos **D**  
4. [ ] FCs: `FC_Modos`, `FC_Secuencia`, `FC_Alarmas`, `FC_EspejoWeb` + calls en OB1  
5. [ ] TONs **F** dentro de `FC_Secuencia`  
6. [ ] Compile → offsets OK (`EstadoMaquina` Int ~18, `UltimoMaterial` Int ~20)  
7. [ ] PLCSIM Advanced RUN → `plc_bridge.py --db 1 --db-hmi 3`  
8. [ ] Web 🖥️ manda comandos; 🏠 muestra acumulado  

---

## Redes: de dónde lee cada cosa (resumen)

| Función | Tag(s) |
|---|---|
| START / STOP / E-STOP | `DB_HMI.Start` / `.Stop` / `.Emergencia` |
| Modo auto | `DB_HMI.ModoAuto` (o copia a `M_ModoAuto`) |
| Reset alarma | `DB_HMI.ResetAlarma` |
| Fin sesión | `DB_HMI.FinSesion` → espejo a `DatosEstacion.FinSesion` |
| Banda / pistón salidas | `Q_Banda` / `Q_Piston` |
| Sensores proceso (AS) | `I_Sensor*` / `I_Piston*` / `I_BasculaLista` |
| Sim sensores desde web | `DB_HMI.Sensor*` (demo) |
| Contadores | `DatosEstacion.ContPlastico` / `.ContAluminio` |
| Latch sistema | `M_SistemaOn` |
| Clasificando | `M_Clasificando` |
| Alarma | `M_Alarma` |

Guías de networks: `tia/LOGICA_LAD_SIM.md` (cambia `M_HMI_X` → `DB_HMI.X` al crear desde cero).
