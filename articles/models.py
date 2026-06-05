from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField('Name',max_length=50)
    announcement = models.CharField('Announcement',max_length=250)
    full_text= models.TextField('Full text')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="articles",)
    likes = models.ManyToManyField(User, related_name="liked_articles", blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Article: {self.title}'
    
    def get_absolute_url (self):
        return f'/articles/{self.id}'
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_at']