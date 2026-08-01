# I/O y tags — CPU 1214C AC/DC/Rly (3 pistones)

Ajusta direcciones si tu MLFB tiene otro mapa; los **nombres** deben coincidir con el LAD.

La 1214C típica trae **14 DI** y **10 DQ** relé: alcanza para banda + **3 cilindros** + lámparas.

---

## Idea mecánica (PLC real)

| Pistón | Tag salida | Rol |
|---|---|---|
| **1** | `Q_Piston1` | **Retenedor / tope** — sujeta la pieza mientras se pesa / clasifica |
| **2** | `Q_Piston2` | **Empuje plástico** → contenedor A |
| **3** | `Q_Piston3` | **Empuje aluminio** → contenedor B |

Cada cilindro: válvula 5/2 + sensor **0%** (retractado) + sensor **100%** (extendido).

```
  [Entrada] → [Báscula] → [Banda] → [P1 retenedor + sensores]
                                      ├─ plástico  → P2 → contenedor A
                                      └─ aluminio  → P3 → contenedor B
```

---

## A) Entradas digitales `%I` (proceso físico)

| Dirección | Nombre | Tipo | Hardware sugerido |
|---|---|---|---|
| `%I0.0` | `I_Start` | Bool | Pulsador NO arranque (opcional si solo usas web) |
| `%I0.1` | `I_Stop` | Bool | Pulsador paro |
| `%I0.2` | `I_Emergencia` | Bool | Seta emergencia (1 = activo) |
| `%I0.3` | `I_ModoAuto` | Bool | Selector auto (opcional; web también escribe modo) |
| `%I0.4` | `I_SensorPieza` | Bool | Pieza en estación |
| `%I0.5` | `I_SensorPlastico` | Bool | Sensor / botón material plástico |
| `%I0.6` | `I_SensorAluminio` | Bool | Sensor / botón material aluminio |
| `%I0.7` | `I_BasculaLista` | Bool | Báscula estable / lista |
| `%I1.0` | `I_Piston1Retractado` | Bool | P1 retenedor @ 0% |
| `%I1.1` | `I_Piston1Extendido` | Bool | P1 retenedor @ 100% |
| `%I1.2` | `I_Piston2Retractado` | Bool | P2 plástico @ 0% |
| `%I1.3` | `I_Piston2Extendido` | Bool | P2 plástico @ 100% |
| `%I1.4` | `I_Piston3Retractado` | Bool | P3 aluminio @ 0% |
| `%I1.5` | `I_Piston3Extendido` | Bool | P3 aluminio @ 100% |

> Manual banda / pistones / reset alarma: solo por **`DB_HMI`** (web). Así caben los 6 finales de carrera en los 14 DI.

Si más adelante amplías DI (módulo extra), puedes cablear `I_ManualBanda`, `I_ManualPiston1..3`, `I_ResetAlarma` y ORearlos en el LAD como en la versión de 1 pistón.

---

## B) Salidas digitales `%Q` (relé)

| Dirección | Nombre | Tipo | Hardware |
|---|---|---|---|
| `%Q0.0` | `Q_Banda` | Bool | Contactor / motor banda |
| `%Q0.1` | `Q_Piston1` | Bool | Solenoide válvula 5/2 — retenedor |
| `%Q0.2` | `Q_Piston2` | Bool | Solenoide válvula 5/2 — plástico |
| `%Q0.3` | `Q_Piston3` | Bool | Solenoide válvula 5/2 — aluminio |
| `%Q0.4` | `Q_LamparaRun` | Bool | Piloto verde |
| `%Q0.5` | `Q_LamparaAlarma` | Bool | Piloto rojo |
| `%Q0.6` | `Q_LamparaEmergencia` | Bool | Piloto amarillo |

> En CPU **Rly**, las Q son contactos secos: alimenta la carga con 24 V / 120-230 V según diseño eléctrico (respetar límites del relé).

---

## C) Memorias internas `%M` (solo PLC)

| Dirección | Nombre | Uso |
|---|---|---|
| `%M0.0` | `M_SistemaOn` | Latch sistema |
| `%M0.1` | `M_ModoAuto` | Modo auto efectivo |
| `%M0.2` | `M_Alarma` | Alarma |
| `%M0.3` | `M_ClasifPlastico` | Secuencia empuje plástico (P2) |
| `%M0.4` | `M_ClasifAluminio` | Secuencia empuje aluminio (P3) |
| `%M0.5` | `M_PulsePlastico` | Pulso flanco (opcional; el conteo va al fin de P2) |
| `%M0.6` | `M_EdgePlastico` | Memoria bobina P (si usas pulso) |
| `%M0.7` | `M_Clasificando` | OR de clasificaciones (para banda / espejo) |

`M_Clasificando := M_ClasifPlastico OR M_ClasifAluminio` (network o SCL).

---

## D) Data blocks (contrato web)

Ver `DB_CONTRATO_WEB.md`.

| DB | Número | Optimized |
|---|---|---|
| `DatosEstacion` | 1 | OFF |
| `DB_HMI` | 3 | OFF |

---

## E) Timers IEC

| Instancia | PT | Uso |
|---|---|---|
| `T_RetardoPiston2` | `T#500ms` | Plástico: espera con P2 extendido antes de contar |
| `T_RetardoPiston3` | `T#500ms` | Aluminio: espera con P3 extendido antes de contar |
| `T_TimeoutPiston2` | `T#3s` | Alarma si P2 no llega a 100% |
| `T_TimeoutPiston3` | `T#3s` | Alarma si P3 no llega a 100% |

---

## F) Quién manda qué

| Señal | Origen preferido |
|---|---|
| Sensores pieza/material/pistones | **`I_*` físicos** |
| Banda / 3 pistones / lámparas | **`Q_*`** |
| START / STOP / modo / manual desde jurado (web) | **`DB_HMI.*`** |
| Contadores a la web | **`DatosEstacion`** |

En LAD, operador web y físico se pueden **OR**-ear (ej. Start web O `I_Start`).
