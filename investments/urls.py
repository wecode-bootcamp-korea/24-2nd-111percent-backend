from django.urls import path
from .           import views

urlpatterns = [
    path("", views.InvestmentListView.as_view()),
    path("/<int:investment_id>", views.InvestmentDetailView.as_view()),
]
