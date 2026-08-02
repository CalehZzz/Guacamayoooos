# Guion de defensa — SIBU / Guacamayos  
**Siemens Youth Innovation Search 2026 · Primera Parte · 15 minutos**

Defensa **virtual**.  
- **Edgar** y **Caleb**: Colegio Don Bosco (pueden compartir pantalla desde sus PCs).  
- **Carla**: se conecta desde otro país (comparte su pantalla en su bloque).

**Jurado:** ingenieros Siemens (CR). Hablen técnico con seguridad; no “vendan humo”.

---

## Mapa rápido: criterios → quién los gana

| Criterio | Pts | Quién lo carga |
|---|---:|---|
| Análisis del problema y propuesta | 10 | **Edgar** |
| Programación PLC en TIA Portal | 20 | **Carla** |
| Simulación electroneumática en AS | 15 | **Carla** |
| Desarrollo de la HMI | 15 | **Caleb** |
| Funcionamiento integral | 15 | Los 3 (demo + cierre físico) |
| Innovación y mejora técnica | 10 | **Caleb** (+ sorpresa física) |
| Presentación técnica | 5 | Estructura de esta defensa |
| Presentación y habilidades comunicativas | 10 | **Edgar** abre; tono de los 3 |
| **TOTAL** | **100** | |

---

## Setup técnico (antes de entrar)

| Quién | Tiene abierto / listo |
|---|---|
| Edgar | Diapos “problema CR” + foto/idea de estación en colegio/parque |
| Carla | TIA V20 (LAD + DBs) + Automation Studio + KEPServer (si hay sim corriendo, mejor) |
| Caleb | GitHub Pages / `index.html` + HMI + (opcional) bridge conectado |
| Los 3 | Zoom/Meet estable · micrófono · “sorpresa física” lista para el minuto 12 |

**Regla de oro virtual:** quien habla, comparte pantalla. Cambio de turno = “te paso la pantalla / te doy el lead”.

---

## Reloj (15:00)

| Min | Bloque | Quién | Pantalla |
|---:|---|---|---|
| 0:00–0:50 | Hook / apertura | Edgar | Edgar |
| 0:50–3:40 | Problemática + propuesta SIBU | Edgar | Edgar |
| 3:40–4:00 | Puente a Carla | Edgar → Carla | — |
| 4:00–9:10 | TIA + AS + KEPServer | Carla | **Carla** |
| 9:10–9:25 | Puente a Caleb | Carla → Caleb | — |
| 9:25–12:10 | Innovación web / HMI | Caleb | **Caleb** |
| 12:10–14:10 | Funcionamiento integral + **sorpresa física** | Caleb + Edgar (+ Carla comenta) | Caleb / cámara física |
| 14:10–15:00 | Cierre memorable | Edgar (+ 1 línea cada uno) | Edgar |

Si se atrasan: corten adornos, **no** corten TIA (20 pts) ni la demo integral.

---

# BLOQUE 1 — Edgar (0:00 → 3:40)  
## Captar atención + problemática + propuesta · ~10 pts análisis + comunicación

### 0:00–0:50 · Hook (no digan “buenas, nosotros somos…”)

**Edgar (mirando a cámara, sin diapos al inicio o con una sola imagen fuerte: basura en parque / colegio):**

> “Ingenieros: imaginen un colegio en San José un viernes a las 2 de la tarde.  
> Hay un contenedor de reciclaje… y al lado, botellas y latas en el piso.  
> No es que la gente no sepa reciclar. Es que **reciclar no da feedback**.  
> No pesa, no clasifica, no premia, no deja evidencia.  
> Hoy les presentamos **SIBU**: una estación de clasificación y pesaje que convierte el reciclaje en un proceso medible — y en una recompensa.”

*(Pausa 1 segundo. Sonrían. Luego sí: presentaciones cortas.)*

> “Somos el equipo Guacamayos — Colegio Don Bosco.  
> Yo soy **Edgar**. Conmigo están **Caleb**, aquí en el colegio.  
> Y en remoto, desde otro país, **Carla**, que les va a mostrar el corazón Siemens del sistema.”

