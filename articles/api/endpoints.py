from rest_framework.routers import DefaultRouter
from . import viewsets
from django.urls import path

router = DefaultRouter()
router.register(r'articles',viewsets.ArticleViewSet)