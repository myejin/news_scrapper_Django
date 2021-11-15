from datetime import datetime

from rest_framework import serializers

from .models import Article, Company

class ArticleListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        articles = [Article(**item) for item in validated_data]
        return Article.objects.bulk_create(articles)

    def update(self, instance, validated_data):
        print(instance)
        article_mapping = {article.cleaned_data: article for article in instance}
        
        data_mapping = dict()
        for data in validated_data:
            cleaned_data = data['cleaned_data']
            if cleaned_data in data_mapping:
                data['count'] = data_mapping[cleaned_data]['count'] + 1
                data_mapping[cleaned_data] = data
            else:
                if cleaned_data in article_mapping:
                    data['count'] = article_mapping[cleaned_data].count + 1
                    data_mapping[cleaned_data] = data
                else:
                    data['count'] = 1
                    data_mapping[cleaned_data] = data
        
        ret = []
        for cleaned_data, data in data_mapping.items():
            article = article_mapping.get(cleaned_data, None)
            if article is None:
                ret.append(self.child.create(data))
            else:
                data['id'] = article.id
                ret.append(self.child.update(article, data))

        return ret


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    original_link = serializers.CharField(max_length=255)
    link = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    pubDate = serializers.DateTimeField()
    cleaned_data = serializers.CharField(max_length=100)
    count = serializers.IntegerField()
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        list_serializer_class = ArticleListSerializer

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.original_link = validated_data.get('original_link', instance.original_link)
        instance.link = validated_data.get('link', instance.link)
        instance.description = validated_data.get('description', instance.description)
        instance.pubDate = validated_data.get('pubDate', instance.pubDate)
        instance.cleaned_data = validated_data.get('cleaned_data', instance.cleaned_data)
        instance.count = validated_data.get('count', instance.count)
        instance.company = validated_data.get('company', instance.company)
        instance.save()
        return instance
        
    @classmethod
    def many_init(cls, *args, **kwargs):
        # Instantiate the child serializer.
        kwargs['child'] = cls()
        # Instantiate the parent list serializer.
        return ArticleListSerializer(*args, **kwargs)