from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Article, Company
from .serializers import ArticleListSerializer, ArticleSerializer, ArticleCreateListRequestSerializer, CompanyListSerializer, CompanySerializer, CompanyCreateSerializer


list_articles_param = openapi.Parameter('company_name', openapi.IN_QUERY, description="삼성", type=openapi.TYPE_STRING)
list_articles_response = openapi.Response('목록 불러오기 완료', ArticleListSerializer(many=True))
create_articles_response = openapi.Response('기사 등록 완료', ArticleCreateListRequestSerializer)
@swagger_auto_schema(method='get', manual_parameters=[list_articles_param], responses={200: list_articles_response})
@swagger_auto_schema(method='post', request_body=ArticleCreateListRequestSerializer, responses={201: create_articles_response})
@api_view(['GET', 'POST'])
def list_or_create_articles(request):
    '''
    기사 목록 불러오기 & 기사 저장하기
    ---
    ### 내용
        * title : 기사 제목
        * original_link : 원본 뉴스 link
        * link : 네이버 뉴스 link
        * description : 기사 요약
        * pubDate : 기사 등록 날짜
        * cleand_data : 기사 주제 키워드
        * count : 관련 기사 갯수
    '''
    def list_articles():
        company_name = request.data.get('company_name')
        if company_name is None:
            articles = Article.objects.all()
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data)
        else:
            articles = get_object_or_404(Company, name=company_name).articles
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data)
    
    def create_articles():
        company_name = request.data.get('company_name', None)
        articles = request.data.get('articles', None)
        if company_name is None or articles is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        company = get_object_or_404(Company, name=company_name)

        for article in articles:
            cleaned_data = article.get('cleaned_data', '')
            if not cleaned_data:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            cleaned_data_article_set = Article.objects.filter(company_id=company.pk, cleaned_data=cleaned_data)
            
            if cleaned_data_article_set.count():
                saved_article = cleaned_data_article_set.get()
                article['id'] = saved_article.id
                article['count'] = saved_article.count + 1
                serializer = ArticleSerializer(instance=saved_article, data=article)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(company=company)
            else:
                article['id'] = saved_article.id
                article['count'] = 1
                serializer = ArticleSerializer(data=article)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(company=company)

        data = {
            'company_name': company_name,
            'articles': articles,
        }
        return Response(data=data ,status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        return list_articles()
    elif request.method == 'POST':
        return create_articles()
    

get_company_by_id_params = openapi.Parameter('company_pk', openapi.IN_PATH, description="0", type=openapi.TYPE_INTEGER)
get_company_response = openapi.Response('기업 불러오기 완료', CompanySerializer)
@swagger_auto_schema(method='get', manual_parameters=[get_company_by_id_params], responses={200: get_company_response})
@api_view(['GET'])
def get_company_by_id(request, company_pk):
    '''
    기업 id로 기업 정보 가져오기
    ---
    ### 내용
        * company_pk : 기업 id
        * keywords : 기업 검색 키워드 array
        * name : 기업 이름
        * follow_users : 해당 기업을 팔로우하고 있는 user들의 id
    '''
    company = get_object_or_404(Company, pk=company_pk)
    serializer = CompanySerializer(company)
    return Response(serializer.data)


list_articles_by_company_id_param = openapi.Parameter('company_pk', openapi.IN_PATH, description="0", type=openapi.TYPE_INTEGER)
list_articles_by_company_id_response = openapi.Response('목록 불러오기 완료', ArticleListSerializer(many=True))
@swagger_auto_schema(method='get', manual_parameters=[list_articles_by_company_id_param], responses={200: list_articles_by_company_id_response})
@api_view(['GET'])
def list_articles_by_company_id(request, company_pk):
    '''
    기업 id로 해당 기업의 기사 목록 가져오기
    ---
    ### 내용
        * title : 기사 제목
        * original_link : 원본 뉴스 link
        * link : 네이버 뉴스 link
        * description : 기사 요약
        * pubDate : 기사 등록 날짜
        * cleand_data : 기사 주제 키워드
        * count : 관련 기사 갯수
    '''
    articles = Article.objects.filter(company_id=company_pk)
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)
    

list_companies_response = openapi.Response('목록 불러오기 완료', CompanyListSerializer(many=True))
create_company_response = openapi.Response('기업 등록 완료', CompanyCreateSerializer)
@swagger_auto_schema(method='get', responses={200: list_companies_response})
@swagger_auto_schema(method='post', responses={201: create_company_response})
@api_view(['GET', 'POST'])
def list_or_create_companies(request):
    '''
    기업 목록 불러오기 & 기업 등록하기
    ---
    ### 내용
        * id : 기업 id
        * name : 기업 이름
        * follow_users : 해당 기업을 팔로우하고 있는 user들의 id
    '''
    def list_companies():
        companies = Company.objects.all()
        serializer = CompanyListSerializer(companies, many=True)
        return Response(serializer.data)

    def create_company():
        serializer = CompanyCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    if request.method == 'GET':
        return list_companies()
    elif request.method == 'POST':
        return create_company()