### 0:50–2:40 · Problemática (cultura de reciclaje → problema de ingeniería)

**Edgar (diapos 2–3: datos locales / observación, no ensayo):**

> “En Costa Rica hablamos mucho de sostenibilidad, pero en la práctica el reciclaje escolar y comunitario tiene tres fallas de ingeniería:  
> 1) **Clasificación inconsistente** — plástico y aluminio se mezclan.  
> 2) **Sin medición** — no hay peso, no hay contadores, no hay sesión.  
> 3) **Sin incentivo cerrado** — el usuario no ve un resultado inmediato.  
>  
> Eso no se resuelve con un afiche. Se resuelve con **automatización + una interfaz que la gente sí use**.”

### 2:40–3:40 · Propuesta (estación replicable)

**Edgar (diapos: sketch estación en colegio / parque):**

> “Nuestra propuesta: una **estación modular SIBU** que se pueda instalar en un colegio, un parque o un centro comunal.  
> Flujo: la persona deja la pieza → se pesa → la banda avanza → sensores identifican material → actuadores separan → la app acumula piezas, kilos y una recompensa en colones.  
>  
> Arquitectura en tres capas, como les gusta a Siemens:  
> - **Campo / simulación:** electroneumática en Automation Studio  
> - **Cerebro:** PLC en TIA Portal  
> - **Innovación:** HMI y app web que habla con el PLC  
>  
> Carla les va a abrir el PLC y el circuito. Caleb, la innovación.  
> Y al final… les tenemos una sorpresa física.”

**Puente (3:40):**  
> “Carla, te paso el lead. Muéstrales por qué esto no es solo una idea bonita: es LAD, timers y un bus de datos limpio.”

---

# BLOQUE 2 — Carla (4:00 → 9:10)  
## TIA Portal (20) + Automation Studio (15) + KEP · el bloque más pesado

> **Tono:** ingeniera a ingenieros. Digan tags, DBs, TON, por qué `%M` y no solo `I/Q` en sim.

### 4:00–4:40 · Arquitectura (1 diagrama)

**Carla (comparte pantalla: diagrama AS ↔ KEP ↔ TIA/PLCSIM):**

> “Buenas. Soy Carla.  
> Stack: **TIA Portal V20**, CPU **1511C** en **PLCSIM Advanced**, **Automation Studio 10**, puente **KEPServerEX 6**.  
> Automation Studio no habla S7 nativo con comodidad; por eso KEPServer mueve tags hacia memorias del PLC.  
> En simulación usamos **`%M`** para sensores y actuadores compartidos con AS.  
> La web no toca I/Q a lo loco: escribe **`DB_HMI`** y lee **`DatosEstacion`**.”

### 4:40–7:10 · Programación PLC en TIA (apunten a los 20 pts)

**Carla (TIA: OB1 + FCs + un network clave en pantalla grande):**

> “Software estructurado en cuatro funciones:  
> - **`FC_Modos`:** Start / Stop / Emergencia / modo auto — latches limpios, sin pelear bobinas.  
> - **`FC_Secuencia`:** banda, detección de material, secuencia de clasificación, conteo.  
> - **`FC_Alarmas`:** timeout de pistón, sensores contradictorios, reset.  
> - **`FC_EspejoWeb`:** copia estado a `DatosEstacion` para la app.  
>  
> Detalle que importa en evaluación:  
> - Una sola bobina por actuador: **AUTO // MANUAL en paralelo**, no doble escritura.  
> - Timers **TON IEC** — retardo de clasificación y timeout de seguridad.  
> - Data Blocks con **Optimized access OFF** porque el bridge usa offsets fijos (snap7).  
> - Contrato claro: comandos en **DB3 `DB_HMI`**, estado en **DB1 `DatosEstacion`**.”

*(Si pueden: 20–30 s de ONLINE / force o simulación corta de un ciclo plástico vs aluminio.)*

> “En el camino a hardware real también diseñamos la variante **S7-1200 1214C** con I/Q físicos y **tres pistones**: retenedor, empuje plástico y empuje aluminio — misma lógica de producto, distinto mapa de campo.”

