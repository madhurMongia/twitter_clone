app_name = 'api'
from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'tweet', views.TweetView)
urlpatterns = [
    path('feed',views.tweet_feed.as_view()),
]
urlpatterns += router.urls