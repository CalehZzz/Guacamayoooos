"""
GUACAMAYOS — Bridge bidireccional
  Firestore hmi_comandos → DB_HMI (PLC)
  DatosEstacion (PLC) → Firestore sesiones_activas

CPU objetivo: 1511C-1 PN en S7-PLCSIM Advanced V7 (snap7 a la IP de la instancia).

  pip install firebase-admin python-snap7
  python plc_bridge.py parque-central --ip 192.168.0.1 --db 1 --db-hmi 3
"""

from __future__ import annotations

import argparse
import sys
import time

import firebase_admin
from firebase_admin import credentials, firestore

try:
    import snap7
    from snap7.util import get_bool, get_int, get_real, set_bool, set_real
except ImportError:
    print("Falta python-snap7. Instala con: pip install python-snap7")
    sys.exit(1)


SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"
DB_READ_SIZE = 24
DB_HMI_SIZE = 8

ESTADO_TXT = {0: "idle", 1: "running", 2: "clasificando", 3: "alarma", 4: "emergencia"}
MATERIAL_TXT = {0: None, 1: "plastico", 2: "aluminio"}

BOOL_MAP = [
    # (firestore_key, byte, bit)
    ("Start", 0, 0),
    ("Stop", 0, 1),
    ("Emergencia", 0, 2),
    ("ResetAlarma", 0, 3),
    ("ModoAuto", 0, 4),
    ("FinSesion", 0, 5),
    ("ManualBanda", 0, 6),
    ("ManualPiston", 0, 7),
    ("BasculaLista", 1, 0),
    ("SensorPieza", 1, 1),
    ("SensorPlastico", 1, 2),
    ("SensorAluminio", 1, 3),
    ("PistonRetractado", 1, 4),
    ("PistonExtendido", 1, 5),
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Bridge Guacamayos HMI↔PLC↔Firestore")
    p.add_argument("estacion_id", help="ID estación Firestore")
    p.add_argument("--ip", default="192.168.0.1", help="IP instancia PLCSIM Advanced")
    p.add_argument("--rack", type=int, default=0)
    p.add_argument("--slot", type=int, default=1)
    p.add_argument("--db", type=int, default=1, help="DB DatosEstacion")
    p.add_argument("--db-hmi", type=int, default=3, help="DB_HMI comandos")
    p.add_argument("--interval", type=float, default=0.35)
    p.add_argument("--reset-on-start", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-hmi-write", action="store_true", help="Solo lee PLC, no escribe DB_HMI")
    return p.parse_args()


def conectar_plc(ip: str, rack: int, slot: int) -> snap7.client.Client:
    client = snap7.client.Client()
    client.connect(ip, rack, slot)
    if not client.get_connected():
        raise RuntimeError(f"No conectó a {ip} r{rack}s{slot}")
    return client


def leer_datos_estacion(client: snap7.client.Client, db_number: int) -> dict:
    raw = client.db_read(db_number, 0, DB_READ_SIZE)
    estado = get_int(raw, 18)
    ultimo = get_int(raw, 20)
    return {
        "materiales": {
            "plastico": {"piezas": int(get_int(raw, 0)), "pesoKg": round(float(get_real(raw, 4)), 4)},
            "aluminio": {"piezas": int(get_int(raw, 2)), "pesoKg": round(float(get_real(raw, 8)), 4)},
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


def escribir_db_hmi(client: snap7.client.Client, db_hmi: int, cmd: dict) -> None:
    raw = bytearray(DB_HMI_SIZE)
    for key, byte, bit in BOOL_MAP:
        set_bool(raw, byte, bit, bool(cmd.get(key, False)))
    peso = cmd.get("PesoActualKg", 0.0)
    try:
        peso = float(peso)
    except (TypeError, ValueError):
        peso = 0.0
    set_real(raw, 4, peso)
    client.db_write(db_hmi, 0, raw)


def reset_sesion_en_plc(client: snap7.client.Client, db_number: int) -> None:
    from snap7.util import set_int

    raw = bytearray(client.db_read(db_number, 0, DB_READ_SIZE))
    set_int(raw, 0, 0)
    set_int(raw, 2, 0)
    set_real(raw, 4, 0.0)
    set_real(raw, 8, 0.0)
    set_real(raw, 12, 0.0)
    set_bool(raw, 16, 0, True)
    set_bool(raw, 16, 1, False)
    set_int(raw, 20, 0)
    client.db_write(db_number, 0, raw)
    print("↺ DatosEstacion reiniciado.")


def main() -> None:
    args = parse_args()
    print(f"PLC {args.ip} r{args.rack}s{args.slot} | DatosEstacion=DB{args.db} | DB_HMI=DB{args.db_hmi}")

    try:
        plc = conectar_plc(args.ip, args.rack, args.slot)
    except Exception as e:
        print("❌ snap7 no conectó. ¿PLCSIM Advanced RUN? ¿IP de la instancia correcta?")
        print(f"   {e}")
        sys.exit(1)
    print("✅ PLC conectado.")

    if args.reset_on_start:
        try:
            reset_sesion_en_plc(plc, args.db)
        except Exception as e:
            print(f"⚠️  reset: {e}")

    cmd_ref = None
    sesion_ref = None
    if not args.dry_run:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred)
        fs = firestore.client()
        sesion_ref = fs.collection("sesiones_activas").document(args.estacion_id)
        cmd_ref = fs.collection("hmi_comandos").document(args.estacion_id)
        if not sesion_ref.get().exists:
            sesion_ref.set({
                "materiales": {
                    "plastico": {"piezas": 0, "pesoKg": 0.0},
                    "aluminio": {"piezas": 0, "pesoKg": 0.0},
                },
                "finalizada": False,
                "plc": {"conectado": False},
                "actualizado": firestore.SERVER_TIMESTAMP,
            })
            print(f"📄 Creado sesiones_activas/{args.estacion_id}")
        print(f"✅ Firestore: sesiones_activas + hmi_comandos / {args.estacion_id}")
    else:
        print("dry-run: sin Firebase")

    print("Loop… Ctrl+C sale.\n")
    try:
        while True:
            # 1) HMI web → PLC
            if not args.dry_run and not args.no_hmi_write and cmd_ref is not None:
                try:
                    snap = cmd_ref.get()
                    if snap.exists:
                        escribir_db_hmi(plc, args.db_hmi, snap.to_dict() or {})
                except Exception as e:
                    print(f"⚠️  escritura DB_HMI: {e}")

            # 2) PLC → web
            try:
                payload = leer_datos_estacion(plc, args.db)
            except Exception as e:
                print(f"⚠️  lectura DatosEstacion: {e}")
                time.sleep(1.0)
                continue

            m = payload["materiales"]
            st = payload["plc"]
            print(
                f"→ P:{m['plastico']['piezas']}/{m['plastico']['pesoKg']:.3f} "
                f"A:{m['aluminio']['piezas']}/{m['aluminio']['pesoKg']:.3f} "
                f"{st['estado']} B={int(st['banda'])} P={int(st['piston'])}"
                + (" FIN" if payload["finalizada"] else "")
            )

            if not args.dry_run and sesion_ref is not None:
                sesion_ref.set(
                    {
                        "materiales": payload["materiales"],
                        "finalizada": payload["finalizada"],
                        "plc": payload["plc"],
                        "actualizado": firestore.SERVER_TIMESTAMP,
                    },
                    merge=True,
                )

            if payload["finalizada"]:
                print("\n✅ FinSesion en PLC.")
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStop.")
    finally:
        try:
            plc.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    main()
