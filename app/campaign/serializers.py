from rest_framework import serializers

from campaign.models import Campaign


class CampaignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'business_type', 'account_no', 'ifsc_code',
                  'beneficiary_name', 'target_amount', 'pitch', 'type',
                  'reward', 'min_investment', 'end_date', 'debt_interest',
                  'debt_period']


class CampaignAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'business_type', 'account_no', 'ifsc_code',
                  'beneficiary_name', 'target_amount', 'pitch', 'type',
                  'reward', 'min_investment', 'end_date', 'debt_interest',
                  'debt_period', 'total_amount']
        extra_kwargs = {
            "name": {"read_only": True},
            "business_type": {"read_only": True},
            "type": {"read_only": True},
            "reward": {"read_only": True},
            "debt_interest": {"read_only": True},
            "debt_period": {"read_only": True},
            "total_amount": {"read_only": True},
        }


class CampaignListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'target_amount', 'type',
                  'reward', 'end_date', 'debt_interest',
                  'debt_period', 'total_amount']


class CampaignDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'business_type', 'target_amount', 'pitch', 'type',
                  'reward', 'min_investment', 'end_date', 'debt_interest',
                  'debt_period', 'total_amount']
