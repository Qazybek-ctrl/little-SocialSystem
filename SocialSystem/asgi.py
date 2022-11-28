import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from chatsystem.consumers import ChatConsumer

django_asgi_app = get_asgi_application()

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialSystem.settings')

from django.urls import path
from chatsystem.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path('messages/<slug>/', ChatConsumer.as_asgi())
                ]
            )
        )
    )
})