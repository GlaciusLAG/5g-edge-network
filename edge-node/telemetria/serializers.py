from rest_framework import serializers
from .models import LecturaDispositivo

class LecturaDispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturaDispositivo
        fields = ['id', 'dispositivo_id', 'tipo_dispositivo', 'datos_payload', 'timestamp']
        
        