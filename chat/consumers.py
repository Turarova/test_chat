from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from channels.db import database_sync_to_async
from djangochannelsrestframework.observer import model_observer


from .models import *
from .serializers import MessageSerializer

class MessageConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    @action()
    async def create_message(self, message):
        await database_sync_to_async(Message.objects.create)(
            user = self.scope["user"],
            text = message
        )

    @model_observer(Message)
    async def send_message(self, message, observer=None):
        await self.send_json(message)
    