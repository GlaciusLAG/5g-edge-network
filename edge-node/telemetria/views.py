import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
import redis

from .models import LecturaDispositivo, ArchivoTelemetria
from .serializers import LecturaDispositivoSerializer, ArchivoTelemetriaSerializer

# Conexión al nodo de caché Redis
redis_client = redis.Redis(
    host=getattr(settings, 'REDIS_HOST', 'nodo_edge_redis'),
    port=int(getattr(settings, 'REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

class IngestaTelemetriaView(APIView):
    """
    Endpoint para recibir transmisiones ligeras (JSON) de dispositivos médicos.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    parser_classes = (JSONParser,)

    def get(self, request, *args, **kwargs):
        """Health-check para que los clientes reconozcan que el endpoint está arriba."""
        return Response({"status": "activo", "mensaje": "API Telemetría 5G Edge operativa"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = LecturaDispositivoSerializer(data=request.data)
        if serializer.is_valid():
            lectura = serializer.save()

            # Guardar la última lectura recibida en caché Redis (TTL 1 hora)
            cache_key = f"dispositivo:{lectura.dispositivo_id}:ultimo"
            payload_cache = {
                "dispositivo_id": lectura.dispositivo_id,
                "tipo_dispositivo": lectura.tipo_dispositivo,
                "datos_payload": lectura.datos_payload,
                "timestamp_cliente": lectura.timestamp_cliente,
                "timestamp_recepcion": lectura.timestamp_recepcion.isoformat()
            }
            try:
                redis_client.set(cache_key, json.dumps(payload_cache), ex=3600)
            except Exception as e:
                print(f"[REDIS ERROR] No se pudo guardar en caché: {e}")

            return Response({
                "status": "exitoso",
                "mensaje": f"Lectura registrada para {lectura.dispositivo_id}",
                "id": lectura.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngestaArchivoView(APIView):
    """
    Endpoint para recibir archivos pesados (DICOM, ECG binarios).
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        archivo_obj = request.FILES.get('archivo')
        if not archivo_obj:
            return Response({"error": "No se proporcionó ningún archivo"}, status=status.HTTP_400_BAD_REQUEST)

        dispositivo_id = request.data.get('dispositivo_id', 'desconocido')
        tipo_dispositivo = request.data.get('tipo_dispositivo', 'generico')

        archivo_record = ArchivoTelemetria.objects.create(
            dispositivo_id=dispositivo_id,
            tipo_dispositivo=tipo_dispositivo,
            archivo=archivo_obj,
            tamano_bytes=archivo_obj.size
        )

        return Response({
            "status": "exitoso",
            "mensaje": f"Archivo de {archivo_obj.size} bytes subido exitosamente",
            "id": str(archivo_record.id)
        }, status=status.HTTP_201_CREATED)