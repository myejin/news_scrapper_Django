from django.db.models import fields
from rest_framework import serializers

from .models import Article, Company, Keyword


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        

class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    company = CompanyListSerializer(read_only=True)
    pubDate = serializers.DateTimeField(input_formats=['%a, %d %b %Y %H:%M:%S %z', 'iso-8601'])
    class Meta:
        model = Article
        fields = '__all__'


class ArticleCreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'original_link', 'link', 'description', 'pubDate', 'cleaned_data')


class ArticleCreateListRequestSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    articles = ArticleListSerializer(many=True)


class KeywordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'name')


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    keywords = KeywordListSerializer(many=True, read_only=True)
    class Meta:
        model = Company
        fields = '__all__'
        

class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')
        