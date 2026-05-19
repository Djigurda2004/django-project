from django.urls.conf import path
from . import views

app_name = 'notifications'
urlpatterns = [
    path('',views.notifications_list,name='list'),
    path('delete/<int:notification_id>',views.delete_notification,name='delete'),
]