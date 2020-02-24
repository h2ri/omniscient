from django.contrib.auth.mixins import PermissionRequiredMixin
from casbin.client import Client
from .models import Article

class PermissionsMixin(PermissionRequiredMixin):
    def has_permission(self, **kwargs):
        subject = self.request.user.first_name
        domain = self.get_object().company.name
        action = self.request.method
        obj = 'article_' + str(self.get_object().id)
        if action == 'GET':
            obj1 = 'articles'
            
        return Client.CheckPermissions(subject, domain, obj, action) or Client.CheckPermissions(subject, domain, obj1, action)