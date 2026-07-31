# Crear proyecto TIA — CPU 1214C AC/DC/Rly (PLC real)

El proyecto de **PLCSIM 1511C no sirve** como device del 1214C.  
Crea un proyecto nuevo.

## 1) Proyecto nuevo
1. TIA Portal V20 → Create new project (ej. `SIBU_PLC_Real_1214C`)
2. Add new device → **S7-1200** → **CPU 1214C AC/DC/Rly**  
   (elige el MLFB exacto de tu CPU, ej. `6ES7 214-1BG40-0XB0` o el que tengas)
3. Firmware: el de tu CPU física

## 2) Red / IP
1. Device configuration → PROFINET interface [X1]
2. IP estática en la misma red que tu PC (ej. `192.168.0.10` / mask `255.255.255.0`)
3. Anota esa IP para el bridge

## 3) Protección (obligatorio para snap7)
Device → CPU → **Protection & Security**:
- Permitir acceso con **PUT/GET** desde partners remotos → **ON**
- Access level: Full access (o el mínimo que permita escritura DB)

Download de **hardware** después de cambiar esto.

## 4) Bloques de programa
Crea (mismos nombres que en sim, distinta lógica de I/O):

| Bloque | Lenguaje | Rol |
|---|---|---|
| `OB1` | LAD | Calls |
| `FC_Modos` | LAD | Start/Stop/Emergencia |
| `FC_Secuencia` | LAD | Banda, conteo, pistón |
| `FC_Alarmas` | LAD | Alarmas |
| `FC_EspejoWeb` | SCL | Espejo a `DatosEstacion` |

## 5) Data blocks
| DB | Nº | Optimized |
|---|---|---|
| `DatosEstacion` | **1** | **OFF** |
| `DB_HMI` | **3** | **OFF** |

Estructura: `DB_CONTRATO_WEB.md` (igual que la web/sim).

## 6) Tag table
Copia `TABLA_IO_1214C.md`.

## 7) Download
1. CPU en STOP o RUN-P según política
2. Download hardware + software
3. RUN
4. Online: verifica DBs y I/Q

## Diferencia clave vs simulación

| | Sim (1511C) | Real (1214C) |
|---|---|---|
| Sensores | `DB_HMI.Sensor*` | **`I_Sensor*`** físicos |
| Banda / pistón | `M_Banda` / `M_Piston` | **`Q_Banda` / `Q_Piston`** |
| Start web | `DB_HMI.Start` | igual (`DB_HMI`) + opcional `I_Start` |
| AS / KEP | no | no |
