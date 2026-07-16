"""
GUACAMAYOS — Simulador de PLC (Fase 1)
--------------------------------------------------------------------------
Este script reemplaza, por ahora, al lector real del PLC (snap7 + PLCSIM).
Escribe en Firestore exactamente el mismo documento que más adelante
escribirá el lector real, para que la app web no necesite ningún cambio
cuando conectes el PLC de verdad.

Contrato de datos (colección "sesiones_activas", 1 documento por estación):

    sesiones_activas/{estacionId}
    {
        "materiales": {
            "plastico": {"piezas": int, "pesoKg": float},
            "carton":   {"piezas": int, "pesoKg": float},
            "aluminio": {"piezas": int, "pesoKg": float}
        },
        "finalizada": bool,   # true = el operador/PLC marcó fin de sesión
        "actualizado": <timestamp servidor>
    }

La app web (index.html) crea este documento en ceros cuando el usuario
presiona "Iniciar" en una estación, y luego solo ESCUCHA los cambios
(onSnapshot). Este script es quien va sumando piezas/peso con el tiempo.

--------------------------------------------------------------------------
CÓMO CORRERLO
--------------------------------------------------------------------------
1. pip install firebase-admin
2. En la consola de Firebase: Configuración del proyecto > Cuentas de
   servicio > "Generar nueva clave privada". Descarga el JSON y ponlo
   junto a este script como "serviceAccountKey.json" (NO lo subas a git).
3. Desde el navegador, entra a Guacamayos, abre una estación con
   "Iniciar" (esto crea el documento en ceros).
4. Corre: python plc_simulador.py <id_de_la_estacion>
   Ejemplo: python plc_simulador.py parque-central
   (el id_de_la_estacion es el mismo "id" que usan tus documentos en la
   colección "estaciones" de Firestore).
5. Verás cómo la app web se actualiza sola, en tiempo real, sin recargar.
6. Presiona ENTER en la terminal en cualquier momento para simular el
   botón de "fin de sesión" del PLC.

--------------------------------------------------------------------------
CUANDO CONECTES EL PLC REAL (snap7)
--------------------------------------------------------------------------
Solo tienes que reemplazar la función `leer_datos_del_plc()` de más abajo
por una lectura real del DB del PLC vía snap7, por ejemplo:

    import snap7
    plc = snap7.client.Client()
    plc.connect("127.0.0.1", 0, 1)  # IP, rack, slot (NetToPLCSim / PLCSIM Advanced)
    data = plc.db_read(DB_NUMBER, START, SIZE)
    piezas_plastico = snap7.util.get_int(data, 0)
    peso_plastico   = snap7.util.get_real(data, 2)
    ...
    fin_de_sesion = snap7.util.get_bool(data, N, 0)  # bit que activa el PLC

El resto del script (la parte que escribe a Firestore) no cambia nada.
"""

import sys
import threading
import time
import random

import firebase_admin
from firebase_admin import credentials, firestore

# ---------------------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------------------
SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"
INTERVALO_SEGUNDOS = 1.1  # qué tan seguido "llegan" piezas nuevas

MATERIALES = {
    "plastico": {"peso_min": 0.02, "peso_max": 0.06},
    "carton":   {"peso_min": 0.05, "peso_max": 0.18},
    "aluminio": {"peso_min": 0.01, "peso_max": 0.03},
}

# ---------------------------------------------------------------------
# ESTADO GLOBAL DE LA SIMULACIÓN (en la fase real, esto seria simplemente
# lo último leído del DB del PLC en cada ciclo)
# ---------------------------------------------------------------------
acumulado = {key: {"piezas": 0, "pesoKg": 0.0} for key in MATERIALES}
fin_de_sesion_solicitado = False


def escuchar_tecla_enter():
    """Corre en un hilo aparte: al presionar ENTER, simula que el PLC
    marcó el fin de la sesión (más adelante esto sería un bit del DB)."""
    global fin_de_sesion_solicitado
    input()  # espera un ENTER
    fin_de_sesion_solicitado = True
    print("\n🔴 Fin de sesión solicitado (simulado). Cerrando en el próximo ciclo...")


def leer_datos_del_plc():
    """
    FASE 1 (actual): genera datos aleatorios, igual que hacía antes la
    función simulateTick() del navegador.

    FASE 2 (futura): aquí van las llamadas reales a snap7 (ver docstring
    del archivo). Debe devolver una tupla (acumulado_actualizado, fin_de_sesion).
    """
    key = random.choice(list(MATERIALES.keys()))
    mat = MATERIALES[key]
    incremento = random.uniform(mat["peso_min"], mat["peso_max"])

    acumulado[key]["piezas"] += 1
    acumulado[key]["pesoKg"] = round(acumulado[key]["pesoKg"] + incremento, 4)

    return acumulado, fin_de_sesion_solicitado


def main():
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
        print(f"⚠️  No existe sesiones_activas/{estacion_id} todavía.")
        print("    Abre la estación en la app web con 'Iniciar' antes de correr este script.")
        sys.exit(1)

    print(f"✅ Conectado. Simulando PLC para la estación: {estacion_id}")
    print("   Presiona ENTER en cualquier momento para terminar la sesión.\n")

    threading.Thread(target=escuchar_tecla_enter, daemon=True).start()

    while True:
        datos, fin = leer_datos_del_plc()

        doc_ref.set({
            "materiales": datos,
            "finalizada": fin,
            "actualizado": firestore.SERVER_TIMESTAMP,
        }, merge=True)

        resumen = ", ".join(
            f"{k}: {v['piezas']}pz/{v['pesoKg']:.2f}kg" for k, v in datos.items()
        )
        print(f"→ {resumen}" + (" [FINALIZADA]" if fin else ""))

        if fin:
            break

        time.sleep(INTERVALO_SEGUNDOS)

    print("\n✅ Sesión marcada como finalizada. La app web debería guardar el registro sola.")


if __name__ == "__main__":
    main()
