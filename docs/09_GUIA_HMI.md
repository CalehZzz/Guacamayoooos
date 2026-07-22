# Configurar la HMI en TIA Portal (ya la agregaste)

Guía práctica WinCC / HMI Basic-Comfort en TIA V20, para Guacamayos.

---

## 0) Antes de dibujar pantallas — conexión al PLC

1. En el árbol del proyecto, abre tu HMI (ej. `HMI_1` / `KTP700...`).
2. Doble clic en **Connections** / **Conexiones**.
3. Debe existir una conexión al PLC, tipo **HMI connection**, partner = tu CPU.

Si no hay ninguna:
1. Clic derecho en Connections → **Add new connection**
2. Partner: tu PLC
3. Acepta los valores por defecto (PROFINET)

Compila PLC + HMI (`Ctrl+B` o Compile → Software).

---

## 1) Crear las pantallas (2 alcanzan para el reto)

Árbol HMI → **Screens** / **Pantallas**:

1. Renombra `Root screen` / `Screen_1` a: **`Operacion`**
2. Clic derecho Screens → **Add screen** → nombre: **`Alarmas`**

(Opcional) Screen management / Plant overview: deja `Operacion` como pantalla de inicio.

---

## 2) Pantalla **Operacion** — qué poner

Abre `Operacion`. En la caja de herramientas (Toolbox) arrastra elementos.

### A) Título
- **Text field**: `Guacamayos — Estación de clasificación`

### B) Botones de mando (Toolbox → Elements → Button)

| Texto del botón | Tipo | Tag PLC a enlazar | Evento |
|---|---|---|---|
| **START** | Button | `I_Start` | Press → Set bit / Write true; Release → Write false (pulso) |
| **STOP** | Button | `I_Stop` | Press → true; Release → false |
| **EMERGENCIA** | Button (rojo) | `I_Emergencia` | Press → true (o toggle) |
| **Reset emergencia** | Button | `I_Emergencia` | Press → false |
| **Fin sesión** | Button | `I_FinSesion` o `DatosEstacion.FinSesion` | Press → true |
| **Reset alarma** | Button | `M_ResetAlarma` | Press → true; Release → false |

#### Cómo enlazar un botón (TIA)
1. Selecciona el botón  
2. Properties → **Events** → `Click` o `Press`  
3. Add function → **SetBit** / **ResetBit** / **InvertBit**  
   o **SimulateTag** / Write to tag (según tu HMI)  
4. Elige el tag del PLC (navega: PLC → PLC tags / DatosEstacion)

**Truco fácil en simulación:**  
Properties del botón → **General** → **Process** / Tag → marca el tag Bool y usa el botón como **momentary** (mientras mantienes, el bit = 1).

### C) Selector Manual / Automático
- Toolbox → **Switch** (o dos botones)
- Enlázalo a: **`M_ModoAuto`** (recomendado)  
  o a `I_ModoAuto` si prefieres

| Posición switch | Valor |
|---|---|
| Auto | `M_ModoAuto` = 1 |
| Manual | `M_ModoAuto` = 0 |

Si usas `M_ModoAuto` desde HMI, en `FC_Modos` NW3 puedes **quitar** el contacto `I_ModoAuto` o dejar que HMI escriba directo a `M_ModoAuto`.

### D) Indicadores (luces)
Toolbox → **IO field** (Bool) o **Circular graphic** / **Graphic IO field**

| Texto | Tag |
|---|---|
| Sistema ON | `M_SistemaOn` o `Q_LamparaRun` |
| Banda | `Q_Banda` |
| Pistón | `Q_Piston` |
| Emergencia | `I_Emergencia` o `Q_LamparaEmergencia` |
| Alarma | `M_Alarma` o `Q_LamparaAlarma` |
| Modo Auto | `M_ModoAuto` |

Color tip: verde = ON, gris = OFF, rojo = emergencia/alarma  
(Properties → Appearance / Animations → Appearance → Fill color según valor del tag)

### E) Contadores y pesos (IO field numérico)
Toolbox → **IO field** → Mode: **Output** (solo lectura)

| Etiqueta en pantalla | Tag |
|---|---|
| Cont. plástico | `DatosEstacion.ContPlastico` |
| Cont. aluminio | `DatosEstacion.ContAluminio` |
| Peso plástico kg | `DatosEstacion.PesoPlasticoKg` |
| Peso aluminio kg | `DatosEstacion.PesoAluminioKg` |
| Peso actual kg | `DatosEstacion.PesoActualKg` |
| Estado máquina | `DatosEstacion.EstadoMaquina` |

