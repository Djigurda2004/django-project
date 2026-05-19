from django.db import models
from articles.models import Article
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

class Comment(MPTTModel):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    parent = TreeForeignKey("self",on_delete=models.CASCADE,related_name='replies',blank=True,null=True)
    likes = models.ManyToManyField(User,related_name='liked_comments',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class MPTTMeta():
        order_insertion_by = ['created_at']