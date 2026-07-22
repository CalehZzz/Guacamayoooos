# Guía Automation Studio — en español

## Desde la pantalla de inicio

1. **Nuevo proyecto**
2. Nombre: `Guacamayos_ElectroNeumatica`
3. Plantilla: **Neumática / Símbolos / Unidades métricas**
4. Abre librerías **Neumática** + **Control eléctrico**

Lista completa: [`../automation_studio/COMPONENTES.md`](../automation_studio/COMPONENTES.md)

---

## Qué armas

Un **cilindro de doble efecto** + **válvula 5/2 con solenoide** + **2 sensores de posición**, y pulsadores que simulan Start / pieza / material.

---

## Paso A — Neumática

Arrastra:

1. **Fuente de presión neumática**
2. **Escape** (×2)
3. **Cilindro de doble efecto**
4. **Válvula 5/2 NC** → Solenoide CC/CA + retorno por muelle
5. **Ref. de sensor** (×2) → una al 0% (retractado), otra al 100% (extendido)

---

## Paso B — Eléctrica

1. **Fuente 24 V** + **Común 0 V**
2. **Pulsadores NA** con alias:  
   `I_Start`, `I_Stop`, `I_Emergencia`, `I_SensorPieza`, `I_SensorPlastico`, `I_SensorAluminio`, `I_ManualBanda`, `I_ManualPiston`
3. **Detectores de proximidad NA** ×2 → `I_PistonRetractado`, `I_PistonExtendido`
4. **Solenoide CC/CA** → alias `Q_Piston` (enlázalo a la válvula 5/2)
5. Opcional: **Bobina** `Q_Banda` + lámparas piloto

---

## Paso C — Simular

**Simulación → Simulación normal**

1. Start  
2. Plástico → no energices el solenoide  
3. Aluminio → `Q_Piston` ON → extiende → OFF → retorna  
4. Emergencia → todo off  

---

## Checklist del reto

- [ ] Circuito electroneumático funcionando  
- [ ] Cilindro de doble efecto  
- [ ] Válvula 5/2 (electroválvula)  
- [ ] Sensores de posición  
- [ ] Demo completa  

---

## Puente con TIA (para la exposición)

| Automation Studio | TIA Portal |
|---|---|
| Solenoide `Q_Piston` | `Q_Piston` |
| Proximidad retractado / extendido | `I_PistonRetractado` / `I_PistonExtendido` |
| Pulsadores de material | `I_SensorPlastico` / `I_SensorAluminio` |
| Bobina `Q_Banda` | `Q_Banda` |
