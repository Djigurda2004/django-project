from rest_framework.routers import DefaultRouter
from articles.api.endpoints import router as articles_router
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView
from rest_framework.routers import BaseRouter

router = DefaultRouter()
router.registry.extend(articles_router.registry)
urlpatterns = router.urls

#jwt auth endpoints
urlpatterns+=[path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
             path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
             path('token/verify/',TokenVerifyView.as_view(),name='token_verify'),
             ]