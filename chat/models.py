from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    room_name = models.CharField(max_length = 200)

    def __str__(self):
        return f"{self.room_name}"
    

class Messages(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField(blank = True, null = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user} {self.content} {self.timestamp}"
    
    class Meta:
        ordering = ["timestamp"]