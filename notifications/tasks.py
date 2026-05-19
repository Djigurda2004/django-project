from dj.celery import app
from celery import shared_task
from django.contrib.auth.models import User
from .models import Notification

@shared_task
def all_followers_notification_task(user_id):
    user = User.objects.get(id=user_id)
    followers = user.profile.followers.all()
    notifications = []
    for follower in followers:
        notifications.append(Notification(receiver=follower,text=f"User {user.username} published a new article."))
    Notification.objects.bulk_create(notifications,batch_size=1000)