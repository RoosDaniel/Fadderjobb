# Generated by Django 2.0.9 on 2019-02-05 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fadderanmalan', '0005_auto_20190205_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='duration',
        ),
        migrations.AlterField(
            model_name='job',
            name='date',
            field=models.DateField(help_text='Vilket datum jobbet gäller.'),
        ),
    ]
