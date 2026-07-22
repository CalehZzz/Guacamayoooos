# FAQ rápida — tags, LAD y offsets

## 1) Añadí `M_PulsePlastico`, `M_ResetAlarma` y `T_RetardoPiston` ¿está bien?

**Sí.** El mapa original no los listaba todos y los usábamos en las redes LAD.

Ejemplo válido:

| Tag | Dirección | Tipo |
|---|---|---|
| `M_PulsePlastico` | `%M0.6` | Bool |
| `M_ResetAlarma` | `%M0.7` | Bool |
| `T_RetardoPiston` | `%T0` (o IEC Timer) | Timer |

Solo asegúrate de que `%M0.6` / `%M0.7` **no estén ya usados** por otro tag.

## 2) ¿Qué significan las letras / rayas en las networks?

Son un **dibujo en texto** de la escalera. No se pegan en TIA.

- Inserta contactos y bobinas con la barra de herramientas LAD.
- En cada uno pon el **nombre del tag** (`I_Start`, `M_SistemaOn`…).
- `I_`, `Q_`, `M_` no son un “modo” aparte: van dentro del nombre.

## 3) `EstadoMaquina` me salió en offset 17.0 y `UltimoMaterial` en 17.1

**Eso no sirve para conectar la web.** Deben quedar:

- `EstadoMaquina` → tipo **Int**, offset **18.0**
- `UltimoMaterial` → tipo **Int**, offset **20.0**

Si ves `17.0` y `17.1`, casi seguro quedaron como **Bool**. Cámbialos a Int, confirma **Optimized block access = OFF**, recompila.
