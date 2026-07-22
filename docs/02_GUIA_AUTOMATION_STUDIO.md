# Guía Automation Studio — Guacamayos (nombres exactos)

## Arranque (pantalla de inicio)

1. **New** / nuevo proyecto  
2. Nombre: `Guacamayos_ElectroNeumatica`  
3. Template: **Pneumatic / Symbols / Metric Units** (o Multitechnology)  
4. Abre el schematic y las librerías **Pneumatic** + **Electrical Control**

Lista detallada de componentes: [`../automation_studio/COMPONENTES.md`](../automation_studio/COMPONENTES.md)

---

## Qué vas a armar (1 frase)

Un **cilindro de doble efecto** empujado por una **válvula 5/2 con solenoide**, con **2 sensores de posición**, más pulsadores que simulan Start/piezas/material.

---

## Paso A — Neumática (nombres exactos)

De la librería **Pneumatic**, arrastra:

1. `Pneumatic Pressure Source`
2. `Exhaust` (×2)
3. `Double-Acting Cylinder` ← Actuators
4. `5/2-Way NC Valve` ← Directional Valves → 5/2-Way  
   - Properties → Technical Specifications → comando **Solenoid DC/AC** + **Spring Return**
5. `Sensor Ref.` (×2) ← Sensors → Sensor References  
   - Uno a extensión **0%** (retractado)  
   - Otro a extensión **100%** (extendido)

Conecta: Fuente → válvula → cilindro; escapes a los puertos de escape de la 5/2.

---

## Paso B — Eléctrica (nombres exactos)

De **Electrical Control**:

1. `Power Supply 24 Volts` + `Common (0 Volts)`
2. Varios `Normally Open Push-Button` con alias:
   - `I_Start`, `I_Stop`, `I_Emergencia`
   - `I_SensorPieza`, `I_SensorPlastico`, `I_SensorAluminio`
   - `I_ManualBanda`, `I_ManualPiston`
3. `Normally Open Proximity Switch` ×2 → alias `I_PistonRetractado`, `I_PistonExtendido`
4. `Solenoid, DC/AC` → alias **`Q_Piston`**
5. (Opcional) `Coil` → `Q_Banda` + pilot lights

### Enlaces (Variable Assignment)
- Solenoide de la **5/2** ↔ Alias `Q_Piston`
- Cada **Sensor Ref.** ↔ su **Proximity Switch**

---

## Paso C — Simular

**Simulation → Normal Simulation**

Historia:
1. Start  
2. Pieza + Plástico → no energices `Q_Piston`  
3. Pieza + Aluminio → `Q_Piston` ON → extiende → sensor 100%  
4. `Q_Piston` OFF → retorna → sensor 0%  
5. Emergencia → off  

---

## Checklist del reto (PDF)

- [ ] Circuito electroneumático funcional  
- [ ] Cilindro: `Double-Acting Cylinder`  
- [ ] Electroválvula: `5/2-Way NC Valve` + Solenoid  
- [ ] Sensores de posición: `Sensor Ref.` + Proximity  
- [ ] Demo completa del proceso  

---

## Relación con TIA (para la defensa)

| Automation Studio | TIA Portal |
|---|---|
| Solenoid `Q_Piston` | `%Q0.1` `Q_Piston` |
| Proximity retractado | `I_PistonRetractado` |
| Proximity extendido | `I_PistonExtendido` |
| Push-Buttons de material | `I_SensorPlastico` / `I_SensorAluminio` |
| Coil `Q_Banda` | `Q_Banda` |
