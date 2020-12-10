from django.urls import path

from campaign.views import CampaignLC

urlpatterns = [
    path('', CampaignLC.as_view()),
]
