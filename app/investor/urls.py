from django.urls import path

from investor.views import InvestmentList, InvestmentDetail, InvestmentCreate

urlpatterns = [
    path('', InvestmentList.as_view()),
    path('invest', InvestmentCreate.as_view()),
    path('<int:id>', InvestmentDetail.as_view()),
]
