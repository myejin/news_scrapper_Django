from django.urls import path

from . import views

# BASE_URL = 'api/v1/news/'

urlpatterns = [
    # articles
    path('articles', views.list_create_articles),        # GET POST
    path('companies/<int:company_pk>/articles', views.list_articles_by_company_id),     # GET
    path('articles/<int:article_pk>', views.delete_article),    # DELETE

    # company
    path('companies', views.list_create_companies),                  # GET POST
    path('companies/<int:company_pk>', views.get_update_delete_company),        # GET, PUT, DELETE

    # keyword
    path('keywords', views.list_keywords),      # GET
    path('keywords/<int:keyword_pk>', views.get_update_delete_keyword_by_id),       # GET, PUT, DELETE
    path('companies/<int:company_pk>/keywords', views.list_create_keywords),        # GET, POST
]
