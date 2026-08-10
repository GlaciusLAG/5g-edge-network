from django.urls import path
from .views import IngestaTelemetriaView

urlpatterns = [
    path('telemetria/', IngestaTelemetriaView.as_view(), name='ingesta_telemetria'),
]

