from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum

from .models import Distribution, Entry

from datetime import datetime, date

def index(request):

    last_entry = Entry.objects.latest('date')

    return show_month(request, last_entry.date.year, last_entry.date.month)

# Return a view that displays the specified month (/YYYY/m/)
def show_month(request, year, month):

    # All Entries for the month
    entry_list = Entry.objects.filter(
        date__year=year,
        date__month=month
    ).order_by('date')

    # List of registered Accounts for the month sorted by their id. Uses the first recorded expense's distribution to collect all the accounts 
    accounts_list = []
    first_expense = Entry.objects.filter(
        date__year=year,
        date__month=month,
        type="EXP"
    ).first()
    for distribution in Distribution.objects.filter(entry=first_expense):
        accounts_list.append(distribution.account)

    # Necessary function to sort data by accounts' ids.
    def account_id(account):
        return account.id

    accounts_list.sort(key=account_id)

    def monthly_total(type, year, month):
        return Entry.objects.filter(
        date__year=year,
        date__month=month,
        type=type
    ).aggregate(Sum('amount'))

    # Total amounts for each account
    monthly_accounts_totals = {}
    expenses = Entry.objects.filter(
        date__year=year,
        date__month=month,
        type="EXP"
    )
    for expense in expenses:
        distributions = expense.distribution_set.all()
        for distribution in distributions:
            if distribution.account not in monthly_accounts_totals.keys():
                monthly_accounts_totals.update(
                    {distribution.account: distribution.amount})
            else:
                monthly_accounts_totals[distribution.account] += distribution.amount

    context = {'showed_month': date(year, month, 1),
               'current_date': datetime.now().date,
               'entries': entry_list,
               'accounts_list': accounts_list,
               'monthly_income': monthly_total("INC", year, month),
               'monthly_expense': monthly_total("EXP", year, month),
            #    The dictionary needs to be sorted by the account's id in order to match the accounts_list in the view
               'monthly_accounts_totals': {key: monthly_accounts_totals[key] for key in sorted(monthly_accounts_totals, key=account_id)}}
               
    return render(request, 'bookkeeping/index.html', context)


def entryDetail(request, entry_id):
    try:
        entry = Entry.objects.get(pk=entry_id)
    except Entry.DoesNotExist:
        raise Http404("L'entrée demandée n'existe pas.")
    return HttpResponse("Détail de l'entrée %s." % entry_id)


def accountsList(request, accounts):
    return HttpResponse("Liste actuelle des comptes: %s" % accounts)
