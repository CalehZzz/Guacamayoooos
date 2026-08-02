# I/O y tags — CPU 1214C AC/DC/Rly (3 pistones · control web)

Ajusta direcciones si tu MLFB tiene otro mapa; los **nombres** deben coincidir con el LAD.

La 1214C típica trae **14 DI** y **10 DQ** relé: alcanza para banda + **3 cilindros** + lámparas.

---

## Operador = solo web (sin pulsadores físicos)

**No hay botonera en la mesa.** Start, Stop, Emergencia, modo auto/manual, manual de banda/pistones y reset alarma van por la app → Firestore → bridge → `DB_HMI`.

En el PLC solo cableas:
- **Sensores de proceso** (`I_Sensor*`, báscula, finales de carrera de pistones)
- **Actuadores** (`Q_Banda`, `Q_Piston1..3`, lámparas)

```
  Celular / laptop (HMI web SIBU)
        ↕ Firestore
   plc_bridge_real.py
        ↕ snap7 (DB_HMI + DatosEstacion)
   CPU 1214C  ←→  sensores + banda + 3 pistones
```

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

## A) Entradas digitales `%I` (solo proceso — no botones)

| Dirección | Nombre | Tipo | Hardware |
|---|---|---|---|
| `%I0.0` | `I_SensorPieza` | Bool | Pieza en estación |
| `%I0.1` | `I_SensorPlastico` | Bool | Sensor material plástico |
| `%I0.2` | `I_SensorAluminio` | Bool | Sensor material aluminio |
| `%I0.3` | `I_BasculaLista` | Bool | Báscula estable / lista |
| `%I0.4` | `I_Piston1Retractado` | Bool | P1 retenedor @ 0% |
| `%I0.5` | `I_Piston1Extendido` | Bool | P1 retenedor @ 100% |
| `%I0.6` | `I_Piston2Retractado` | Bool | P2 plástico @ 0% |
| `%I0.7` | `I_Piston2Extendido` | Bool | P2 plástico @ 100% |
| `%I1.0` | `I_Piston3Retractado` | Bool | P3 aluminio @ 0% |
| `%I1.1` | `I_Piston3Extendido` | Bool | P3 aluminio @ 100% |

`%I1.2`…`%I1.5` quedan libres (reserva).

> No uses tags `I_Start` / `I_Stop` / `I_Emergencia` / `I_ModoAuto` / `I_Manual*`: el operador es 100 % web.

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
| `%M0.1` | `M_ModoAuto` | Modo auto efectivo (`:= DB_HMI.ModoAuto`) |
| `%M0.2` | `M_Alarma` | Alarma |
| `%M0.3` | `M_ClasifPlastico` | Secuencia empuje plástico (P2) |
| `%M0.4` | `M_ClasifAluminio` | Secuencia empuje aluminio (P3) |
| `%M0.5` | `M_PulsePlastico` | Reserva / opcional |
| `%M0.6` | `M_EdgePlastico` | Reserva / opcional |
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

| Señal | Origen |
|---|---|
| Sensores pieza / material / báscula / pistones | **`I_*` físicos** |
| Banda / 3 pistones / lámparas | **`Q_*`** |
| START / STOP / emergencia / modo / manual / reset | **solo `DB_HMI.*` (web)** |
| Contadores y estado a la web | **`DatosEstacion`** |
