# Generated by Django 4.0 on 2022-01-09 19:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping', '0012_alter_account_start_date_alter_distribution_entry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 9, 20, 33, 14, 276888)),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 1, 9, 20, 33, 14, 308799)),
        ),
    ]