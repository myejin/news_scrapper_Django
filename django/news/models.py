from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=45)
    follow_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="follow_companies", through='FollowCompany')

    def __str__(self):
        return f'{self.pk}, {self.name}'


class Article(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    original_link = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    pubDate = models.DateTimeField(auto_now_add=True)
    cleaned_data = models.CharField(max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return f'{self.pk}, {self.title}'


class FollowCompany(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    receive_email = models.BooleanField(default=False)
    receive_sms = models.BooleanField(default=False)


class Keyword(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='keywords')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pk}, ({self.company.name}, {self.name})'
        