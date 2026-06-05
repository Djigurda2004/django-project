from .redis_keys import get_user_unread_notifications_key
from core.redis_client import redis_client

def increment_unread_notifications(user_id):
    key = get_user_unread_notifications_key(user_id)
    redis_client.incr(key)

def decrement_unread_notifications(user_id):
    key = get_user_unread_notifications_key(user_id)
    redis_client.decr(key)