Formato:
- Int → sin decimales  
- Real → 1 o 2 decimales (`##.##`)

### F) Botones solo en MANUAL (opcionales)
| Texto | Tag |
|---|---|
| Banda manual | `I_ManualBanda` |
| Pistón manual | `I_ManualPiston` |

### G) Navegación
Botón **Alarmas** → Event Click → **ActivateScreen** → `Alarmas`

---

## 3) Pantalla **Alarmas**

| Elemento | Contenido |
|---|---|
| Título | `Diagnóstico / Alarmas` |
| Indicador | `I_Emergencia` — texto “Emergencia activa” |
| Indicador | `M_Alarma` — texto “Alarma activa” |
| Texto fijo | Timeout pistón / Sensores contradictorios (explicación) |
| Botón | Reset alarma → `M_ResetAlarma` |
| Botón | Volver → ActivateScreen `Operacion` |

(Si más adelante quieres Alarm view formal de WinCC, se puede; con indicadores Bool cumples el PDF.)

---

## 4) Layout sugerido de **Operacion**

```
┌─────────────────────────────────────────────┐
│  Guacamayos — Estación de clasificación     │
├──────────────┬──────────────────────────────┤
│ START        │  Sistema ON   [●]            │
│ STOP         │  Modo Auto    [switch]       │
│ EMERGENCIA   │  Banda        [●]            │
│ Reset emerg. │  Pistón       [●]            │
│ Fin sesión   │  Alarma       [●]            │
│ Reset alarma │  Emergencia   [●]            │
├──────────────┴──────────────────────────────┤
│ Plástico: #### pzs   ##.## kg               │
│ Aluminio: #### pzs   ##.## kg               │
│ Peso actual: ##.## kg                       │
│ Estado: #                                   │
├─────────────────────────────────────────────┤
│ [Manual: Banda] [Manual: Pistón]  [Alarmas] │
└─────────────────────────────────────────────┘
```

---

## 5) Compilar y simular HMI + PLC

1. Compile todo (PLC + HMI)  
2. Selecciona el **PLC** → **Start simulation** → descarga → PLCSIM en **RUN**  
3. Selecciona la **HMI** → clic derecho → **Start simulation**  
   (o botón Simulation de WinCC Runtime)  
4. Se abre la pantalla Runtime  
5. Prueba:
   - START → Sistema ON, banda (si auto)  
   - Switch en Auto  
   - En PLCSIM o watch table fuerza sensores de una pieza, **o** agrega botones HMI temporales a `I_SensorPieza` / `I_SensorPlastico` / `I_SensorAluminio` para la demo  

### Tip demo sin hardware
En la HMI agrega una zona chica “Simular pieza”:
- Botón `Pieza+Plástico` → Set `I_SensorPieza`, `I_BasculaLista`, `I_SensorPlastico`  
- Botón `Pieza+Aluminio` → Set pieza, báscula, aluminio  
- Botón `Pistón extendido` → `I_PistonExtendido`  
Así demuestras todo desde la HMI.

También puedes editar `DatosEstacion.PesoActualKg` con un IO field **Input** (ej. 0.04) antes de simular la pieza.

---

## 6) Checklist del PDF (HMI)

- [ ] Encender / detener (START / STOP)
- [ ] Modo manual / automático (switch)
- [ ] Ver sensores / actuadores (banda, pistón, luces)
- [ ] Contador de piezas (plástico + aluminio)
- [ ] Alarmas / estado (pantalla Alarmas + indicadores)

---

## Problemas frecuentes

| Problema | Qué hacer |
|---|---|
| No salen tags del PLC en la HMI | Connections mal / compila PLC primero / refresca tags |
| Botón no hace nada | Revisa Events del botón y que PLCSIM esté en RUN |
| IO field en rojo | Tag inexistente o tipo mal (Int vs Real) |
| HMI simulation no abre | Licencia Runtime / Start simulation desde el dispositivo HMI |
| START no mantiene el sistema | OK: es pulso; el latch es `M_SistemaOn` en el PLC |

---

## Orden recomendado ahora (30–40 min)

1. Verificar **Connections** HMI↔PLC  
2. Pantalla `Operacion`: START, STOP, EMERGENCIA, switch Auto, luces Banda/Pistón/Alarma  
3. IO fields de contadores del DB `DatosEstacion`  
4. Pantalla `Alarmas` simple  
5. Simular PLC + HMI juntos  
