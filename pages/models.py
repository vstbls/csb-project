from django.db import models

class User(models.Model):
    username = models.TextField()
    password = models.TextField()
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='send_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()