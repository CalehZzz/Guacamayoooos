# Tabla maestra de tags — desde cero (CPU 1511C-1 PN)

> **Modo actual (sin AS):** sensores y comandos van por **`DB_HMI`**.  
> Guía: `docs/11_SIN_AS_SOLO_WEB.md` · Networks: `tia/NETWORKS_WEB_ONLY.md`.

HMI web SIBU → **`DB_HMI`** (vía bridge).  
Espejo a la web → **`DatosEstacion`**.

---

## Grupos (modo web-only)

| Grupo | Área | Uso |
|---|---|---|
| **B. Lógica interna** | `%M` | `M_SistemaOn`, `M_Banda`, `M_Piston`, alarmas… |
| **C. DB_HMI (DB3)** | DB | Comandos + **sensores simulados** desde la web |
| **D. DatosEstacion (DB1)** | DB | Contadores / estado → web |
| **E. Timers** | TON IEC | Retardo y timeout pistón |

~~Grupo A (AS/KEP `%M2.x`)~~ — **no necesario** si no usas Automation Studio.

---

## A) Tags de proceso — AS / KEPServer (`%M` Bool)

Créalos en la **PLC tag table**. En KEPServer mapea **los mismos nombres / direcciones**.

### Sensores (AS → PLC)

| Nombre | Dirección | Tipo | En Automation Studio |
|---|---|---|---|
| `M_SensorPieza` | `%M2.0` | Bool | Pieza en estación |
| `M_SensorPlastico` | `%M2.1` | Bool | Sensor / pulsador plástico |
| `M_SensorAluminio` | `%M2.2` | Bool | Sensor / pulsador aluminio |
| `M_BasculaLista` | `%M2.3` | Bool | Báscula lista |
| `M_PistonRetractado` | `%M2.4` | Bool | Ref. sensor 0% |
| `M_PistonExtendido` | `%M2.5` | Bool | Ref. sensor 100% |

### Actuadores (PLC → AS)

| Nombre | Dirección | Tipo | En Automation Studio |
|---|---|---|---|
| `M_Banda` | `%M3.0` | Bool | Motor / marcha banda |
| `M_Piston` | `%M3.1` | Bool | Solenoide válvula 5/2 |
| `M_LamparaRun` | `%M3.2` | Bool | Piloto run (opcional en AS) |
| `M_LamparaAlarma` | `%M3.3` | Bool | Piloto alarma |
| `M_LamparaEmergencia` | `%M3.4` | Bool | Piloto emergencia |

> En el LAD, donde antes decía `Q_Banda` / `Q_Piston`, usa **`M_Banda` / `M_Piston`**.  
> KEPServer lee esas M y las refleja en AS.

---

## B) Lógica interna PLC (`%M` Bool) — no mapear a AS

| Nombre | Dirección | Tipo | Descripción |
|---|---|---|---|
| `M_SistemaOn` | `%M0.0` | Bool | Latch sistema ON |
| `M_ModoAuto` | `%M0.1` | Bool | Modo auto (copia de DB_HMI o directo) |
| `M_Alarma` | `%M0.2` | Bool | Alarma activa |
| `M_Clasificando` | `%M0.3` | Bool | Secuencia aluminio |
| `M_PulsePlastico` | `%M0.4` | Bool | Resultado flanco P |
| `M_EdgePlastico` | `%M0.5` | Bool | Memoria flanco P (solo del TON/P) |

---

## C) `DB_HMI` — número **3** · Optimized **OFF**

Solo HMI web (no KTP). Bridge: Firestore `hmi_comandos` → este DB.

| Nombre | Tipo | Offset típico | Control web 🖥️ |
|---|---|---|---|
| `Start` | Bool | 0.0 | START |
| `Stop` | Bool | 0.1 | STOP |
| `Emergencia` | Bool | 0.2 | EMERGENCIA |
| `ResetAlarma` | Bool | 0.3 | Reset alarma |
| `ModoAuto` | Bool | 0.4 | Switch Auto |
| `FinSesion` | Bool | 0.5 | Fin sesión |
| `ManualBanda` | Bool | 0.6 | Banda manual |
| `ManualPiston` | Bool | 0.7 | Pistón manual |
| `BasculaLista` | Bool | 1.0 | Sim báscula (demo sin AS) |
| `SensorPieza` | Bool | 1.1 | Sim pieza |
| `SensorPlastico` | Bool | 1.2 | Sim plástico |
| `SensorAluminio` | Bool | 1.3 | Sim aluminio |
| `PistonRetractado` | Bool | 1.4 | Sim retractado |
| `PistonExtendido` | Bool | 1.5 | Sim extendido |
| `PesoActualKg` | Real | **2.0** (tu compile) | Peso actual kg |

