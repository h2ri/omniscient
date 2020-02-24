from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin, ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context


class ArticleListView(LoginRequiredMixin, ListView):

    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title']


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title']
    template_name_suffix = '_update_form'


# def article_detail_view(request, primary_key):
#     book = get_object_or_404(Book, pk=primary_key)
#     return render(request, 'catalog/book_detail.html', context={'book': book})