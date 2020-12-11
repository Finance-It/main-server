from django.urls import path

from payments.views import InvestmentPayment, CallBackInvestmentPayment

urlpatterns = [
    path('investments/<int:id>', InvestmentPayment.as_view()),
    path('callbacks/investments', CallBackInvestmentPayment.as_view()),
]
