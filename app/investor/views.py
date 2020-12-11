from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView

from investor.models import Investment
from investor.permissions import IsCampaignActive
from investor.serializers import InvestmentListSerializers, \
    InvestmentCreateSerializers, InvestmentDetailSerializers


class InvestmentCreate(CreateAPIView):
    serializer_class = InvestmentCreateSerializers
    permission_classes = [permissions.IsAuthenticated, IsCampaignActive]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(investor=user)


class InvestmentList(ListAPIView):
    serializer_class = InvestmentListSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Investment.objects.filter(investor=self.request.user.id)


class InvestmentDetail(RetrieveAPIView):
    lookup_url_kwarg = 'id'
    serializer_class = InvestmentDetailSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Investment.objects.filter(investor=self.request.user.id)
