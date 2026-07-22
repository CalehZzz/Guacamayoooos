# Automation Studio — qué usar con TU librería (Guacamayos)

Respuestas directas a lo que te salió en pantalla.

---

## 1) No hay “Válvula 5/2 NC” — ¿qué pongo?

Usa la **Válvula 5/2** normal (la que sí te aparece).

1. Arrástrala al esquema  
2. Doble clic → **Especificaciones técnicas**  
3. Configura los mandos:
   - Un lado: **Solenoide** (o “mando eléctrico / bobina”)
   - El otro: **Retorno por muelle / resorte**

Con eso queda monoestable (como una 5/2 NC típica de laboratorio).

### ¿Y la 3/2 NC?
Sí sirve, pero cambia el cilindro:

| Válvula | Cilindro recomendado |
|---|---|
| **5/2** (la tuya) | **Cilindro de doble efecto** ← usa esta combo |
| **3/2 NC** | Cilindro de **simple efecto** (retorno por muelle) |

**Recomendación:** quédate con **5/2 + cilindro de doble efecto**.

---

## 2) ¿Referencia de sensor uni o bidimensional?

Para el pistón (retractado / extendido) usa:

**Referencia de sensor unidimensional** (o solo “Ref. de sensor” / “Sensor Ref.”)

- 1 sensor en **0%** del cilindro → retractado  
- 1 sensor en **100%** → extendido  

**Bidimensional** NO: eso es para planos X-Y, no para un vástago que solo avanza/retorna.

---

## 3) Detector de proximidad NA / Contacto NA — no deja alias

En muchas versiones el alias **no se pide al soltarlos**. Se pone así:

1. Doble clic en el componente  
2. Busca una de estas pestañas:
   - **Identificación**
   - **Nombre**
   - **Etiqueta**
   - **Simulación** / **Variable**
3. Campo **Nombre** / **Alias** / **Tag** → escribe por ejemplo `I_PistonExtendido`

Si tampoco hay campo de nombre:
- Enlázalo por **Asignación de variables** (*Variable Assignment*) al **Ref. de sensor** del cilindro  
- El “nombre” queda en el sensor; el detector solo se asocia

Para el **Contacto NA**:
- No siempre lleva alias propio  
- Se asocia a una **Bobina / Relé** (el contacto “sigue” a esa bobina)  
- Doble clic en el contacto → elige la bobina a la que pertenece

---

## 4) No encuentro “Solenoide CC/CA” ni “Bobina”

Los nombres cambian según idioma/versión. Busca en la librería **Control eléctrico** con el buscador:

### Para el pistón (lo que alimenta la 5/2)
Prueba estos nombres:
- **Solenoide**
- **Solenoide eléctrico**
- **Bobina de solenoide**
- **Electroimán**
- **Actuador eléctrico**
- En inglés: `Solenoid`, `Solenoid DC`, `Solenoid AC`

Ruta típica: **Componentes de salida** / **Salidas** / **Actuadores**

### Si de plano no hay solenoide suelto
Plan B (muy común en AS):

1. En la **válvula 5/2**, pon el mando en **Solenoide**  
2. En el esquema eléctrico arma la lógica con lo que sí tengas  
3. Doble clic válvula → **Asignación de variables**  
4. Click en el solenoide de la válvula (`?(ls)`)  
5. AS te lista variables compatibles: elige un **pulsador**, una **salida** o una **bobina de relé** que hayas creado  

Mientras el `?(ls)` se reemplace por un nombre, ya está enlazado.

### Para “Bobina” (banda / relé auxiliar)
Busca:
- **Bobina**
- **Bobina de relé**
- **Relé**
- **Contactor**
- En inglés: `Coil`, `Relay coil`

Ruta: **Componentes de salida → Bobinas** (*Output Components → Coils*)

Si no hay bobina:
- Usa una **lámpara piloto** o un **pulsador** solo para la demo de banda (simbólico), o  
- Omite la banda en AS y demuéstrala solo en TIA/HMI (el PDF prioriza cilindro + válvula + sensores)

---

## 5) Lista mínima que SÍ puedes armar con lo que describes

### Neumática
| Componente | Cant. |
|---|---|
| Fuente de presión neumática | 1 |
| Escape | 2 |
| Cilindro de doble efecto | 1 |
| **Válvula 5/2** (configurada solenoide + muelle) | 1 |
| **Ref. de sensor unidimensional** | 2 |

### Eléctrica (con lo que encuentres)
| Componente | Cant. | Nota |
|---|---|---|
| Fuente 24 V + Común 0 V | 1+1 | |
| Pulsador NA | 6–8 | Start, Stop, Emergencia, Pieza, Plástico, Aluminio… |
| Detector de proximidad NA | 2 | Enlazar a los Ref. de sensor |
| Lo que haga de solenoide / salida | 1 | Enlazar a la 5/2 |
| Bobina o relé (si aparece) | 0–1 | Opcional banda |

---

## 6) Orden práctico ahora

1. Arma solo neumática: fuente + **5/2** + cilindro doble efecto + 2 escapes + 2 ref. **unidimensionales**  
2. Simulación → mueve la válvula a mano (si tiene botón) y verifica que el cilindro sale/entra y los sensores cambian  
3. Pasa a eléctrico: 24 V, pulsadores, proximidades  
4. Enlaza válvula ↔ salida/solenoide por **Asignación de variables**  
5. Lo que no exista (Solenoide CC/CA exacto, Bobina exacta) sustitúyelo por el equivalente que sí te liste el buscador  

---

## Resumen rápido

| Tu duda | Respuesta |
|---|---|
| ¿5/2 o 3/2 NC? | **5/2** + cilindro doble efecto |
| ¿Sensor uni o bi? | **Unidimensional** (×2) |
| ¿Alias en proximidad/contacto? | En propiedades / asignación de variables; el contacto va ligado a una bobina |
| ¿Solenoide CC/CA / Bobina? | Busca “Solenoide”, “Bobina de relé”, “Relé”; o enlaza la 5/2 por Asignación de variables a lo que sí tengas |
