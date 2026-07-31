# I/O y tags — CPU 1214C AC/DC/Rly

Ajusta direcciones si tu MLFB tiene otro mapa; los **nombres** deben coincidir con el LAD.

La 1214C típica trae DI suficientes para esta tabla y DQ relé para banda/pistón/lámparas.

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
| `%I1.0` | `I_PistonRetractado` | Bool | Final de carrera 0% |
| `%I1.1` | `I_PistonExtendido` | Bool | Final de carrera 100% |
| `%I1.2` | `I_ManualBanda` | Bool | Pedido banda en manual |
| `%I1.3` | `I_ManualPiston` | Bool | Pedido pistón en manual |
| `%I1.4` | `I_ResetAlarma` | Bool | Reset alarma físico (opcional) |

---

## B) Salidas digitales `%Q` (relé)

| Dirección | Nombre | Tipo | Hardware |
|---|---|---|---|
| `%Q0.0` | `Q_Banda` | Bool | Contactor / motor banda |
| `%Q0.1` | `Q_Piston` | Bool | Solenoide válvula 5/2 |
| `%Q0.2` | `Q_LamparaRun` | Bool | Piloto verde |
| `%Q0.3` | `Q_LamparaAlarma` | Bool | Piloto rojo |
| `%Q0.4` | `Q_LamparaEmergencia` | Bool | Piloto amarillo |

> En CPU **Rly**, las Q son contactos secos: alimenta la carga con 24 V / 120-230 V según diseño eléctrico (respetar límites del relé).

---

## C) Memorias internas `%M` (solo PLC)

| Dirección | Nombre | Uso |
|---|---|---|
| `%M0.0` | `M_SistemaOn` | Latch sistema |
| `%M0.1` | `M_ModoAuto` | Modo auto efectivo |
| `%M0.2` | `M_Alarma` | Alarma |
| `%M0.3` | `M_Clasificando` | Secuencia aluminio |
| `%M0.4` | `M_PulsePlastico` | Pulso flanco plástico |
| `%M0.5` | `M_EdgePlastico` | Memoria bobina P |

---

## D) Data blocks (contrato web — iguales al demo)

Ver `DB_CONTRATO_WEB.md`.

| DB | Número | Optimized |
|---|---|---|
| `DatosEstacion` | 1 | OFF |
| `DB_HMI` | 3 | OFF |

---

## E) Timers IEC

| Instancia | PT |
|---|---|
| `T_RetardoPiston` | `T#500ms` |
| `T_TimeoutPiston` | `T#3s` |

---

## F) Quién manda qué

| Señal | Origen preferido |
|---|---|
| Sensores pieza/material/pistón | **`I_*` físicos** |
| Banda / pistón / lámparas | **`Q_*`** |
| START / STOP / modo desde jurado (web) | **`DB_HMI.*`** |
| Contadores a la web | **`DatosEstacion`** |

En LAD, operador web y físico se pueden **OR**-ear (ej. Start web O `I_Start`).
