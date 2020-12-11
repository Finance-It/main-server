from rest_framework import serializers

from campaign.serializers import CampaignListSerializer, \
    CampaignDetailsSerializer
from investor.models import Investment


class InvestmentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['campaign', 'amount']


class InvestmentListSerializers(serializers.ModelSerializer):
    campaign = CampaignListSerializer()

    class Meta:
        model = Investment
        fields = ['campaign', 'amount', 'status']
        depth = 2


class InvestmentDetailSerializers(serializers.ModelSerializer):
    campaign = CampaignDetailsSerializer()

    class Meta:
        model = Investment
        fields = ['campaign', 'amount', 'status']
        depth = 2
