# Networks LAD — PLC real 1214C (plástico / latas / vidrio)

**Reglas:** sensores `I_*` · actuadores `Q_*` · operador solo `DB_HMI.*` · espejo `DatosEstacion`.

| Pistón | Salida | Material |
|---|---|---|
| P1 | `Q_Piston1` | Plástico |
| P2 | `Q_Piston2` | Latas |
| P3 | `Q_Piston3` | Vidrio |

Simple efecto: 1 FC `I_PistonNExtendido` por cilindro. Detalle I/O: `TABLA_IO_1214C.md`.

La versión sim (mismos roles, sensores en `DB_HMI`) está en `tia/NETWORKS_WEB_ONLY.md`.

---

## OB1
`FC_Modos` → `FC_Secuencia` → `FC_Alarmas` → `FC_EspejoWeb`

---

## FC_Modos
- START → `(S) M_SistemaOn` (con `/Stop` `/Emergencia`)
- STOP / EMERGENCIA → `(R) M_SistemaOn`
- `DB_HMI.ModoAuto` → `M_ModoAuto`

---

## FC_Secuencia

**Banda:** AUTO (On·Auto·/Emerg·/Alarma·/Clasificando) // MANUAL (`ManualBanda`) → `Q_Banda`

**Latch plástico** (`I_SensorPlastico`, excluye otros) → `(S) M_ClasifPlastico`  
**Latch latas** (`I_SensorAluminio`) → `(S) M_ClasifAluminio`  
**Latch vidrio** (`I_SensorVidrio`) → `(S) M_ClasifVidrio`

**P1 / P2 / P3** — una bobina cada uno, dos ramas:

```
AUTO:   ClasifX · /I_PistonNExtendido ──┐
                                        ├──( ) Q_PistonN
MANUAL: M_SistemaOn · /M_ModoAuto · DB_HMI.Manual… ─┘
```

| Pistón | Auto | Manual (`DB_HMI`) |
|---|---|---|
| P1 | `M_ClasifPlastico` | `ManualPiston1` @ 1.6 |
| P2 | `M_ClasifAluminio` | `ManualPiston2` @ 1.7 |
| P3 | `M_ClasifVidrio` | `ManualPiston` @ 0.7 |

**Importante (simple efecto):**  
- **Extender** = bit Manual = 1 → `Q` ON  
- **Retractar** = bit Manual = 0 → `Q` OFF (no enciende nada; el resorte mete el vástago)  
- Sin **START** (`M_SistemaOn`) la rama MANUAL no activa la Q.  
- Debe existir modo **MANUAL** (`DB_HMI.ModoAuto = 0`).

**Contar:** TON retardo con `I_PistonNExtendido` → reset latch + incrementar `Cont*` / `Peso*`  
`UltimoMaterial` = 1 / 2 / 3

**Timeouts:** TON 3s sin FC → `(S) M_Alarma`

`M_Clasificando := ClasifPlastico OR ClasifAluminio OR ClasifVidrio`

---

## FC_EspejoWeb
```scl
DatosEstacion.BandaOn   := Q_Banda;
DatosEstacion.Piston1On := Q_Piston1;
DatosEstacion.Piston2On := Q_Piston2;
DatosEstacion.Piston3On := Q_Piston3;
DatosEstacion.PistonOn  := Q_Piston1 OR Q_Piston2 OR Q_Piston3;
DatosEstacion.PesoActualKg := DB_HMI.PesoActualKg;
```
