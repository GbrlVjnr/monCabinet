from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.deletion import CASCADE

import datetime

from django.db.models.fields import EmailField

class Account(models.Model):
    GENDERS = [
        ('M', 'male'),
        ('F', 'female')
    ]
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDERS, default='M')
    email = models.EmailField(max_length=254, null=True)
    contractType = models.TextChoices(
        'contractType', 'tenant sublet legal unspecified')
    contract = models.CharField(
        max_length=12, choices=contractType.choices, default='unspecified')
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

class Entry(models.Model):
    ENTRY_TYPES = [
        ('INC', 'income'),
        ('EXP', 'expense'),
    ]
    VAT_RATES = [
        ('NOR', 'normal(20%)'),
        ('MID', 'middle(10%)'),
        ('RED', 'reduced(5,5%)'),
        ('SPE', 'special(2,1%)'),
        ('ND', 'undetermined'),
    ]
    label = models.CharField(max_length=300)
    amount = models.FloatField(default=0.00)
    type = models.CharField(max_length=3, choices=ENTRY_TYPES)
    VAT_rate = models.CharField(max_length=3, choices=VAT_RATES, default='ND')
    date = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return self.label

class Distribution(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    account = models.ForeignKey(
        Account, on_delete=CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Account: {self.account.full_name} // Entry: {self.entry.label}"

# class Invoice(models.Model):
#     account = models.ForeignKey(
#         Account, on_delete=CASCADE)
#     date = models.DateField(default=datetime.datetime.now())
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
