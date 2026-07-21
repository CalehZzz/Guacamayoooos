"""
GUACAMAYOS — Simulador de PLC (sin TIA / sin snap7)
--------------------------------------------------------------------------
Escribe en Firestore el MISMO contrato que plc_bridge.py, para que puedas
desarrollar y demostrar la app web mientras terminas el programa en TIA.

Contrato: sesiones_activas/{estacionId}
  - materiales.plastico / materiales.aluminio
  - finalizada
  - plc { conectado, sistemaOn, modoAuto, ... }

Uso:
  1. pip install firebase-admin
  2. serviceAccountKey.json en esta carpeta
  3. En la app: Conectar a la estación
  4. python plc_simulador.py parque-central
  5. ENTER = fin de sesión
"""

from __future__ import annotations

import random
import sys
import threading
import time

import firebase_admin
from firebase_admin import credentials, firestore

SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"
INTERVALO_SEGUNDOS = 1.2

MATERIALES = {
    "plastico": {"peso_min": 0.02, "peso_max": 0.06},
    "aluminio": {"peso_min": 0.01, "peso_max": 0.03},
}

acumulado = {key: {"piezas": 0, "pesoKg": 0.0} for key in MATERIALES}
fin_de_sesion_solicitado = False
ultimo_material = None
piston_pulse = False


def escuchar_tecla_enter() -> None:
    global fin_de_sesion_solicitado
    input()
    fin_de_sesion_solicitado = True
    print("\nFin de sesión solicitado (simulado).")


def tick() -> dict:
    global ultimo_material, piston_pulse
    key = random.choice(list(MATERIALES.keys()))
    mat = MATERIALES[key]
    incremento = random.uniform(mat["peso_min"], mat["peso_max"])

    acumulado[key]["piezas"] += 1
    acumulado[key]["pesoKg"] = round(acumulado[key]["pesoKg"] + incremento, 4)
    ultimo_material = key
    piston_pulse = key == "aluminio"

    return {
        "materiales": {
            "plastico": dict(acumulado["plastico"]),
            "aluminio": dict(acumulado["aluminio"]),
        },
        "finalizada": fin_de_sesion_solicitado,
        "plc": {
            "conectado": True,
            "sistemaOn": True,
            "modoAuto": True,
            "emergencia": False,
            "alarma": False,
            "banda": True,
            "piston": piston_pulse,
            "estado": "clasificando" if piston_pulse else "running",
            "ultimoMaterial": ultimo_material,
            "pesoActualKg": round(incremento, 4),
            "sesionActiva": True,
        },
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python plc_simulador.py <id_de_la_estacion>")
        print("Ejemplo: python plc_simulador.py parque-central")
        sys.exit(1)

    estacion_id = sys.argv[1]
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    doc_ref = db.collection("sesiones_activas").document(estacion_id)

    if not doc_ref.get().exists:
        print(f"No existe sesiones_activas/{estacion_id}.")
        print("Abre la estación en la app con 'Conectar' antes de correr este script.")
        sys.exit(1)

    print(f"Simulando PLC para estación: {estacion_id}")
    print("ENTER = terminar sesión\n")
    threading.Thread(target=escuchar_tecla_enter, daemon=True).start()

    while True:
        payload = tick()
        doc_ref.set(
            {
                **payload,
                "actualizado": firestore.SERVER_TIMESTAMP,
            },
            merge=True,
        )
        m = payload["materiales"]
        print(
            f"→ P:{m['plastico']['piezas']}pz/{m['plastico']['pesoKg']:.3f}kg  "
            f"A:{m['aluminio']['piezas']}pz/{m['aluminio']['pesoKg']:.3f}kg"
            + (" [FINALIZADA]" if payload["finalizada"] else "")
        )
        if payload["finalizada"]:
            break
        time.sleep(INTERVALO_SEGUNDOS)

    print("\nSesión finalizada. La app web debería guardar sola.")


if __name__ == "__main__":
    main()
