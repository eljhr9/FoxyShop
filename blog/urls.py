from django.urls import path
from . import views
from .feeds import LatestArticlesFeed

app_name = 'blog'

urlpatterns = [
    path('all/', views.blog_list, name='list'),
    path('feed/', LatestArticlesFeed(), name='article_feed'),
    path('<slug:tag_slug>/', views.blog_list, name='by_tag'),
    path('article/<slug:article_slug>/', views.blog_detail, name='detail'),
]
