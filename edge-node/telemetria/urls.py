from django.urls import path
from .views import IngestaTelemetriaView, IngestaArchivoView

urlpatterns = [
    path('telemetria/', IngestaTelemetriaView.as_view(), name='ingesta_telemetria'),
    path('telemetria/archivo/', IngestaArchivoView.as_view(), name='ingesta_archivo'),
]