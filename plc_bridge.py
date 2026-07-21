"""
GUACAMAYOS — Bridge PLC virtual (PLCSIM) → Firestore
--------------------------------------------------------------------------
Lee el Data Block `DatosEstacion` (DB1) del PLC Siemens vía snap7 y publica
el mismo documento que consume index.html:

    sesiones_activas/{estacionId}

Requisitos:
  pip install firebase-admin python-snap7

Antes de correr:
  1. TIA Portal: PLCSIM en RUN, DB con Optimized access OFF, PUT/GET ON
  2. NetToPLCSim (o PLCSIM Advanced) escuchando
  3. En la app web: pulsar "Conectar" en la estación (crea el doc en ceros)
  4. serviceAccountKey.json junto a este script

Uso:
  python plc_bridge.py parque-central
  python plc_bridge.py parque-central --ip 127.0.0.1 --db 1 --reset-on-start
  python plc_bridge.py parque-central --dry-run
"""

from __future__ import annotations

import argparse
import struct
import sys
import time

import firebase_admin
from firebase_admin import credentials, firestore

try:
    import snap7
    from snap7.util import get_bool, get_int, get_real, set_bool, set_int, set_real
except ImportError:
    print("Falta python-snap7. Instala con: pip install python-snap7")
    sys.exit(1)


SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"
DB_READ_SIZE = 24  # bytes (ver tia/MAPA_IO_Y_DB.md)

ESTADO_TXT = {
    0: "idle",
    1: "running",
    2: "clasificando",
    3: "alarma",
    4: "emergencia",
}

MATERIAL_TXT = {
    0: None,
    1: "plastico",
    2: "aluminio",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Bridge Guacamayos PLC → Firestore")
    p.add_argument("estacion_id", help="ID de la estación (doc Firestore)")
    p.add_argument("--ip", default="127.0.0.1", help="IP del PLC / NetToPLCSim")
    p.add_argument("--rack", type=int, default=0)
    p.add_argument("--slot", type=int, default=1)
    p.add_argument("--db", type=int, default=1, help="Número del Data Block")
    p.add_argument("--interval", type=float, default=0.4, help="Segundos entre lecturas")
    p.add_argument("--reset-on-start", action="store_true",
                   help="Pone contadores/pesos en 0 y SesionActiva=1 al conectar")
    p.add_argument("--dry-run", action="store_true",
                   help="Solo imprime lecturas, no escribe Firebase")
    return p.parse_args()


def conectar_plc(ip: str, rack: int, slot: int) -> snap7.client.Client:
    client = snap7.client.Client()
    client.connect(ip, rack, slot)
    if not client.get_connected():
        raise RuntimeError(f"No se pudo conectar al PLC en {ip} rack={rack} slot={slot}")
    return client


def leer_db(client: snap7.client.Client, db_number: int) -> dict:
    raw = client.db_read(db_number, 0, DB_READ_SIZE)
    estado = get_int(raw, 18)
    ultimo = get_int(raw, 20)
    return {
        "materiales": {
            "plastico": {
                "piezas": int(get_int(raw, 0)),
                "pesoKg": round(float(get_real(raw, 4)), 4),
            },
            "aluminio": {
                "piezas": int(get_int(raw, 2)),
                "pesoKg": round(float(get_real(raw, 8)), 4),
            },
        },
        "finalizada": bool(get_bool(raw, 16, 1)),
        "plc": {
            "conectado": True,
            "sistemaOn": bool(get_bool(raw, 16, 2)),
            "modoAuto": bool(get_bool(raw, 16, 3)),
            "emergencia": bool(get_bool(raw, 16, 4)),
            "alarma": bool(get_bool(raw, 16, 5)),
            "banda": bool(get_bool(raw, 16, 6)),
            "piston": bool(get_bool(raw, 16, 7)),
            "estado": ESTADO_TXT.get(estado, "idle"),
            "ultimoMaterial": MATERIAL_TXT.get(ultimo),
            "pesoActualKg": round(float(get_real(raw, 12)), 4),
            "sesionActiva": bool(get_bool(raw, 16, 0)),
        },
    }


def reset_sesion_en_plc(client: snap7.client.Client, db_number: int) -> None:
    """Limpia contadores y marca SesionActiva=1, FinSesion=0."""
    raw = bytearray(client.db_read(db_number, 0, DB_READ_SIZE))
    set_int(raw, 0, 0)   # ContPlastico
    set_int(raw, 2, 0)   # ContAluminio
    set_real(raw, 4, 0.0)
    set_real(raw, 8, 0.0)
    set_real(raw, 12, 0.0)
    set_bool(raw, 16, 0, True)   # SesionActiva
    set_bool(raw, 16, 1, False)  # FinSesion
    set_int(raw, 20, 0)          # UltimoMaterial
    client.db_write(db_number, 0, raw)
    print("↺ Contadores del PLC reiniciados (SesionActiva=1).")


def publicar(doc_ref, payload: dict) -> None:
    doc_ref.set(
        {
            "materiales": payload["materiales"],
            "finalizada": payload["finalizada"],
            "plc": payload["plc"],
            "actualizado": firestore.SERVER_TIMESTAMP,
        },
        merge=True,
    )


def main() -> None:
    args = parse_args()

    print(f"Conectando a PLC {args.ip} (rack {args.rack}, slot {args.slot}), DB{args.db}...")
    try:
        plc = conectar_plc(args.ip, args.rack, args.slot)
    except Exception as e:
        print("❌ No se pudo abrir snap7.")
        print("   ¿PLCSIM en RUN? ¿NetToPLCSim Start Server? ¿IP/rack/slot correctos?")
        print(f"   Detalle: {e}")
        sys.exit(1)
    print("✅ PLC conectado.")

    if args.reset_on_start:
        try:
            reset_sesion_en_plc(plc, args.db)
        except Exception as e:
            print(f"⚠️  No se pudo resetear el DB: {e}")

    db = None
    doc_ref = None
    if not args.dry_run:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        doc_ref = db.collection("sesiones_activas").document(args.estacion_id)
        if not doc_ref.get().exists:
            print(f"⚠️  No existe sesiones_activas/{args.estacion_id}.")
            print("    Abre la app y pulsa Conectar en esa estación, luego vuelve a correr.")
            plc.disconnect()
            sys.exit(1)
        print(f"✅ Firestore listo → sesiones_activas/{args.estacion_id}")
    else:
        print("modo --dry-run: no se escribe Firebase")

    print("Leyendo... Ctrl+C para salir.\n")
    try:
        while True:
            try:
                payload = leer_db(plc, args.db)
            except Exception as e:
                print(f"⚠️  Error de lectura: {e}. Reintentando...")
                time.sleep(1.0)
                continue

            mat = payload["materiales"]
            plc_st = payload["plc"]
            print(
                f"→ P:{mat['plastico']['piezas']}pz/{mat['plastico']['pesoKg']:.3f}kg  "
                f"A:{mat['aluminio']['piezas']}pz/{mat['aluminio']['pesoKg']:.3f}kg  "
                f"estado={plc_st['estado']} banda={int(plc_st['banda'])} "
                f"piston={int(plc_st['piston'])}"
                + (" [FIN SESIÓN]" if payload["finalizada"] else "")
            )

            if not args.dry_run:
                publicar(doc_ref, payload)

            if payload["finalizada"]:
                print("\n✅ PLC marcó FinSesion. La app debería cerrar y guardar sola.")
                break

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
    finally:
        try:
            plc.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    # struct import kept for posibles extensiones de packing
    _ = struct
    main()
