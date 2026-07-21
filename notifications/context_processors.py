from common.redis_client import redis_client
from .redis_keys import get_user_unread_notifications_key

def unread_notifications(request):
    user = request.user
    if user.is_authenticated:
        unread_count_cache = redis_client.get(get_user_unread_notifications_key(user.id))
        if unread_count_cache is None:
            unread_count_db = user.notifications.filter(is_read=False).count()
            redis_client.set(get_user_unread_notifications_key(request.user.id),unread_count_db)
            return {"unread_notifications":unread_count_db}
        return {"unread_notifications":unread_count_cache}
    return {}