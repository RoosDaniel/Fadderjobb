# Generated by Django 2.0.9 on 2019-02-06 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fadderanmalan', '0006_auto_20190205_1228'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('size', models.CharField(blank=True, help_text='Frivillig storlek på utrustningen. Användbart för t.ex. t-shirts.', max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentOwnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispensed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships', to='fadderanmalan.Equipment')),
                ('for_job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipments', to='fadderanmalan.Job')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
