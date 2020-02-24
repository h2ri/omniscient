from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from lib.casbin.client import Client

class PermissionsMixin(PermissionRequiredMixin):
    def has_permission(self, **kwargs):
        subject = self.request.user.first_name
        domain = self.get_object().company.name
        action = self.request.method
        if action == 'GET':
            obj = 'articles'
        else:
            obj = 'article_' + str(self.get_object().id)
        return Client.CheckPermissions(subject, domain, obj, action)

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


class ArticleDetailView(PermissionsMixin, LoginRequiredMixin, DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.request.user.first_name
        domain = self.get_object().company.name
        obj = 'article_' + str(self.get_object().id)
        action = 'POST'
        context['can_edit'] = Client.CheckPermissions(subject, domain, obj, action)
        return context


class ArticleUpdateView(PermissionsMixin, LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'content']


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content']
    template_name_suffix = '_update_form'