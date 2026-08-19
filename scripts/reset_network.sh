#!/bin/bash
INTERFACE=${1:-eth0}

echo "[NETWORK] Eliminando reglas de tc/netem en $INTERFACE..."
tc qdisc del dev $INTERFACE root 2>/dev/null
echo "[NETWORK] Configuración de red restaurada a estado original."
tc qdisc show dev $INTERFACE
