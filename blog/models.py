from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from lib.casbin.client import Client

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Company)
def auth_handler(sender, **kwargs):
    domain = kwargs['instance'].name
    obj = 'articles'
    Client.AddPolicy('admin', domain, obj, 'GET')
    Client.AddPolicy('admin', domain, obj, 'POST')
    Client.AddPolicy('member', domain, obj, 'GET')
    admin = User.objects.filter(is_staff=True)
    Client.AddGroupingPolicy(admin[0].first_name, 'admin', domain)

class Article(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='blog_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()

    def get_absolute_url(self):
        return reverse('article')

    def __str__(self):
        return self.title
