from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Article
from common.redis_client import redis_client
from .redis_keys import get_article_views_key

@receiver(post_delete,sender=Article)
def handle_article_post_delete(sender,instance,**kwargs):
    redis_client.delete(get_article_views_key(instance.id))