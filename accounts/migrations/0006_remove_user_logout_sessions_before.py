# Generated by Django 2.0.9 on 2018-11-14 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20181114_0951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='logout_sessions_before',
        ),
    ]
