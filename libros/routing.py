from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Esta ruta debe ser igual a la del fetch en el HTML
    re_path(r'ws/libros/$', consumers.LibroConsumer.as_asgi()),
]