from django.urls import path

from . import views

app_name = 'news'

# BASE_URL = 'api/v1/news/'

urlpatterns = [
    # articles
    path('articles', views.list_or_create_articles),        # GET POST

    # company
    path('companies/<int:company_pk>', views.get_company_by_id),        # GET
    path('companies/<int:company_pk>/articles', views.list_articles_by_company_id),     # GET
    path('companies', views.list_or_create_companies),      # GET POST
]
