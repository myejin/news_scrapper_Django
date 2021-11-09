from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=45)
    follow_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="follow_companies", through='FollowCompany')

    def __str__(self):
        return (self.pk, self.name)


class News(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    original_link = models.CharField(max_length=50)
    link = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    pubDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.pk, self.title)


class FollowCompany(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    receive_email = models.BooleanField()
    receive_sms = models.BooleanField()
