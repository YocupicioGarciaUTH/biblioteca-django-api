import os
from django.core.asgi import get_asgi_application

# 1. Configuramos el entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_project.settings')

# 2. ¡INICIALIZAMOS DJANGO PRIMERO! (Esto soluciona el error)
django_asgi_app = get_asgi_application()

# 3. AHORA SÍ importamos Channels y nuestras rutas
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import libros.routing

# 4. Definimos el enrutador
application = ProtocolTypeRouter({
    # Usamos la variable que inicializamos arriba
    "http": django_asgi_app,
    
    # Manejo de WebSockets
    "websocket": AuthMiddlewareStack(
        URLRouter(
            libros.routing.websocket_urlpatterns
        )
    ),
})