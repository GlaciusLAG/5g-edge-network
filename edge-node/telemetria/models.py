from django.db import models

class LecturaDispositivo(models.Model):
    dispositivo_id = models.CharField(max_length=100, help_text="ID o Hostname del contenedor/sensor")
    tipo_dispositivo = models.CharField(max_length=50, help_text="Ej: cardiograma, respirador, termómetro")
    datos_payload = models.JSONField(help_text="Lectura biométrica o métricas transmitidas en formato JSON")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_dispositivo} ({self.dispositivo_id}) - {self.timestamp}"
    
