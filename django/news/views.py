from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.timezone import get_current_timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article, Company, Keyword, Alarm as Al
from .serializers import ArticleSerializer, CompanySerializer, KeywordSerializer
from .alarm import *


## Article views
@api_view(['GET', 'POST'])
def list_create_articles(request):
    def list_articles():
        company_name = request.GET.get('company_name')
        if company_name is None:
            articles = Article.objects.all()
            serializer = ArticleSerializer(instance=articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            company = get_object_or_404(Company, name=company_name)
            articles = Article.objects.filter(company=company).all()
            serializer = ArticleSerializer(instance=articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create_articles():
        company_name = request.data.get('company_name', None)
        if company_name is None:
            return Response({'error': 'company_name이 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        company = get_object_or_404(Company, name=company_name)
        company_id = company.id

        datas = request.data.get('articles', None)
        if datas is None:
            return Response({'error': 'datas가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        for data in datas:
            data['company'] = company_id
            data['count'] = 0
        
        now_date = datetime.now(tz=get_current_timezone())
        seven_days_ago_date = now_date + timedelta(days=-7)

        articles = Article.objects.filter(pubDate__range=(seven_days_ago_date, now_date), company=company).all()
        serializer = ArticleSerializer(instance=articles, data=datas, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        return list_articles()
    elif request.method == 'POST':
        return create_articles()
    

@api_view(['GET'])
def list_articles_by_company_id(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk)
    articles = Article.objects.filter(company=company).all()
    serializer = ArticleSerializer(instance=articles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view(['DELETE'])
def delete_article(request, article_pk):
    try:
        article = Article.objects.get(pk=article_pk)
    except Company.DoesNotExist:
        return Response({'error': '해당 article_pk 기사가 존재하지 않습니다'}, status=status.HTTP_404_NOT_FOUND)
    
    article.delete()
    return Response({ 'id': article_pk }, status=status.HTTP_204_NO_CONTENT)


## Company views
@api_view(['GET', 'POST'])
def list_create_companies(request):
    def list_companies():
        companies = Company.objects.all()
        serializer = CompanySerializer(instance=companies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create_company():
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        return list_companies()
    elif request.method == 'POST':
        return create_company()


@api_view(['GET'])
def get_company_by_id(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk)
    serializer = CompanySerializer(instance=company)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])
def get_update_delete_company(request, company_pk):
    try:
        company = Company.objects.get(pk=company_pk)
    except Company.DoesNotExist:
        return Response({'error': '해당 company_pk 기업이 존재하지 않습니다'}, status=status.HTTP_404_NOT_FOUND)
    
    def get_company():
        serializer = CompanySerializer(instance=company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_company():
        serializer = CompanySerializer(instance=company, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_company():
        company.delete()
        return Response({ 'id': company_pk }, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return get_company()
    elif request.method == 'PUT':
        return update_company()
    elif request.method == 'DELETE':
        return delete_company()


## Keyword views
@api_view(['GET'])
def list_keywords(request):
    company_name = request.GET.get('company_name')
    if company_name is None:
        keywords = Keyword.objects.all()
        serializer = KeywordSerializer(instance=keywords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        company = get_object_or_404(Company, name=company_name)
        keywords = Keyword.objects.filter(company=company).all()
        serializer = KeywordSerializer(instance=keywords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def get_update_delete_keyword_by_id(request, keyword_pk):
    keyword = get_object_or_404(Keyword, pk=keyword_pk)

    def get_keyword_by_id():
        serializer = KeywordSerializer(instance=keyword)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_keyword():
        serializer = KeywordSerializer(instance=keyword, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_keyword():
        keyword.delete()
        return Response({ 'id': keyword_pk }, status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'GET':
        return get_keyword_by_id()
    elif request.method == 'PUT':
        return update_keyword()
    elif request.method == 'DELETE':
        return delete_keyword()


@api_view(['GET', 'POST'])
def list_create_keywords(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk)

    def list_keywords_by_company_id():
        keywords = Keyword.objects.filter(company=company).all()
        serializer = KeywordSerializer(instance=keywords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_keyword():
        serializer = KeywordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        return list_keywords_by_company_id()
    elif request.method == 'POST':
        return create_keyword()
