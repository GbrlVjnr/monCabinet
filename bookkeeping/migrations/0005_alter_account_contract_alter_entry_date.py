# Generated by Django 4.0 on 2021-12-19 19:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping', '0004_alter_account_contract_alter_entry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='contract',
            field=models.CharField(choices=[('tenant', 'Tenant'), ('sublet', 'Sublet'), ('unspecified', 'Unspecified')], default='unspecified', max_length=12),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 12, 19, 20, 28, 54, 909654)),
        ),
    ]
