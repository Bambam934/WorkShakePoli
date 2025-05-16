# WorkShakePoli/asgi.py
import os
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth    import AuthMiddlewareStack
import achievements.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WorkShakePoli.settings")

django_asgi = get_asgi_application()

application = ProtocolTypeRouter({
    "http": ASGIStaticFilesHandler(django_asgi),      # ← este reemplaza al viejo StaticFilesWrapper
    "websocket": AuthMiddlewareStack(
        URLRouter(achievements.routing.websocket_urlpatterns)
    ),
})
