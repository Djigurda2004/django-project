from django.shortcuts import render
from common.redis_client import redis_client
from articles.redis_keys import get_most_popular_articles_key
from articles.models import Article
from articles.utils import get_articles_views
from .data import BRIEF_INFO,STACK_ICONS,FEATURES_LIST

def index(request):
    articles_ids = [int(article_id) for article_id in redis_client.lrange(get_most_popular_articles_key(),0,-1)]
    articles = Article.objects.filter(id__in=articles_ids)
    articles_redis_views = get_articles_views(articles)
    for i,article in enumerate(articles):
        article.redis_views = int(articles_redis_views[i])
    return render(request, "base/index.html",{"articles":articles})

def about(request):
    context = {'brief_info':BRIEF_INFO,
               'stack_icons':STACK_ICONS,
               'features_list':FEATURES_LIST,
               }
    return render(request, "base/about.html",context)