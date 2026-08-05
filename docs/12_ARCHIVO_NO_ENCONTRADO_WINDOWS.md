# “El sistema no puede encontrar el archivo especificado” (Windows)

Ese mensaje es **WinError 2**. Casi nunca significa que el archivo “no esté” en el Explorador: Python o Windows buscan **otra ruta** u **otro archivo** (a menudo `snap7.dll`).

---

## Caso A — `serviceAccountKey.json` (sí lo ves, pero falla)

El JSON debe estar en la **raíz del repo** (junto a `plc_bridge.py`), no solo en `Downloads` o en `plc_real/`.

En PowerShell:

```powershell
cd RUTA\A\TU\REPO\SIBU
dir serviceAccountKey.json
dir plc_bridge.py
py plc_real\plc_bridge_real.py --ip 192.168.0.10
```

Si `dir serviceAccountKey.json` falla → no está en esa carpeta (aunque lo veas en otra ventana).

El bridge ahora imprime `CWD=…` y `🔑 Firebase key: …` para que veas qué ruta usó.

---

## Caso B — `snap7.dll` (el más frecuente con ese texto exacto)

`pip install python-snap7` instala el wrapper Python; Windows aún necesita la DLL nativa.

```powershell
py -m pip install --upgrade python-snap7
py -c "import snap7, os; print(os.path.dirname(snap7.__file__))"
```

Abre esa carpeta. Si no hay `snap7.dll` (a veces está en `lib\` o hay que bajarlo del [proyecto Snap7](https://sourceforge.net/projects/snap7/)):

1. Copia `snap7.dll` (64-bit si tu Python es 64-bit) a la carpeta de `snap7`, **o**
2. Cópiala a la carpeta desde donde corres el bridge, **o**
3. Agrégala a una carpeta que esté en el **PATH**.

Cierra y vuelve a abrir la terminal.

Prueba sin Firebase:

```powershell
py plc_probe.py --ip 192.168.0.10
```

Si el probe conecta, snap7 está OK.

---

## Caso C — Corres el `.py` con doble clic / desde otra carpeta

No uses doble clic. Abre terminal en la raíz:

```powershell
cd RUTA\A\TU\REPO\SIBU
py plc_real\plc_bridge_real.py --ip 192.168.0.10
```

o el launcher:

```powershell
.\run_bridge_real.bat 192.168.0.10
```

---

## Qué archivo NO es

| Ves esto | No es esto |
|---|---|
| `serviceAccountKey.json` | `snap7.dll` |
| `FIX_DB_INVALID_ADDRESS.md` | No lo ejecuta el bridge |
| Script en `plc_real\` | La key va en la **raíz**, no obligatoriamente en `plc_real\` |