### 7:10–9:00 · Automation Studio + KEPServer (15 pts)

**Carla (AS en pantalla: cilindro, 5/2, sensores 0%/100%):**

> “En Automation Studio modelamos la estación electroneumática:  
> fuente → válvula **5/2** → cilindro de doble efecto → referencias de sensor en **0% y 100%**.  
>  
> KEPServer enlaza esas variables a tags del PLC.  
> Cuando el PLC pone el solenoide, AS mueve el vástago; cuando llega a 100%, el sensor regresa al PLC y la secuencia avanza.  
> Eso cierra el lazo: **no es un GIF, es feedback de proceso**.”

### 9:00–9:10 · Handoff a Caleb

> “Hasta aquí: cerebro Siemens + músculo neumático.  
> Caleb les muestra la capa que el usuario toca — y por qué eso es nuestra innovación.”

---

# BLOQUE 3 — Caleb (9:25 → 12:10)  
## HMI (15) + Innovación (10)

### 9:25–10:20 · La apuesta de innovación

**Caleb (abre la web / GitHub Pages):**

> “La innovación no fue poner otra KTP en el rack.  
> Fue preguntarnos: ¿quién usa la estación en un colegio o un parque?  
> Un estudiante con el celular. Un docente. Un jurado remoto.  
>  
> Entonces construimos **SIBU web**:  
> - App de usuario: sesión, materiales, kilos, recompensa en **colones**.  
> - **HMI virtual** estilo Comfort/KTP para operar como panel industrial.  
> - Puente **`plc_bridge.py`**: Firestore ↔ snap7 ↔ DBs del PLC.  
>  
> El navegador no habla S7. El bridge sí. Eso es diseño de sistema, no maquillaje.”

### 10:20–11:40 · HMI: qué hace (demo viva)

**Caleb (HMI a pantalla completa si pueden):**

> “En la HMI el operador manda Start, Stop, emergencia, modo auto/manual, peso y — en la versión real — **Extender/Retractar** de cada pistón.  
> Los comandos caen en `DB_HMI`.  
> El estado vuelve por `DatosEstacion`: banda, pistones, contadores, alarmas.  
>  
> Para el usuario final no mostramos tags: mostramos progreso y recompensa.  
> Misma verdad de proceso, dos lenguajes: industrial y humano.”

*(Click real: Start → simular plástico/aluminio o mostrar sesión en vivo. 30–40 s máximo.)*

### 11:40–12:10 · Por qué esto suma innovación técnica

> “Mejora técnica concreta:  
> 1) HMI remota usable en defensa virtual y en sitio.  
> 2) Contrato de datos versionado (offsets, DBs).  
> 3) Camino a PLC real 1214C sin rehacer la app.  
> Eso es innovación aplicada a Siemens, no una landing page decorativa.”

**Puente:**  
> “Ahora el criterio que amarra todo: funcionamiento integral. Y la sorpresa.”

---

# BLOQUE 4 — Funcionamiento integral + sorpresa física (12:10 → 14:10) · 15 pts + boost innovación

### 12:10–12:50 · Ciclo integral (narrado en 40 s)

**Caleb o Edgar (mientras se ve el flujo):**

> “Ciclo completo:  
> pieza → peso → banda → material → clasificación → conteo → recompensa en app.  
> Si hay timeout o sensores contradictorios: alarma.  
> Si hay emergencia: paro.  
> Eso es funcionamiento integral: no tres demos sueltas, un sistema.”

### 12:50–14:10 · SORPRESA — enfoque físico

**Coreografía sugerida (virtual):**

1. Edgar:  
   > “Hasta ahora vieron simulación y software. La pregunta del jurado siempre es: ¿esto vive fuera de la laptop?”
2. Caleb acerca la cámara / comparte video corto / muestra mesa:  
   > “Estamos llevando SIBU a **físico**: estación real con banda, sensores y **tres pistones** — retenedor, plástico, aluminio — operada desde la misma web. Sin botonera: el mando es el HMI.”
