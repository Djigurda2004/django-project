from celery import shared_task
from .models import Article
from .utils import get_articles_views
from common.redis_client import redis_client
from .redis_keys import get_most_popular_articles_key

@shared_task
def sync_article_stats_with_db():
    articles = Article.objects.all()
    articles_redis_views = get_articles_views(articles)
    updated_articles = []
    for i,article in enumerate(articles):
        curr_article_redis_views = int(articles_redis_views[i])
        if article.views!=curr_article_redis_views:
            article.views=curr_article_redis_views
            updated_articles.append(article)
    Article.objects.bulk_update(updated_articles,['views'])

@shared_task
def get_most_popular_articles():
    articles_ids = list(Article.objects.order_by("-views").values_list("id",flat=True)[:5])
    if articles_ids:
        pipe = redis_client.pipeline()
        pipe.delete(get_most_popular_articles_key())
        pipe.rpush(get_most_popular_articles_key(),*articles_ids)
        pipe.execute()


    