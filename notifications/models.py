from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']