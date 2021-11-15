from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.timezone import get_current_timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article, Company, Alarm as Al
from .serializers import ArticleSerializer
from .alarm import *


@api_view(['GET', 'POST'])
def list_or_create_articles(request):
    def list_articles():
        articles = Article.objects.all()
        serializer = ArticleSerializer(instance=articles, many=True)
        return Response(serializer.data)

    def create_articles():
        company_name = request.data['company_name']
        company_id = get_object_or_404(Company, name=company_name).id

        datas = request.data['articles']
        for data in datas:
            data['company'] = company_id
            data['count'] = 0
        
        now_date = datetime.now(tz=get_current_timezone())
        seven_days_ago_date = now_date + timedelta(days=-7)

        articles = Article.objects.filter(pubDate__range=(seven_days_ago_date, now_date)).all()
        serializer = ArticleSerializer(instance=articles, data=datas, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        return list_articles()
    elif request.method == 'POST':
        return create_articles()
        