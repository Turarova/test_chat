from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from channels.db import database_sync_to_async
from djangochannelsrestframework.observer import model_observer
from datetime import datetime

from .models import *
from .serializers import MessageSerializer

class MessageConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    @action()
    async def create_message(self, message, **kwargs):
        user = await database_sync_to_async(User.objects.get)(
            id = kwargs["user"]
        )
        print("TYPE", message)
        await database_sync_to_async(Message.objects.create)(
            user = user,
            text = message
        )


    # @model_observer(Message)
    # async def send_message(self, message, observer=True, subscribing_request_ids=[299]):
    #     print('fwjfaofjoaiwjfioaj')
    #     for request_id in subscribing_request_ids:
    #         await self.send_json({"message": message, "request_id": request_id})

        # await self.send_json('fwafahoifhaiofhwfioahfoiahfoiahwfio')


    # @model_observer(Message)
    # async def send_message(self, message, observer=None):
    #     await self.send_json(message)


    # @send_message.serializer
    # def send_message(self, message, action, **kwargs):
    #     return dict(data=MessageSerializer(message), action=action.value, pk=message.pk)



    @model_observer(Message)
    async def send_message(
        self,
        message: MessageSerializer,
        observer=None,
        subscribing_request_ids=[],
        **kwargs
    ):
        print("EEEEEE", message)
        await self.send_json(dict(message))

    @send_message.serializer
    def return_message_serialier(self, instance: Message, action, **kwargs):
        """This will return the message serializer"""
        print("RRRRR", MessageSerializer(instance))
        return MessageSerializer(instance).data

    @action()
    async def subscribe_to_send_message(self, request_id, **kwargs):
        await self.send_message.subscribe(request_id=request_id)