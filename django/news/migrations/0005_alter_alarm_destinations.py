# Generated by Django 3.2.9 on 2021-11-14 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_alarm_destinations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='destinations',
            field=models.ManyToManyField(blank=True, related_name='alarms', to='news.FollowCompany'),
        ),
    ]
