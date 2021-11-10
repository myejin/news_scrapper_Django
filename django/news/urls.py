from django.urls import path

from . import views

app_name = 'news'

# BASE_URL = 'api/v1/news/'

urlpatterns = [
    # articles
    path('articles', views.list_or_create_articles),

    # company
    path('companies/articles', views.list_articles_by_company_name),
    path('companies/<int:company_pk>/articles', views.list_articles_by_company_id),
]
