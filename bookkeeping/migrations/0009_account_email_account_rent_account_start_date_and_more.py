# Generated by Django 4.0 on 2021-12-27 12:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping', '0008_alter_distribution_entry_alter_entry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='rent',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='account',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 27, 13, 13, 2, 414966)),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 12, 27, 13, 13, 2, 449204)),
        ),
    ]