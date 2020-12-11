from django.urls import path

from payments.views import InvestmentPayment, RazorpayWebhook, \
    CallBackInvestmentPayment, CreateVirtualAccForDebtRepay

urlpatterns = [
    path('investments/<int:id>', InvestmentPayment.as_view()),
    path('callbacks/investments', CallBackInvestmentPayment.as_view()),
    path('campaign/<int:id>/repay', CreateVirtualAccForDebtRepay.as_view()),

    # Webhooks
    path('webhooks', RazorpayWebhook.as_view()),
]
