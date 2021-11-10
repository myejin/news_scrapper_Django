from rest_framework import serializers

from .models import Article, Company


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
        