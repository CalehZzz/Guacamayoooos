# Automation Studio — lista rápida de componentes

Proyecto sugerido: `Guacamayos_ElectroNeumatica`

## Neumática
- Unidad de servicio (filtro/regulador)
- Electroválvula 5/2 monoestable (bobina = `Q_Piston`)
- Cilindro (pistón clasificador de latas)
- Sensor magnético retractado → `I_PistonRetractado`
- Sensor magnético extendido → `I_PistonExtendido`

## Eléctrica / señales demo
- Pulsador Start / Stop / Emergencia
- Pulsador o sensor `Pieza`
- Pulsador `Plastico`
- Pulsador `Aluminio`
- Contactor/piloto motor banda → `Q_Banda`
- Pilotos Run / Alarma / Emergencia

## Historia de simulación (2 minutos)
1. Start → banda ON
2. Pieza + Plástico → NO bobina
3. Pieza + Aluminio → bobina ON → extendido → OFF → retractado
4. Emergencia → todo OFF
