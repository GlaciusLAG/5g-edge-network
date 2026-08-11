#!/bin/bash
set -e

echo "Esperando conexión con PostgreSQL ($DB_HOST:$DB_PORT)..."

python -c "
import socket, time, os
host = os.getenv('DB_HOST', 'nodo_edge_postgres')
port = int(os.getenv('DB_PORT', 5432))
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        s.close()
        print('¡PostgreSQL está respondiendo!')
        break
    except Exception:
        time.sleep(1)
"

echo "Iniciando servidor de desarrollo de Django..."
exec "$@"
