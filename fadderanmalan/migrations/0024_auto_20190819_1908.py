# Generated by Django 2.2.4 on 2019-08-19 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fadderanmalan', '0023_auto_20190708_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentownership',
            name='job',
            field=models.ForeignKey(blank=True, help_text='Vilket jobb gäller utdelningen? Kan vara tom.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipments', to='fadderanmalan.Job'),
        ),
    ]
