import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import simulation.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wall_e.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(simulation.routing.websocket_urlpatterns)
    ),
})
