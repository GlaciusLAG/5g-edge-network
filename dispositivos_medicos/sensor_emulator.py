import os
import time
import random
import socket
import asyncio
import httpx

# Carga de variables de entorno con fallbacks seguros
EDGE_URL_JSON = os.getenv("EDGE_URL_JSON", "http://edge_django:8000/api/telemetria/")
EDGE_URL_FILE = os.getenv("EDGE_URL_FILE", "http://edge_django:8000/api/telemetria/archivo/")
TIPO_DISPOSITIVO = os.getenv("TIPO_DISPOSITIVO", "cardiograma")
DISPOSITIVO_ID = os.getenv("HOSTNAME", socket.gethostname())

def generar_datos_biometricos():
    """Genera datos biométricos realistas según el tipo de dispositivo médico."""
    if TIPO_DISPOSITIVO == "cardiograma":
        return {
            "frecuencia_cardiaca_bpm": random.randint(60, 140),
            "ritmo": random.choice(["Normal", "Sinusal", "Arritmia leve"]),
            "spo2_porcentaje": random.randint(95, 100)
        }
    elif TIPO_DISPOSITIVO == "respirador":
        return {
            "presion_fio2": random.randint(21, 60),
            "frecuencia_respiratoria": random.randint(12, 30),
            "volumen_tidal_ml": random.randint(400, 600)
        }
    else:
        return {"lectura_generica": random.uniform(1.0, 100.0)}

async def esperar_disponibilidad_backend(client: httpx.AsyncClient):
    """Bucle de preparación (Health-Check) hasta que Django responda en la red."""
    print(f"[{DISPOSITIVO_ID}] Esperando disponibilidad del nodo Edge ({EDGE_URL_JSON})...", flush=True)
    while True:
        try:
            # Activamos follow_redirects=True por si Django redirige la URL con/sin diagonal final
            r = await client.get(EDGE_URL_JSON, follow_redirects=True)
            # Si el servidor responde con cualquier código < 500, sabemos que Django está activo
            if r.status_code == 200:
                print(f"[{DISPOSITIVO_ID}] Conexión establecida con el nodo Edge (HTTP {r.status_code}).", flush=True)
                break
            else:
                print(f"[{DISPOSITIVO_ID}] Servidor responde con error {r.status_code}. Reintentando...", flush=True)
        except Exception as e:
            print(f"[{DISPOSITIVO_ID}] Esperando red/Django ({e})...", flush=True)
            
        await asyncio.sleep(2.0)

async def transmitir_telemetria_continua():
    print(f"[{DISPOSITIVO_ID}] Iniciando emulador de {TIPO_DISPOSITIVO}...", flush=True)

    # Reutilizamos un cliente HTTP asíncrono con Pooling de conexiones habilitado
    async with httpx.AsyncClient(timeout=15.0) as client:
        await esperar_disponibilidad_backend(client)

        contador = 0
        while True:
            t1 = time.time()
            payload = {
                "dispositivo_id": DISPOSITIVO_ID,
                "tipo_dispositivo": TIPO_DISPOSITIVO,
                "datos_payload": generar_datos_biometricos(),
                "timestamp_cliente": t1
            }

            try:
                # 1. Enviar registro de telemetría ligero en JSON
                resp_json = await client.post(EDGE_URL_JSON, json=payload)
                if resp_json.status_code == 201:
                    print(f"[{DISPOSITIVO_ID}] JSON OK #{contador}", flush=True)
                else:
                    print(f"[{DISPOSITIVO_ID}] Error JSON {resp_json.status_code}: {resp_json.text}", flush=True)

                # 2. Enviar archivo pesado simulado (cada 5 envíos JSON)
                if contador % 5 == 0:
                    contenido_simulado = os.urandom(1024 * 10)  # 10 KB de datos binarios
                    files = {'archivo': ('ecg_trace.dcm', contenido_simulado, 'application/dicom')}
                    data = {'dispositivo_id': DISPOSITIVO_ID, 'tipo_dispositivo': TIPO_DISPOSITIVO}

                    resp_file = await client.post(EDGE_URL_FILE, data=data, files=files)
                    if resp_file.status_code == 201:
                        print(f"[{DISPOSITIVO_ID}] Archivo DICOM/ECG OK", flush=True)
                    else:
                        print(f"[{DISPOSITIVO_ID}] Error Archivo {resp_file.status_code}: {resp_file.text}", flush=True)

            except Exception as e:
                print(f"[{DISPOSITIVO_ID}] Error de red / transmisión: {e}", flush=True)

            contador += 1
            # Intervalo entre transmisiones
            await asyncio.sleep(3.0)

if __name__ == "__main__":
    asyncio.run(transmitir_telemetria_continua())