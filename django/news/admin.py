from django.contrib import admin

from .models import Article, Company, FollowCompany, Keyword

admin.site.register(Article)
admin.site.register(Company)
admin.site.register(FollowCompany)
admin.site.register(Keyword)