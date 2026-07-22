# Mapa de I/O y bloque de datos (DB1)

Copia estos nombres **exactamente** en TIA Portal (PLC tags + DB). Así el bridge Python y la web coinciden.

---

## 1. Entradas digitales (`%I`)

| Dirección | Nombre simbólico | Tipo | Descripción |
|---|---|---|---|
| `%I0.0` | `I_Start` | Bool | Pulsador arranque (NO) |
| `%I0.1` | `I_Stop` | Bool | Pulsador paro (NC lógico: en simulación lo tratamos activo en 1 = pedir paro) |
| `%I0.2` | `I_Emergencia` | Bool | Paro de emergencia (1 = activado / peligro) |
| `%I0.3` | `I_ModoAuto` | Bool | 1 = automático, 0 = manual (o selector HMI) |
| `%I0.4` | `I_SensorPieza` | Bool | Pieza presente en zona de clasificación |
| `%I0.5` | `I_SensorPlastico` | Bool | Material = plástico (botella) |
| `%I0.6` | `I_SensorAluminio` | Bool | Material = aluminio (lata) |
| `%I0.7` | `I_BasculaLista` | Bool | Báscula terminó de estabilizar peso |
| `%I1.0` | `I_PistonRetractado` | Bool | Cilindro en casa (sensor magnético) |
| `%I1.1` | `I_PistonExtendido` | Bool | Cilindro extendido |
| `%I1.2` | `I_FinSesion` | Bool | Botón físico “terminar sesión usuario” |
| `%I1.3` | `I_ManualBanda` | Bool | En modo manual: pedir marcha banda |
| `%I1.4` | `I_ManualPiston` | Bool | En modo manual: pedir pistón |

> En HMI puedes mapear Start/Stop/Modo/FinSesión a bits de memoria en vez de entradas físicas. Para PLCSIM es más fácil usar **tags de memoria** (`M`) controlados desde la HMI.

---

## 2. Salidas digitales (`%Q`)

| Dirección | Nombre simbólico | Tipo | Descripción |
|---|---|---|---|
| `%Q0.0` | `Q_Banda` | Bool | Motor / marcha de banda |
| `%Q0.1` | `Q_Piston` | Bool | Electroválvula: extender pistón (empuja aluminio) |
| `%Q0.2` | `Q_LamparaRun` | Bool | Indicador sistema en marcha |
| `%Q0.3` | `Q_LamparaAlarma` | Bool | Indicador alarma |
| `%Q0.4` | `Q_LamparaEmergencia` | Bool | Indicador emergencia |

---

## 3. Memorias internas (`%M`) y temporizadores

Los `%M` concretos (M0.0, M0.6…) **no tienen que ser iguales a los de nadie**. Lo importante es que **no se repitan** y que el **nombre** coincida con el programa.

| Nombre | Tipo | Ejemplo OK | Uso |
|---|---|---|---|
| `M_SistemaOn` | Bool | `%M0.0` | Latch de sistema energizado |
| `M_ModoAuto` | Bool | `%M0.1` | Copia del modo (HMI o selector) |
| `M_Alarma` | Bool | `%M0.2` | Alarma activa |
| `M_Clasificando` | Bool | `%M0.3` | Secuencia aluminio en curso |
| `M_PulsePieza` | Bool | `%M0.4` | Flanco genérico (opcional) |
| `M_ResetContadores` | Bool | `%M0.5` | Reset pedido desde HMI |
| `M_PulsePlastico` | Bool | `%M0.6` | Flanco: se contó una botella |
| `M_ResetAlarma` | Bool | `%M0.7` | Botón HMI para borrar alarma |
| `T_RetardoPiston` | Instancia TON (IEC) | DB de instancia auto | Espera con pistón extendido antes de contar |
| `T_TimeoutPiston` | Instancia TON (IEC) | DB de instancia auto | Alarma si el pistón no llega a tiempo |

> En S7-1200 **no uses** un tag `%T0` de la tag table para esto.  
> Inserta el bloque **TON**, y en el `???` de arriba escribe `T_RetardoPiston` para que TIA cree su DB.  
> Para contactos usa `T_RetardoPiston.Q` (ver `docs/06_COMO_USAR_TON.md`).

> Orden completo de networks: `tia/LOGICA_LAD.md`.

---

## 4. DB1 — `DatosEstacion` (contrato con la web)

Crea un **Data Block** global llamado `DatosEstacion` (número DB1).

