# Generated by Django 4.0 on 2022-01-30 20:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping', '0020_alter_account_start_date_alter_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 30, 21, 59, 29, 532371)),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 1, 30, 21, 59, 29, 566343)),
        ),
    ]
