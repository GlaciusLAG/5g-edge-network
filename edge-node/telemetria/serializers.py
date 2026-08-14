from rest_framework import serializers
from .models import LecturaDispositivo, ArchivoTelemetria

class LecturaDispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturaDispositivo
        fields = ['id', 'dispositivo_id', 'tipo_dispositivo', 'datos_payload', 'timestamp_cliente', 'timestamp_recepcion']
        read_only_fields = ['id', 'timestamp_recepcion']


class ArchivoTelemetriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivoTelemetria
        fields = ['id', 'dispositivo_id', 'tipo_dispositivo', 'archivo', 'tamano_bytes', 'timestamp_subida']
        read_only_fields = ['id', 'tamano_bytes', 'timestamp_subida']