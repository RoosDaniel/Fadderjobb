# Generated by Django 2.0.9 on 2019-02-06 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fadderanmalan', '0009_auto_20190206_0920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmentownership',
            name='for_job',
        ),
        migrations.AddField(
            model_name='equipmentownership',
            name='job',
            field=models.ForeignKey(blank=True, help_text='Vilket jobb gäller utdelningen? Kan vara tom.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipments', to='fadderanmalan.Job'),
        ),
    ]
