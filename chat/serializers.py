from rest_framework.serializers import ModelSerializer 
from django.contrib.auth import get_user_model

User = get_user_model()

from chat.models import Message, Room

class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'        


class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', ]