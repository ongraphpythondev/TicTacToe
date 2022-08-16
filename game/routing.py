from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/play/(?P<room_code>\w+)/$', consumers.TicTacToeConsumer.as_asgi()),
]