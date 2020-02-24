from django.contrib import admin
from .models import Company, Article
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from casbin.client import Client



class UserForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label="")

    class Meta:
        model = User
        fields = "__all__"


class ArticleForm(forms.ModelForm):
    user = forms.ModelChoiceField(required=False,queryset=User.objects.all(), empty_label="")

    class Meta:
        model = Article
        fields = "__all__"

class UserAdmin(UserAdmin):
    form = UserForm

    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'company',),
        }),
    )

    def save_model(self, request, obj, form, change):
        super(UserAdmin, self).save_model(request, obj, form, change)
        if form.fields.get('company'):
            subject = obj.first_name
            domain = dict(form.fields['company'].choices)[int(form.data['company'])]
            Client.AddGroupingPolicy(subject, 'member', domain)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    fieldsets = (
        (None, {
            'fields': ('company', 'author', 'title', 'slug', 'content')
        }),
        ('User Access', {
            'fields': ('user',),
        }),
    )

    def save_model(self, request, obj, form, change):
        super(ArticleAdmin, self).save_model(request, obj, form, change)
        subject = form.cleaned_data['author'].first_name
        domain = form.cleaned_data['company'].name
        action = 'POST'
        o = f'article_{obj.id}'
        Client.AddPolicy(subject, domain, o, action)
        extra_field = form.data['user']
        if extra_field:
            user = User.objects.filter(id=extra_field)
            if user:
                subject = user[0].first_name
                Client.AddPolicy(subject, domain, o, action)
                Client.AddPolicy(subject, domain, o, 'GET')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Company)