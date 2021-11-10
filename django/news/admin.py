from django.contrib import admin

from .models import Article, Company, FollowCompany

admin.site.register(Article)
admin.site.register(Company)
admin.site.register(FollowCompany)