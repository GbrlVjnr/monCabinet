# Generated by Django 4.0 on 2021-12-19 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='contract',
            field=models.CharField(default='unspecified', max_length=15),
        ),
    ]
