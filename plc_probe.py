"""
Diagnóstico snap7 → PLCSIM Advanced (Invalid address 0x05).

Uso:
  py plc_probe.py --ip 192.168.0.1

Prueba: conexión, Merker, DB1..DB10 con varios tamaños.
No usa Firebase.
"""

from __future__ import annotations

import argparse
import sys

try:
    import snap7
except ImportError:
    print("Falta python-snap7. Instala: py -m pip install python-snap7")
    sys.exit(1)


def _hint_dll(err: BaseException) -> None:
    msg = str(err).lower()
    if getattr(err, "winerror", None) == 2 or "no puede encontrar el archivo" in msg or "cannot find the file" in msg:
        print("   → Suele ser snap7.dll faltante. Ver docs/12_ARCHIVO_NO_ENCONTRADO_WINDOWS.md")
        print("     py -m pip install --upgrade python-snap7")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--ip", default="192.168.0.1")
    p.add_argument("--rack", type=int, default=0)
    p.add_argument("--slot", type=int, default=1)
    args = p.parse_args()

    try:
        client = snap7.client.Client()
    except Exception as e:
        print(f"❌ No pude crear cliente snap7: {e}")
        _hint_dll(e)
        sys.exit(1)
    try:
        client.set_connection_type(3)
    except Exception:
        pass
    print(f"Conectando a {args.ip} rack={args.rack} slot={args.slot} …")
    try:
        client.connect(args.ip, args.rack, args.slot)
    except Exception as e:
        print(f"❌ No conectó: {e}")
        _hint_dll(e)
        sys.exit(1)

    if not client.get_connected():
        print("❌ get_connected() = False")
        sys.exit(1)
    print("✅ Conectado.\n")

    # Merker: si esto falla, el problema es comunicación/protección, no el DB
    print("--- Merker %MB0 (2 bytes) ---")
    try:
        raw = client.mb_read(0, 2)
        print(f"  OK: {raw.hex()}")
    except Exception as e:
        print(f"  FAIL: {e}")
        print("  → Revisa PUT/GET descargado + instancia PLCSIM correcta.\n")

    sizes = [2, 4, 6, 7, 8, 12, 16, 20, 22, 24, 28, 32]
    print("\n--- Data Blocks DB1..DB10 ---")
    found = []
    for dbn in range(1, 11):
        ok_sizes = []
        last_err = None
        for sz in sizes:
            try:
                raw = client.db_read(dbn, 0, sz)
                ok_sizes.append(sz)
                _ = raw
            except Exception as e:
                last_err = e
                break
        if ok_sizes:
            mx = max(ok_sizes)
            found.append((dbn, mx))
            print(f"  DB{dbn}: OK hasta {mx} bytes  (DatosEstacion≥28, DB_HMI≥7)")
        else:
            print(f"  DB{dbn}: no legible  ({last_err})")

    print("\n=== Resultado ===")
    if not found:
        print("Ningún DB legible.")
        print("Causas típicas:")
        print("  1) El programa NO está descargado en ESTA instancia PLCSIM (IP).")
        print("  2) Los DB son Optimized ON (hay que OFF + download de nuevo).")
        print("  3) PUT/GET no quedó en la CPU de esa instancia (download hardware).")
        print("  4) Estás conectado a otra instancia / IP distinta a la del TIA online.")
        print("  Guía: plc_real/FIX_DB_INVALID_ADDRESS.md")
    else:
        print("DBs legibles:", ", ".join(f"DB{n}(≤{s}B)" for n, s in found))
        print()
        for n, s in found:
            if s >= 28:
                print(f"  candidato DatosEstacion: --db {n}  (tamaño OK ≥28)")
            elif s >= 22:
                print(f"  DB{n}: {s}B — candidato DatosEstacion PARCIAL (falta ContVidrio/PesoVidrio → ≥28)")
            elif s >= 7:
                print(f"  DB{n}: {s}B — si es DatosEstacion, falta ampliar (necesita ≥28)")
            if s >= 7:
                print(f"  candidato DB_HMI: --db-hmi {n}  (tamaño OK ≥7)")
            elif s > 0:
                print(f"  DB{n}: {s}B — si es DB_HMI, agrega PesoActualKg Real + byte 6 (necesita ≥7)")
        print()
        print("Si DB1 no aparece pero otro sí: en TIA el número del DB no es 1,")
        print("o DatosEstacion no se descargó. Mira en TIA el [DBx] al lado del nombre.")
        print("Guía: plc_real/FIX_DB_INVALID_ADDRESS.md")

    try:
        client.disconnect()
    except Exception:
        pass


if __name__ == "__main__":
    main()
