# Generated by Django 2.2.3 on 2019-07-08 19:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fadderanmalan', '0022_auto_20190705_2208'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='enterqueue',
            unique_together={('job', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='leavequeue',
            unique_together={('job', 'user')},
        ),
    ]