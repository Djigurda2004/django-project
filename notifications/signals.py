from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import Notification
from articles.models import Article
from comments.models import Comment
from users.models import Profile
from django.contrib.auth.models import User
from .tasks import all_followers_notification_task

@receiver(post_save,sender=Article)
def notify_on_article_create(sender,instance,created,**kwargs):
    if created:
        Notification.objects.create(receiver=instance.author,text="Your article has been successfully published.")
        all_followers_notification_task.delay(instance.author.id)

@receiver(m2m_changed,sender=Article.likes.through)
def notify_on_article_like(sender,instance,action,pk_set,**kwargs):
    if action == 'post_add':
        notifications = []
        for pk in pk_set:
            user = User.objects.get(id=pk)
            notifications.append(Notification(receiver=instance.author,text=f"User {user.username} liked your article."))
        Notification.objects.bulk_create(notifications,batch_size=1000)

@receiver(post_save,sender=Comment)
def notify_on_comment_create(sender,instance,created,**kwargs):
    if created:
        Notification.objects.create(receiver=instance.article.author,text=f"User {instance.author} commented on your article.")
        if instance.is_child_node():
            Notification.objects.create(receiver=instance.parent.author,text=f"User {instance.author} replied to your comment.")

@receiver(m2m_changed,sender=Comment.likes.through)
def notify_on_comment_like(sender,instance,action,pk_set,**kwargs):
    if action == 'post_add':
        notifications = []
        for pk in pk_set:
            user = User.objects.get(id=pk)
            notifications.append(Notification(receiver=instance.author,text=f"User {user.username} liked your comment."))
        Notification.objects.bulk_create(notifications,batch_size=1000)

@receiver(m2m_changed,sender=Profile.followers.through)
def notify_on_profile_follow(sender,instance,action,pk_set,**kwargs):
    if action == 'post_add':
        notifications = []
        for pk in pk_set:
            follower = User.objects.get(id=pk)
            notifications.append(Notification(receiver=instance.user,text=f"User {follower.username} has followed you"))
        Notification.objects.bulk_create(notifications,batch_size=1000)