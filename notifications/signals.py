from django.db.models.signals import post_save, m2m_changed , post_delete
from django.dispatch import receiver
from .models import Notification
from articles.models import Article
from comments.models import Comment
from users.models import Profile
from django.contrib.auth.models import User
from .tasks import send_notification_to_followers
from django.contrib.contenttypes.models import ContentType
from .utils import increment_unread_notifications,decrement_unread_notifications

@receiver(post_save,sender=Article)
def handle_article_post_save(sender,instance,created,**kwargs):
    if created:
        Notification.objects.create(receiver=instance.author,type="ARTICLE_PUBLISHED_FOR_AUTHOR",content_type=ContentType.objects.get_for_model(Article),object_id=instance.id)
        send_notification_to_followers.delay(instance.author.id,instance.id)

@receiver(m2m_changed,sender=Article.likes.through)
def handle_article_like_m2m_changed(sender,instance,action,pk_set,**kwargs):
    if action == 'post_add':
        notifications = []
        for pk in pk_set:
            notifications.append(Notification(receiver=instance.author,type="ARTICLE_LIKED",content_type=ContentType.objects.get_for_model(User),object_id=pk))
        Notification.objects.bulk_create(notifications,batch_size=1000)
        increment_unread_notifications(instance.author.id)

@receiver(post_save,sender=Comment)
def handle_comment_post_save(sender,instance,created,**kwargs):
    if created:
        Notification.objects.create(receiver=instance.article.author,type="COMMENT_CREATED",content_type=ContentType.objects.get_for_model(User),object_id=instance.author.id)
        if instance.is_child_node():
            Notification.objects.create(receiver=instance.parent.author,type="COMMENT_CREATED_FOR_PARENT",content_type=ContentType.objects.get_for_model(User),object_id=instance.author.id)

@receiver(m2m_changed,sender=Comment.likes.through)
def handle_comment_like_m2m_changed(sender,instance,action,pk_set,**kwargs):
    if action == 'post_add':
        notifications = []
        for pk in pk_set:
            notifications.append(Notification(receiver=instance.author,type="COMMENT_LIKED",content_type=ContentType.objects.get_for_model(User),object_id=pk))
        Notification.objects.bulk_create(notifications,batch_size=1000)
        increment_unread_notifications(instance.author.id)

@receiver(m2m_changed,sender=Profile.followers.through)
def handle_profile_follow_m2m_changed(sender,instance,action,pk_set,**kwargs):
    if action == 'post_add':
        notifications = []
        for pk in pk_set:
            notifications.append(Notification(receiver=instance.user,type="PROFILE_FOLLOW",content_type=ContentType.objects.get_for_model(User),object_id=pk))     
        Notification.objects.bulk_create(notifications,batch_size=1000)
        increment_unread_notifications(instance.user.id)

@receiver(post_save,sender=Notification)
def handle_notification_post_save(sender,instance,created,**kwargs):
    if created and instance.is_read == False:
        increment_unread_notifications(instance.receiver.id)

@receiver(post_delete,sender=Notification)
def handle_notification_post_delete(sender,instance,**kwargs):
    if instance.is_read == False:
        decrement_unread_notifications(instance.receiver.id)