from django.urls import path
from .           import views

urlpatterns = [
    path('/listview', views.InvestmentListView.as_view()), 
    ]
