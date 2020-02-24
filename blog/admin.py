from django.contrib import admin
from .models import Company, Article
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
import pdb



class UserForm(forms.ModelForm):
    extra_field = forms.CharField(required=False)

    def processData(self, input):
        # example of error handling
        if False:
            raise forms.ValidationError('Processing failed!')

        return input + " has been processed"

    def save(self, commit=True):
        extra_field = self.cleaned_data.get('extra_field', None)
        print(extra_field)
        # self.description = "my result" note that this does not work

        # Get the form instance so I can write to its fields
        instance = super(User, self).save(commit=commit)

        # this writes the processed data to the description field
        #instance.description = self.processData(extra_field)

        if commit:
            instance.save()

        return instance

    class Meta:
        model = User
        fields = "__all__"


class ArticleForm(forms.ModelForm):
    extra_field = forms.CharField(required=False)

    def clean_extra_field(self):
        #TODO set permission
        print("asd")

    def processData(self, input):
        print("asd")
        # example of error handling
        if False:
            raise forms.ValidationError('Processing failed!')

        return input + " has been processed"

    # def save(self, commit=False):
    #
    #     self.save()
    # def save(self, commit=True):
    #     #extra_field = self.cleaned_data.get('extra_field', None)
    #     # self.description = "my result" note that this does not work
    #
    #     # Get the form instance so I can write to its fields
    #     instance = super(Article, self).save(commit=commit)
    #
    #     # this writes the processed data to the description field
    #     #instance.description = self.processData(extra_field)
    #
    #     if commit:
    #         instance.save()
    #
    #     return instance

    class Meta:
        model = Article
        fields = "__all__"

# class UserAdmin(UserAdmin):
#     form = UserForm
#
#     fieldsets = (
#         (None, {
#             'fields': ('extra_field',),
#         }),
#     )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    #list_display = ('company', 'author', 'title', 'slug', 'content', 'admin_list')
    fieldsets = (
        (None, {
            'fields': ('company', 'author', 'title', 'slug', 'content')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('extra_field',),
        }),
    )


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Company)
# admin.site.register(ArticleAdmin)