### Estructura (optimized = OFF / “Standard” para offsets fijos)

| Offset | Nombre | Tipo | Notas |
|---|---|---|---|
| 0.0 | `ContPlastico` | Int | Piezas plásticas de la sesión |
| 2.0 | `ContAluminio` | Int | Piezas aluminio de la sesión |
| 4.0 | `PesoPlasticoKg` | Real | Peso acumulado plástico (kg) |
| 8.0 | `PesoAluminioKg` | Real | Peso acumulado aluminio (kg) |
| 12.0 | `PesoActualKg` | Real | Último peso leído de la báscula |
| 16.0 | `SesionActiva` | Bool | Hay usuario conectado / sesión abierta |
| 16.1 | `FinSesion` | Bool | PLC pide cerrar sesión (web guarda) |
| 16.2 | `SistemaOn` | Bool | Espejo de marcha |
| 16.3 | `ModoAuto` | Bool | Espejo modo |
| 16.4 | `Emergencia` | Bool | Espejo emergencia |
| 16.5 | `Alarma` | Bool | Espejo alarma |
| 16.6 | `BandaOn` | Bool | Espejo salida banda |
| 16.7 | `PistonOn` | Bool | Espejo salida pistón |
| 18.0 | `EstadoMaquina` | **Int** | 0 idle, 1 running, 2 clasificando, 3 alarma, 4 emergencia |
| 20.0 | `UltimoMaterial` | **Int** | 0 ninguno, 1 plástico, 2 aluminio |

### Offsets que NO sirven para la web

Si al compilar ves algo como:

- `EstadoMaquina` → **17.0**
- `UltimoMaterial` → **17.1**

eso casi siempre significa que quedaron como **Bool** (bits), no como **Int**.  
El bridge Python espera **Int en 18 y 20**. Corrige el tipo a `Int`, recompila y verifica que digan **18.0** y **20.0**.

También confirma: clic derecho en el DB → Properties → Attributes → **Optimized block access = OFF**.

### Cómo crear el DB en TIA (resumen)

1. Project tree → PLC → Program blocks → Add new block → **Data block**.
2. Name: `DatosEstacion`, Type: Global DB, Language: DB.
3. En Attributes del DB: **desactiva Optimized block access** (importante para snap7).
4. Agrega los campos de la tabla en el mismo orden y con el **tipo exacto** (Int / Real / Bool).
5. Compile y revisa la columna Offset.

---

## 5. Entrada analógica de báscula (opcional / simulado)

Si simulas peso sin hardware real:

- Usa un `Real` en el DB (`PesoActualKg`) escrito desde HMI o desde un FC que genere valores de prueba.
- Si más adelante tienes módulo analógico: `%IW64` → escala a kg.

Rangos típicos de prueba:
- Botella plástica: **0.02 – 0.06 kg**
- Lata aluminio: **0.01 – 0.03 kg**

---

## 6. Lógica de clasificación (regla simple)

Cuando `I_SensorPieza` = 1 y báscula lista:

| Sensor plástico | Sensor aluminio | Acción |
|---|---|---|
| 1 | 0 | ContPlastico++, sumar PesoActual a PesoPlastico; pistón **NO** |
| 0 | 1 | ContAluminio++, sumar PesoActual a PesoAluminio; pistón **SÍ** (extender → esperar → retraer) |
| 1 | 1 | **Alarma** (lectura inválida) |
| 0 | 0 | Esperar / no contar |

---

## 7. Lectura desde Python (offsets del bridge)

```text
ContPlastico      = get_int(db, 0)
ContAluminio      = get_int(db, 2)
PesoPlasticoKg    = get_real(db, 4)
PesoAluminioKg    = get_real(db, 8)
PesoActualKg      = get_real(db, 12)
SesionActiva      = get_bool(db, 16, 0)
FinSesion         = get_bool(db, 16, 1)
SistemaOn         = get_bool(db, 16, 2)
ModoAuto          = get_bool(db, 16, 3)
Emergencia        = get_bool(db, 16, 4)
Alarma            = get_bool(db, 16, 5)
BandaOn           = get_bool(db, 16, 6)
PistonOn          = get_bool(db, 16, 7)
EstadoMaquina     = get_int(db, 18)
UltimoMaterial    = get_int(db, 20)
```

Tamaño mínimo a leer: **22 bytes** (lee 24 para alinear).
