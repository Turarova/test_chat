from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from channels.db import database_sync_to_async
from djangochannelsrestframework.observer import model_observer

from .models import *
from .serializers import MessageSerializer, RoomSerializer, UserSerializer

class FullConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    async def disconnect(self, code):
        if hasattr(self, "room_subscribe"):
            await self.remove_user_from_room(self.room_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.add_user_to_room(pk)
        await self.notify_users()

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)
    
    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'usuarios': await self.current_users(room)
                }
            )


    @action()
    async def create_message(self, message, **kwargs):
        """ Создаем сообщения и сохраняем в бд """
        room: Room = await self.get_room(pk=self.room_subscribe)
        user = await database_sync_to_async(User.objects.get)(
            id = kwargs["user"]
        )
        await database_sync_to_async(Message.objects.create)(
            room = room,
            user = user,
            text = message
        )


    @model_observer(Message)
    async def send_message(
        self,
        message: MessageSerializer,
        observer=None,
        subscribing_request_ids=[],
        **kwargs
    ):

        """ Отправляем сериализованные данные фронту """
        await self.send_json(dict(message))

    @send_message.serializer
    def return_message_serialier(self, instance: Message, action, **kwargs):
        """ Сериализуем сообщения """
        return MessageSerializer(instance).data

    @action()
    async def subscribe_to_send_message(self, request_id, **kwargs):
        """ Создаем action, чтобы на фронте 
            можно было обратиться к нашей вьюшке """
        await self.send_message.subscribe(request_id=request_id)




    @database_sync_to_async
    def remove_user_from_room(self, room):
        user: User = self.scope["user"]
        user.room.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        user: User = self.scope["user"]
        if not user.room.filter(pk=self.room_subscribe).exists():
            user.room.add(Room.objects.get(pk=pk))


    @database_sync_to_async
    def current_users(self, room: Room):
        return [UserSerializer(user).data for user in room.user.all()]


    @database_sync_to_async
    def get_room(self, pk: int) -> Room:
        return Room.objects.get(pk=pk)