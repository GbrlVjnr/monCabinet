# Generated by Django 4.0 on 2022-01-08 14:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping', '0011_alter_account_start_date_alter_distribution_entry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 8, 15, 26, 57, 779659)),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping.entry'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 1, 8, 15, 26, 57, 821598)),
        ),
    ]