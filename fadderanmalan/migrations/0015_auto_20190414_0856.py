# Generated by Django 2.1.7 on 2019-04-14 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fadderanmalan', '0014_auto_20190414_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='extra_info',
            field=models.URLField(blank=True, help_text='Länk till extra information om jobbet. Visas ändast för faddrar registrerade på jobbet.', null=True),
        ),
    ]
