from django.contrib.auth.mixins import PermissionRequiredMixin
from casbin.client import Client
from .models import Article

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