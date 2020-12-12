# Create your views here.
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, \
    RetrieveAPIView

from campaign.models import Campaign
from campaign.permissions import IsCampaignAdmin, IsUpdateAllowedOrReadOnly
from campaign.serializers import CampaignAdminSerializer, \
    CampaignListSerializer, CampaignDetailsSerializer, CampaignCreateSerializer


class CampaignLC(ListCreateAPIView):
    queryset = Campaign.objects.filter(status='ACTIVE')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CampaignCreateSerializer
        else:
            return CampaignListSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)


class CampaignDetails(RetrieveAPIView):
    lookup_url_kwarg = 'id'
    queryset = Campaign.objects.all()
    serializer_class = CampaignDetailsSerializer


class CampaignRU(RetrieveUpdateAPIView):
    lookup_url_kwarg = 'id'
    queryset = Campaign.objects.all()
    serializer_class = CampaignAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsCampaignAdmin,
                          IsUpdateAllowedOrReadOnly]


class MyCampaign(ListCreateAPIView):
    serializer_class = CampaignDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Campaign.objects.filter(created_by=self.request.user)
