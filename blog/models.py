from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
