# myapp/models.py
from django.db import models
from django.contrib.auth.models import User
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='nexusapp_sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='nexusapp_received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.subject}"