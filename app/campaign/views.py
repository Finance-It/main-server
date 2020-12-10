# Create your views here.
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView

from campaign.models import Campaign
from campaign.serializers import CampaignAdminSerializer, CampaignListSerializer


class CampaignLC(ListCreateAPIView):
    queryset = Campaign.objects.filter(status='ACTIVE')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CampaignAdminSerializer
        else:
            return CampaignListSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
