from rest_framework.serializers import ModelSerializer 

from chat.models import Message, Room

class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'

