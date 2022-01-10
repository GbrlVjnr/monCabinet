from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/', views.show_month, name='showMonth'),
    path('<int:entry_id>/', views.entryDetail, name='entryDetail'),
    path('accounts/', views.accountsList, name='accounts')
]