# Automation Studio — dónde clicás (válvula, sensores, alias)

---

## 1) Válvula 5/2: dónde poner Solenoide + retorno por muelle

1. **Doble clic** en la **Válvula 5/2** del esquema  
2. En el menú de la **izquierda** de la ventana de propiedades, entra a:

   **Especificaciones técnicas**  
   (si está en inglés: **Technical Specifications**)

3. Ahí verás el “constructor” de la válvula: los mandos de izquierda y derecha del cajón 5/2.

4. En **un lado** (ej. izquierda):
   - Si hay Push-Button / mando que no quieras → selecciónalo → **Eliminar mando** / Delete selected command  
   - Agrega / cambia a: **Solenoide** / **Solenoide CC/CA** / **Solenoid**

5. En el **otro lado** (ej. derecha):
   - Debe quedar **Retorno por muelle** / **Retorno por resorte** / **Spring Return**  
   - Si no está, agrégalo igual que el solenoide (lista de mandos)

6. Confirma con el **check verde** / Aceptar / OK

### Si no ves “Especificaciones técnicas”
Prueba estas pestañas del mismo diálogo:
- **Datos técnicos**
- **Constructor de válvula**
- **Mandos** / **Commands**
- **Configuración**

Lo que buscas es la pantalla donde se ven los **símbolos de mando** pegados a la válvula (botón, solenoide, muelle), no la de presión/caudal.

### Cómo saber que quedó bien
En el símbolo de la 5/2 debes ver:
- de un lado un **rectángulo de solenoide** (bobina)
- del otro un **muelle**

Si solo tiene botones mecánicos, aún no quedó en modo eléctrico.

---

## 2) Sensores unidimensionales: qué alias / nombre ponerles

Ponles nombres claros (en el Ref. de sensor o al enlazar):

| Sensor en el cilindro | Nombre / alias |
|---|---|
| En **0%** (vástago adentro) | `M_PistonRetractado` |
| En **100%** (vástago afuera) | `M_PistonExtendido` |

Esos mismos nombres van en TIA (`%M2.4` / `%M2.5`) y en KEPServer.  
Guía detallada: `tia/AS_TAGS_Y_SENSORES_0_100.md`.

### Cómo ponerles nombre
1. Doble clic en cada **Ref. de sensor unidimensional**  
2. Pestaña **Identificación** / **Nombre** / **General**  
3. Campo **Nombre** o **Alias** → escribe `M_PistonRetractado` o `M_PistonExtendido`

Si esa ref. no tiene campo de nombre:
- El nombre se lo pones al **detector / relé sensor** eléctrico al enlazarlo, o  
- En **Asignación de variables** al crear el vínculo

---

## 3) “Relé sensor” sin opción de alias — normal

En AS muchos sensores eléctricos **no piden alias al soltarlos**. Se nombran o se enlazan después.

Prueba en este orden:

### Opción A — propiedades del componente
1. Doble clic en el **relé sensor** / detector  
2. Busca:
   - **Identificación**
   - **Nombre**
   - **Etiqueta**
   - **Simulación**
3. Si hay cuadro **Nombre** / **Alias** / **Tag** → pon `I_PistonRetractado` (o Extendido)

### Opción B — no tiene nombre propio: se enlaza
1. Doble clic en la **Ref. de sensor** del cilindro (o en el relé sensor)  
2. **Asignación de variables** (*Variable Assignment*)  
3. Asocia:
   - Ref. @ 0% ↔ relé/detector retractado  
   - Ref. @ 100% ↔ relé/detector extendido  

Cuando el enlace existe, en simulación el detector cambia solo al llegar el cilindro.

### Opción C — el “nombre” está en otro lado
A veces el texto visible se edita:
- Clic en el texto al lado del símbolo en el esquema → renombrar  
- O clic derecho → **Editar texto** / **Rename**

---

## 4) Mini checklist

- [ ] 5/2 abierta → **Especificaciones técnicas** → Solenoide + Muelle  
- [ ] Sensor @ 0% → nombre `I_PistonRetractado`  
- [ ] Sensor @ 100% → nombre `I_PistonExtendido`  
- [ ] Relé/detector enlazado por **Asignación de variables** (aunque no tenga alias)

---

## 5) Si puedes, mándame (o describe) qué pestañas te salen

En la válvula, al hacer doble clic, ¿qué nombres ves a la izquierda?  
Ejemplos típicos: Datos, Especificaciones técnicas, Asignación de variables, Documentación…

Con esa lista te digo el clic exacto en tu versión.
