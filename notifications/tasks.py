from celery import shared_task
from users.models import User
from .models import Notification
from articles.models import Article
from django.contrib.contenttypes.models import ContentType
from .utils import increment_unread_notifications

@shared_task
def send_notification_to_followers(user_id,article_id):
    user = User.objects.get(id=user_id)
    followers = user.followers.all()
    notifications = []
    for follower in followers:
        notifications.append(Notification(receiver=follower,type="ARTICLE_PUBLISHED_FOR_FOLLOWERS",content_type=ContentType.objects.get_for_model(Article),object_id=article_id))
        increment_unread_notifications(follower.id)
    Notification.objects.bulk_create(notifications,batch_size=1000)