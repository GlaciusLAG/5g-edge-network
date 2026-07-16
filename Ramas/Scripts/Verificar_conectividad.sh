#!/bin/bash

# Contenedores
SIMULADOR="simulador_dispositivos"
EDGE="edge_node"

echo "========================================="
echo " DIAGNÓSTICO DE CONECTIVIDAD ICMP"
echo "========================================="
echo

# Verificación Simulador -> Edge
echo -n "[$SIMULADOR -> $EDGE] "

docker exec $SIMULADOR ping -c 3 $EDGE > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "[OK] Comunicación establecida."
else
    echo "[FAIL] No hay respuesta."
fi

# Verificación Edge -> Simulador
echo -n "[$EDGE -> $SIMULADOR] "

docker exec $EDGE ping -c 3 $SIMULADOR > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "[OK] Comunicación establecida."
else
    echo "[FAIL] No hay respuesta."
fi

echo
echo "Diagnóstico finalizado."
