# tu_app_notificaciones/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/notificaciones/<int:user_id>/', consumers.NotificationConsumer.as_asgi()),
]