### LAD: operador vs proceso

| Función | Leer |
|---|---|
| START / STOP / Emergencia | `DB_HMI.Start` / `.Stop` / `.Emergencia` |
| Modo | `DB_HMI.ModoAuto` |
| Sensores con AS corriendo | `M_SensorPieza`, `M_SensorPlastico`, … |
| Sensores solo demo web | `DB_HMI.SensorPieza` **o** OR con `M_Sensor…` |
| Banda / pistón salida | bobina **`M_Banda`** / **`M_Piston`** |

Ejemplo OR (AS o web):
```
---| M_SensorPieza |----+----(
---| DB_HMI.SensorPieza |--+
```

---

## D) `DatosEstacion` — número **1** · Optimized **OFF**

| Nombre | Tipo | Offset típico | Descripción |
|---|---|---|---|
| `ContPlastico` | Int | 0.0 | Piezas plástico |
| `ContAluminio` | Int | 2.0 | Piezas aluminio |
| `PesoPlasticoKg` | Real | 4.0 | kg plástico |
| `PesoAluminioKg` | Real | 8.0 | kg aluminio |
| `PesoActualKg` | Real | 12.0 | último peso |
| `SesionActiva` | Bool | 16.0 | sesión abierta |
| `FinSesion` | Bool | 16.1 | fin → web |
| `SistemaOn` | Bool | 16.2 | espejo |
| `ModoAuto` | Bool | 16.3 | espejo |
| `Emergencia` | Bool | 16.4 | espejo |
| `Alarma` | Bool | 16.5 | espejo |
| `BandaOn` | Bool | 16.6 | espejo `M_Banda` |
| `PistonOn` | Bool | 16.7 | espejo `M_Piston` |
| `EstadoMaquina` | Int | 18.0 | 0…4 |
| `UltimoMaterial` | Int | 20.0 | 0/1/2 |

En `FC_EspejoWeb`:  
`DatosEstacion.BandaOn := M_Banda;` · `DatosEstacion.PistonOn := M_Piston;`

---

## E) Timers

| Instancia | PT | Uso |
|---|---|---|
| `T_RetardoPiston` | `T#500ms` | Contar aluminio tras extendido |
| `T_TimeoutPiston` | `T#3s` | Alarma timeout |

---

## Mapa mental

```
AS 10  ←—— M_Sensor* / M_Banda / M_Piston ——→  KEPServerEX 6  ←→  PLC 1511C
                                                      ↑
                                              DB_HMI (HMI web)
                                              DatosEstacion (web estado)
```

---

## Checklist creación

1. [ ] Tag table: grupo **A** (AS/KEP) + grupo **B** (interna)  
2. [ ] `DatosEstacion` DB1 Optimized OFF  
3. [ ] `DB_HMI` DB3 Optimized OFF  
4. [ ] En KEPServer: mismos `%M2.x` / `%M3.x`  
5. [ ] LAD: salidas a `M_Banda` / `M_Piston` (no Q)  
6. [ ] TONs + FCs + OB1  
7. [ ] Bridge `--db 1 --db-hmi 3`

---

## Reemplazo rápido en networks

| Antes (guías viejas) | Ahora |
|---|---|
| `Q_Banda` | `M_Banda` |
| `Q_Piston` | `M_Piston` |
| `Q_LamparaRun` | `M_LamparaRun` |
| `Q_LamparaAlarma` | `M_LamparaAlarma` |
| `Q_LamparaEmergencia` | `M_LamparaEmergencia` |
| `I_SensorPieza` | `M_SensorPieza` |
| `I_SensorPlastico` | `M_SensorPlastico` |
| `I_SensorAluminio` | `M_SensorAluminio` |
| `I_BasculaLista` | `M_BasculaLista` |
| `I_PistonRetractado` | `M_PistonRetractado` |
| `I_PistonExtendido` | `M_PistonExtendido` |
| `M_HMI_Start` / botones | `DB_HMI.Start` … |
