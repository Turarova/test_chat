from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Room(models.Model):
    TYPES = [
        ('GR', 'GROUP'),
        ('DM', 'DIRECT'),
    ]
    user = models.ManyToManyField(User, related_name='room')
    image = models.ImageField(null=True, upload_to='chat_images')
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=TYPES, null=True)


class Message(models.Model):
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

