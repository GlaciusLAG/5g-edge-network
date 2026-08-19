#!/bin/bash
INTERFACE=${1:-eth0}

echo "[NETWORK] Aplicando Perfil 5G Edge en la interfaz $INTERFACE..."
tc qdisc del dev $INTERFACE root 2>/dev/null
tc qdisc add dev $INTERFACE root netem delay 2ms 1ms loss 0.01%
echo "[NETWORK] Perfil 5G Edge aplicado correctamente."
tc qdisc show dev $INTERFACE
