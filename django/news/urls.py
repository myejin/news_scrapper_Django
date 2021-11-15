from django.urls import path

from . import views

# BASE_URL = 'api/v1/news/'

urlpatterns = [
    # articles
    path('articles', views.list_or_create_articles),        # GET POST

    # company
    # path('companies/<int:company_pk>', views.get_company_by_id),        # GET
    # path('companies/articles', views.list_articles_by_company_name),    # GET
    # path('companies/<int:company_pk>/articles', views.list_articles_by_company_id),     # GET
]