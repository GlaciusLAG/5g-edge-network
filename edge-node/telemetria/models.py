import uuid
from django.db import models

class LecturaDispositivo(models.Model):
    dispositivo_id = models.CharField(max_length=100, db_index=True)
    tipo_dispositivo = models.CharField(max_length=50)
    datos_payload = models.JSONField()
    timestamp_cliente = models.FloatField(null=True, blank=True)
    timestamp_recepcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp_recepcion']

    def __str__(self):
        return f"{self.tipo_dispositivo} ({self.dispositivo_id}) - {self.timestamp_recepcion}"


class ArchivoTelemetria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dispositivo_id = models.CharField(max_length=100, db_index=True)
    tipo_dispositivo = models.CharField(max_length=50)
    archivo = models.FileField(upload_to='telemetria_files/%Y/%m/%d/')
    tamano_bytes = models.BigIntegerField()
    timestamp_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp_subida']

    def __str__(self):
        return f"Archivo {self.id} de {self.dispositivo_id}"