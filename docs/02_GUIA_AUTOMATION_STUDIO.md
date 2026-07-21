# Guía — Automation Studio (desde la pantalla de inicio)

Objetivo del reto: **circuito electroneumático funcional** que represente tu estación (cilindro/pistón, electroválvula, sensores de posición, y de ser posible la idea de la banda).

No necesitas que Automation Studio hable solo con TIA el primer día. En la presentación demuestras:
1. El circuito neumático funcionando en AS.
2. El PLC + HMI funcionando en TIA/PLCSIM.
3. La app web recibiendo datos (bridge o simulador).

Si tu laboratorio tiene co-simulación AS ↔ TIA, úsala al final. Si no, basta con la simulación AS independiente alineada al mismo diseño.

---

## Parte A — Nuevo proyecto en Automation Studio

1. En la pantalla de inicio: **New** / **Nouveau projet** / proyecto vacío.
2. Nombre: `Guacamayos_ElectroNeumatica`
3. Elige un entorno con **Pneumatics** + **Electrical** (o Electropneumatics).
4. Abre un diagrama **Pneumatic** y otro **Electrical/Ladder** o usa el workspace electropneumático.

---

## Parte B — Componentes neumáticos mínimos

Arma este circuito del **pistón clasificador** (empuja latas de aluminio):

| Componente | Cantidad | Rol |
|---|---|---|
| Fuente de aire / service unit (FRL) | 1 | Alimentación |
| Electroválvula 5/2 monoestable (o 4/2) | 1 | Controla el cilindro |
| Cilindro simple efecto **o** doble efecto | 1 | Pistón empujador |
| Sensores magnéticos de posición | 2 | Retractado / Extendido |
| Silenciadores / escapes | según válvula | Buenas prácticas |

### Secuencia neumática
1. Reposo: vástago **retractado** (sensor retractado = 1).
2. Cuando el PLC/lógica pide clasificar aluminio: energiza la bobina de la electroválvula → vástago **extiende**.
3. Sensor extendido = 1 → (en el PLC) cuenta pieza y corta bobina.
4. Retorno por muelle (simple efecto) o segunda cámara (doble efecto).

---

## Parte C — Parte eléctrica (bobina + sensores)

En el diagrama eléctrico:

1. Bobina de la electroválvula = salida `Q_Piston` (en tu diseño PLC).
2. Contactos/sensores de cilindro = entradas `I_PistonRetractado` / `I_PistonExtendido`.
3. Agrega un **pulsador** de marcha y uno de paro si quieres una mini-demo solo en AS.
4. Indicadores (pilot lights) para “banda” y “alarma” aunque la banda sea solo un motor simbólico.

### Banda transportadora en AS
Opciones según lo que permita tu licencia:
- Motor eléctrico + rodillos (simplificado), o
- Un actuador lineal que represente “avance de pieza”, o
- Documento visual + un bit “conveyor ON” en la parte eléctrica.

Para el reto, lo crítico electroneumático es el **cilindro de clasificación**. La banda puede ser más simple.

---

## Parte D — Sensores de material (simbolicos)

Automation Studio no “ve” plástico vs aluminio como un sensor real de planta. Simúlalos así:

1. Dos pulsadores o sensores digitales:
   - `Sensor_Plastico`
   - `Sensor_Aluminio`
2. Un sensor de “pieza en estación”.
3. En la demo: tú activas el que corresponda (como harías en PLCSIM).

En la presentación di: *“En el prototipo real estos serían sensores inductivos/capacitivos o de visión; aquí se emulan.”*

---

## Parte E — Simulación completa del proceso (checklist AS)

Practica esta historia en AS hasta que salga fluida:

1. Aire ON / sistema listo.
2. “Banda” ON.
3. Pieza llega → sensor pieza.
4. Caso A — plástico: NO energiza válvula; pieza sigue / cae a contenedor plástico.
5. Caso B — aluminio: energiza válvula → cilindro extiende → sensor fin de carrera → retorna.
6. Muestra contador en un display numérico de AS (si tienes) o anótalo en HMI/TIA.

---

## Parte F — Cómo relacionarlo con TIA en la defensa

Prepara una lámina (o diapositiva) con la misma tabla I/O:

| Señal AS | Señal TIA |
|---|---|
| Bobina EV pistón | `Q_Piston` |
| Sensor retractado | `I_PistonRetractado` |
| Sensor extendido | `I_PistonExtendido` |
| Sensor pieza | `I_SensorPieza` |
| Sensor plástico | `I_SensorPlastico` |
| Sensor aluminio | `I_SensorAluminio` |
| Motor banda | `Q_Banda` |

Eso demuestra coherencia de diseño aunque la co-simulación no esté cableada.

---

## Checklist del PDF (Automation Studio)

- [ ] Circuito electroneumático funcional
- [ ] Cilindro(s) neumático(s)
- [ ] Electroválvula(s)
- [ ] Sensores de posición
- [ ] Simulación completa del proceso (demo contada de punta a punta)
