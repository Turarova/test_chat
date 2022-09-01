from django.urls import re_path
from . import consumers
# from djangochannelsrestframework.consumers import 

websocket_urlpatterns = [
    re_path('ws/chat/', consumers.FullConsumer.as_asgi()),
]
