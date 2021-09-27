from django.urls import path
from .           import views

urlpatterns = [
    path("/invest/<int:investment_id>", views.InvestTransactionView.as_view())
]
