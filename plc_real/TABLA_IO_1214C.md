# I/O — CPU 1214C (3 pistones · plástico / latas / vidrio)

Operador **100 % web** (`DB_HMI`). En mesa: sensores + banda + 3 cilindros **simple efecto**.

| Pistón | Salida | Material |
|---|---|---|
| **P1** | `Q_Piston1` | Plástico |
| **P2** | `Q_Piston2` | Latas (aluminio) |
| **P3** | `Q_Piston3` | Vidrio |

```
  [Entrada] → [Báscula] → [Banda] → sensores
                                      ├─ plástico → P1
                                      ├─ latas    → P2
                                      └─ vidrio   → P3
```

## Entradas `%I` (8)

| Dir | Tag | Hardware |
|---|---|---|
| `%I0.0` | `I_SensorPieza` | Pieza presente |
| `%I0.1` | `I_SensorPlastico` | Plástico |
| `%I0.2` | `I_SensorAluminio` | Latas |
| `%I0.3` | `I_SensorVidrio` | Vidrio |
| `%I0.4` | `I_BasculaLista` | Báscula lista |
| `%I0.5` | `I_Piston1Extendido` | P1 extendido |
| `%I0.6` | `I_Piston2Extendido` | P2 extendido |
| `%I0.7` | `I_Piston3Extendido` | P3 extendido |

## Salidas `%Q` (7)

| Dir | Tag | Hardware |
|---|---|---|
| `%Q0.0` | `Q_Banda` | Banda |
| `%Q0.1` | `Q_Piston1` | Solenoide 3/2 plástico |
| `%Q0.2` | `Q_Piston2` | Solenoide 3/2 latas |
| `%Q0.3` | `Q_Piston3` | Solenoide 3/2 vidrio |
| `%Q0.4` | `Q_LamparaRun` | Verde |
| `%Q0.5` | `Q_LamparaAlarma` | Rojo |
| `%Q0.6` | `Q_LamparaEmergencia` | Amarillo |

## Memorias

`M_SistemaOn` · `M_ModoAuto` · `M_Alarma` · `M_ClasifPlastico` · `M_ClasifAluminio` · `M_ClasifVidrio` · `M_Clasificando`

## DBs

`DatosEstacion` DB1 · `DB_HMI` DB3 · Optimized **OFF** (ver `DB_CONTRATO_WEB.md`)
