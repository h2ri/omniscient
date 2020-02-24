from django.urls import path
from .views import HomePageView, ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView

urlpatterns = [
    #path('', HomePageView.as_view(), name='home'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('', ArticleListView.as_view(), name='article'),
    path('article/new/', ArticleCreateView.as_view(), name='article-new'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article-update'),
]