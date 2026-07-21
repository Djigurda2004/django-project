from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls.base import reverse

class User(AbstractUser):
    email = models.EmailField(max_length=255,unique=True,blank=False)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/",blank=True)
    followers = models.ManyToManyField("self",related_name="following",symmetrical=False,blank=True)

    
    def get_absolute_url(self):
        return reverse('users:profile',username=self.username)