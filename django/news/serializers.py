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
    class Meta:
        model = Article
        fields = '__all__'


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
        