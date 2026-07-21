import redis
from django.conf import settings

_redis_client_instance = None

def get_redis_client():
    global _redis_client_instance
    if _redis_client_instance is None:
        _redis_client_instance = redis.StrictRedis.from_url(settings.REDIS_URL,decode_responses=True)
    return _redis_client_instance

redis_client = get_redis_client()