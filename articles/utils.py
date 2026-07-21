from django.core.paginator import Paginator
from django.db.models import Q
from common.redis_client import redis_client
from .redis_keys import get_article_views_key

def pagination(request,query_set,obj_per_page):
    query = request.GET.get("q", "")
    articles = query_set
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(author__username__icontains=query))
    paginator = Paginator(articles, obj_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    articles_redis_views = get_articles_views(page_obj.object_list)
    for i,article in enumerate(page_obj):
            article.redis_views = int(articles_redis_views[i])
    return {"query":query,"page_obj":page_obj}

def get_articles_views(query_set):
    article_ids = [article.id for article in query_set]
    if article_ids:
        redis_views_keys = [get_article_views_key(id) for id in article_ids]
        redis_views = redis_client.mget(redis_views_keys)
        return redis_views
