from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginPage, name='login'),
    path('unlog/', views.unlogUser, name='deconnect'),
    path('<int:year>/<int:month>/', views.show_month, name='showMonth'),
    path('import/', views.importBankData, name='importTransactions'),
    path('edit/<int:entry_id>/', views.editEntry, name='editEntry'),
    path('invoices/<int:year>/<int:month>/', views.invoices, name='invoices'),
    path('pdfinvoice/<int:year>/<int:month>/<int:accountid>/', views.pdf_invoice, name='invoicePDF'),
    path('sendinvoice/<int:year>/<int:month>/<int:accountid>/', views.send_invoice, name='sendInvoice')
]