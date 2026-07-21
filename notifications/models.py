from django.db import models
from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notification(models.Model):
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    type = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,blank=True,null=True)
    object_id = models.PositiveIntegerField(blank=True,null=True)
    content_object = GenericForeignKey('content_type','object_id')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']