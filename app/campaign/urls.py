from django.urls import path

from campaign.views import CampaignLC, CampaignRU, CampaignDetails, MyCampaign

urlpatterns = [
    path('', CampaignLC.as_view()),
    path('<int:id>/admin', CampaignRU.as_view()),
    path('<int:id>', CampaignDetails.as_view()),
    path('myCampaign', MyCampaign.as_view())
]
