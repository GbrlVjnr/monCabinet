from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse

from .models import Distribution, Entry

def index(request):
    entry_list = Entry.objects.order_by('date')[:10]
    distributions_list = Distribution.objects.all()
    context = {'entry_list': entry_list, 'distributions': distributions_list}
    return render(request, 'bookkeeping/index.html', context)

def entryDetail(request, entry_id):
    try:
        entry = Entry.objects.get(pk=entry_id)
    except Entry.DoesNotExist:
        raise Http404("L'entrée demandée n'existe pas.")
    return HttpResponse("Détail de l'entrée %s." % entry_id)

def accountsList(request, accounts):
    return HttpResponse("Liste actuelle des comptes: %s" % accounts)