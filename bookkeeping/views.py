# Imports from Django's librairies
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Sum
from django.template.loader import get_template

# Woob imports (module used to collect bank data)
from woob.capabilities.bank.base import AccountNotFound

# Models imports
from .models import Account, Distribution, Entry

# Python's modules imports
from datetime import datetime, date
from io import BytesIO

from xhtml2pdf import pisa

# Collects data from a specific month
def month_data(year, month):

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

    return {
        'entries': entry_list, 
        'distributions': distributions,
        'accounts': accounts_list, 
        'total_income': monthly_total("INC", year, month),
        'total_expenses': monthly_total("EXP", year, month),
        #    The dictionary needs to be sorted by the account's id in order to match the accounts_list in the view
        'accounts_totals': {key: monthly_accounts_totals[key] for key in sorted(monthly_accounts_totals, key=account_id)}
        }

def index(request):

    last_entry = Entry.objects.latest('date')

    return show_month(request, last_entry.date.year, last_entry.date.month)

# Return a view that displays the specified month (/YYYY/m/)
def show_month(request, year, month):

    context = {'showed_month': date(year, month, 1), 'title': "Livre-journal",
               'current_date': datetime.now().date,
               'entries': month_data(year, month)['entries'],
               'accounts_list': month_data(year, month)['accounts'],
               'monthly_income': month_data(year, month)['total_income'],
               'monthly_expense': month_data(year, month)['total_expenses'],
               'monthly_accounts_totals': month_data(year,month)['accounts_totals']}

    return render(request, 'bookkeeping/index.html', context)

# Returns new data from the bank account
def importBankData(request):
    from woob.core import Woob
    from woob.capabilities.bank import CapBank

    try:

        w = Woob()
        w.load_backends(CapBank)

        bank_accounts = list(w.iter_accounts())
        all_transactions = w.iter_history(bank_accounts[0])

        def isNew(transaction):

            last_entry = Entry.objects.latest('date')

            if transaction.date >= last_entry.date and abs(transaction.amount) != last_entry.amount:
                return True
            else:
                return False

        transactions_to_import = filter(isNew, all_transactions)

        transactions_counter = 0
        for transaction in transactions_to_import:
            if transaction.amount < 0:
                new_transaction = Entry(type='EXP', date=transaction.date,
                                        label=transaction.label, amount=abs(transaction.amount))
            else:
                new_transaction = Entry(type='INC', date=transaction.date,
                                        label=transaction.label, amount=abs(transaction.amount))
            new_transaction.save()
            transactions_counter += 1

        context = {
            'title': "Importation des données bancaires",
            'message': f"{transactions_counter} transaction(s) importée(s).",
            'transactions': transactions_to_import}

    except AccountNotFound:

        ErrorMessage = "Les données n'ont pas pu être chargées. Veuillez réessayer."
        context = {'message': ErrorMessage}

    return render(request, 'bookkeeping/import.html', context)

# Allows editing an entry
def editEntry(request, entry_id):

    entry = Entry.objects.get(pk=entry_id)

    if request.method == "POST":

        try:

            entry.label = request.POST['label']
            entry.save()

            # Distributes the transaction equally among tenants and creates Distribution equal to 0 for the others
            if request.POST['distribution'] == "tenants":
                distributed_amount = entry.amount / 3
                tenants = Account.objects.filter(contract="tenant")
                others = Account.objects.all().exclude(
                    is_active=False).exclude(contract="tenant")
                for tenant in tenants:
                    new_distribution = Distribution(
                        entry=entry, account=tenant, amount=distributed_amount)
                    new_distribution.save()
                for other in others:
                    new_distribution = Distribution(
                        entry=entry, account=other, amount=0.00)
                    new_distribution.save()

            # Distributes the transaction among active accounts depending on their rent
            elif request.POST['distribution'] == "rent":
                accounts = Account.objects.filter(is_active=True)
                for account in accounts:
                    if account.contract == "tenant":
                        subrents_amount = accounts.aggregate(Sum('rent'))
                        new_distribution = Distribution(
                            entry=entry, account=account, amount=(entry.amount - float(subrents_amount['rent__sum']))/3)
                        new_distribution.save()
                        print("saved!")
                    else:
                        new_distribution = Distribution(
                            entry=entry, account=account, amount=account.rent)
                        new_distribution.save()

            # Distributes the transaction depending on the amounts specified in the form
            elif request.POST['distribution'] == "custom":
                active_accounts = Account.objects.filter(is_active=True)
                for account in active_accounts:
                    if request.POST[str(account.id)] == '':
                        new_distribution = Distribution(
                            entry=entry, account=account, amount=0.00)
                        new_distribution.save()
                    else:
                        new_distribution = Distribution(
                            entry=entry, account=account, amount=request.POST[str(account.id)])
                        new_distribution.save()

            return redirect('index')

        except:

            return render(request, 'bookkeeping/edit.html', {'error_message': "Problème lors de l'enregistrement des données."})

    else:

        accounts = Account.objects.filter(is_active=True)

        context = {'transaction': entry, 'accounts': accounts,
                   'title': "Éditer une transaction"}

    return render(request, 'bookkeeping/edit.html', context)

# Returns a view displaying a preview of all invoices for a specific month
def invoices(request, year, month):

    accounts = month_data(year, month)['accounts']

    data = []

    for account in accounts:
        expenses = Distribution.objects.filter(account=account, entry__date__year=year, entry__date__month=month).exclude(amount=0)
        data_set = {'account': account, 'expenses': expenses, 'total': expenses.aggregate(Sum('amount'))}
        data.append(data_set)    
    
    context = {
        'title': "Factures",
        'showed_month': date(year, month, 1),
        'current_date': datetime.now().date,
        'invoices': data
       }

    return render(request, 'bookkeeping/invoices.html', context)

# Loads a PDF file for a specific invoice
def pdf_invoice(request, year, month, accountid):

    # Collects the data for the invoice view
    account = Account.objects.get(pk=accountid)
    expenses = Distribution.objects.filter(account=account, entry__date__year=year, entry__date__month=month).exclude(amount=0)
    total = expenses.aggregate(Sum('amount'))

    data = {
        'account': account,
        'expenses': expenses,
        'total': total,
        'current_date': datetime.now().date,
    }
    
    # PDF rendering
    template = get_template('bookkeeping/pdf_template.html')
    html = template.render(data)
    result = BytesIO()
    pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    
    return HttpResponse(result.getvalue(), content_type='application/pdf')