# Generated by Django 2.1.7 on 2019-02-25 10:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fadderanmalan', '0012_auto_20190225_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobuser',
            name='requested_give',
            field=models.ManyToManyField(blank=True, related_name='give_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobuser',
            name='requested_take',
            field=models.ManyToManyField(blank=True, related_name='take_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
