from rest_framework import serializers

from campaign.serializers import CampaignListSerializer, \
    CampaignDetailsSerializer
from investor.models import Investment


class InvestmentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'campaign', 'amount']


class InvestmentListSerializers(serializers.ModelSerializer):
    campaign = CampaignListSerializer()

    class Meta:
        model = Investment
        fields = ['id', 'campaign', 'amount', 'status', 'razorpay_payment_link']
        depth = 2


class InvestmentDetailSerializers(serializers.ModelSerializer):
    campaign = CampaignDetailsSerializer()

    class Meta:
        model = Investment
        fields = ['id', 'campaign', 'amount', 'status', 'razorpay_payment_link']
        depth = 2