3. Carla (10 s, refuerzo Siemens):  
   > “Eso implica pasar de tags `%M`/AS a **I/Q reales** en 1214C, manteniendo el mismo contrato de DBs. Misma lógica de producto, otro nivel de campo.”

**No prometan hardware que no puedan mostrar.** Si el físico está a medias:  
> “Esta es la mesa en construcción / la prueba de concepto física; el software ya está listo para alimentarla.”

---

# BLOQUE 5 — Cierre (14:10 → 15:00)

**Edgar:**

> “SIBU ataca un problema real de cultura de reciclaje con una respuesta de automatización:  
> clasifica, mide y recompensa.  
> Siemens en el núcleo. Una web como puente al mundo real.  
> Y una estación pensada para colegios y espacios públicos en Costa Rica.”

**Cada uno, una línea (ensayen, suena a banda):**

- **Carla:** “PLC estructurado, seguro y listo para campo.”  
- **Caleb:** “Innovación que un estudiante puede tocar con el celular.”  
- **Edgar:** “Gracias. Quedamos abiertos a sus preguntas técnicas.”

---

## Frases prohibidas (suenan a feria escolar)

- “Es como un Arduino pero con Siemens…”  
- “La página es lo más importante y el PLC es secundario…”  
- “No alcanzó el tiempo para alarmas/timers…”  
- “KEPServer es un programa que conecta cosas” *(digan **tags / OPC / `%M`**)*  

## Frases que suman con jurado Siemens

- “Optimized block access OFF por offsets de snap7.”  
- “Una bobina por salida: AUTO y MANUAL en paralelo.”  
- “Timeout TON de pistón → alarma.”  
- “AS da el feedback de posición; el PLC decide.”  
- “La HMI web escribe `DB_HMI`; no reemplaza la lógica del PLC.”  

---

## Checklist de ensayo (1 corrida cronometrada)

- [ ] Edgar abre sin leer el celular  
- [ ] Carla tiene TIA + AS listos (ventanas acomodadas)  
- [ ] Caleb tiene HMI en pantalla completa y un ciclo demo que no falle  
- [ ] Cambio de pantalla Edgar→Carla→Caleb &lt; 15 s  
- [ ] Sorpresa física ensayada (ángulo de cámara)  
- [ ] Cierre a los 14:50, no a los 16:00  
- [ ] Preguntas frecuentes listas (abajo)

---

## Preguntas típicas del jurado (respuestas cortas)

**1) ¿Por qué web y no solo Comfort Panel?**  
Porque la estación vive en colegios/parques: el usuario trae el celular; el operador igual puede usar HMI web. El PLC sigue siendo el master.

**2) ¿Qué pasa si se cae internet?**  
El PLC puede seguir su lógica local; la app/bridge pierde telemetría. En sitio real se prioriza red local + bridge en PC de estación.

**3) ¿Dónde está la seguridad?**  
Emergencia y stop en lógica; timeout de actuadores; en físico se suma E-stop cableado cuando el hardware lo permita.

**4) ¿Plástico y aluminio nada más?**  
Alcance deliberado del prototipo (2 materiales). Arquitectura de tags/contadores extensible.

**5) ¿Cuál fue el aporte de cada quien?**  
Edgar: problema/propuesta/comunicación. Carla: TIA + AS + KEP. Caleb: web/HMI/bridge/innovación.

---

## Mini-cue cards (imprimir / segunda pantalla)

### Edgar
1. Hook basura vs contenedor  
2. 3 fallas: clasificar / medir / incentivar  
3. Estación modular colegio-parque  
4. Paso a Carla  
5. Cierre + sorpresa

### Carla
1. Diagrama AS–KEP–TIA  
2. 4 FCs + DB_HMI / DatosEstacion  
3. AUTO//MANUAL, TON, Optimized OFF  
4. AS 5/2 + sensores 0/100  
5. Paso a Caleb · refuerzo 1214C

### Caleb
1. Innovación = HMI/app real para humanos  
2. Bridge snap7 + Firestore  
3. Demo HMI (Start / ciclo)  
4. Camino a físico 3 pistones  
5. Una línea de cierre
