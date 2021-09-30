from django.urls import path
from .           import views

urlpatterns = [
    path("/invest/<int:investment_id>", views.InvestTransactionView.as_view()),
    path("/deposit", views.DepositTransactionView.as_view()),
    path("/portfolio", views.PortfolioView.as_view()),
    path("/transaction", views.TransactionInformationView.as_view()),
]
