from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article, Company
from .serializers import ArticleListSerializer, ArticleSerializer, CompanySerializer
from .alarm import news_publisher


@api_view(['GET', 'POST'])
def list_or_create_articles(request):
    def list_articles():
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    
    def create_articles():
        def notify_alarms(alerted_articles):
            news_publisher.addNews(alerted_articles)  # 기업이름도 같이 넘어가야해
            news_publisher.notifyAlarms()
            
        articles = request.data
        alerted_articles = []
        for article in articles:
            company_name = article.get('company_name', '')
            if not company_name:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            company = get_object_or_404(Company, name=company_name)
            article.pop('company_name', None)

            cleaned_data = article.get('cleaned_data', '')
            if not cleaned_data:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            cleaned_data_article_set = Article.objects.filter(company_id=company.pk, cleaned_data=cleaned_data)
            
            if cleaned_data_article_set.count():
                saved_article = cleaned_data_article_set.get()
                article['count'] = saved_article.count + 1
                serializer = ArticleSerializer(instance=saved_article, data=article)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(company=company)
                if article['count'] == 3:  # 기준점을 정하기
                    alerted_articles.append(article)                    
            else:
                article['count'] = 1
                serializer = ArticleSerializer(data=article)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(company=company)
        notify_alarms(alerted_articles)
        return Response(status=status.HTTP_201_CREATED)

    
    if request.method == 'GET':
        return list_articles()
    elif request.method == 'POST':
        return create_articles()
    

@api_view(['GET'])
def get_company_by_id(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk)
    serializer = CompanySerializer(company)
    return Response(serializer.data)


@api_view(['GET'])
def list_articles_by_company_name(request):
    company_name = request.GET.get('company_name', '')
    articles = get_object_or_404(Company, name=company_name).articles
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def list_articles_by_company_id(request, company_pk):
    articles = Article.objects.filter(company_id=company_pk)
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)
    