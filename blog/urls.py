from django.urls import path
from .views import HomePageView, ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView

urlpatterns = [
    path('articles/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('', ArticleListView.as_view(), name='article'),
    path('articles/new/', ArticleCreateView.as_view(), name='article-new'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article-update'),
]