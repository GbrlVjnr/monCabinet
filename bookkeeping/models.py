from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.deletion import CASCADE

import datetime

from django.db.models.fields import EmailField

class Account(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, null=True)
    contractType = models.TextChoices(
        'contractType', 'tenant sublet legal unspecified')
    contract = models.CharField(
        max_length=12, choices=contractType.choices, default='unspecified')
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return self.full_name

class Entry(models.Model):
    ENTRY_TYPES = [
        ('INC', 'income'),
        ('EXP', 'expense'),
    ]
    label = models.CharField(max_length=300)
    amount = models.FloatField(default=0.00)
    type = models.CharField(max_length=3, choices=ENTRY_TYPES)
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
