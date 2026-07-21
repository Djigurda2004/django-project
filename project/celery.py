import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_finalize.connect
def setup_periodic_task(sender,**kwargs):
    sender.add_periodic_task(crontab(minute='*/10'),sender.signature('articles.tasks.sync_article_stats_with_db'))
    sender.add_periodic_task(crontab(minute='*/30'),sender.signature('articles.tasks.get_most_popular_articles'))