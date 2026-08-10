from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def estado_nodo(request):
    return JsonResponse({
        "sistema": "Nodo Edge Hospitalario 5G",
        "estado": "Operativo"
    })

urlpatterns = [
    path('', estado_nodo),
    path('admin/', admin.site.urls),
    path('api/', include('telemetria.urls')),
]