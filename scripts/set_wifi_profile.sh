#!/bin/bash
INTERFACE=${1:-eth0}

echo "[NETWORK] Aplicando Perfil Wi-Fi Convencional en la interfaz $INTERFACE..."
tc qdisc del dev $INTERFACE root 2>/dev/null
tc qdisc add dev $INTERFACE root netem delay 45ms 15ms loss 2%
echo "[NETWORK] Perfil Wi-Fi aplicado correctamente."
tc qdisc show dev $INTERFACE
