from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LecturaDispositivo
from .serializers import LecturaDispositivoSerializer

class IngestaTelemetriaView(APIView):
    """
    Endpoint para recibir transmisiones de dispositivos médicos en la red 5G Edge.
    """
    def post(self, request, *args, **kwargs):
        serializer = LecturaDispositivoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "exitoso",
                "mensaje": f"Lectura recibida del dispositivo {serializer.data['dispositivo_id']}"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
