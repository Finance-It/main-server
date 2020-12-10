from rest_framework import serializers

from campaign.models import Campaign


class CampaignAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['name', 'business_type', 'account_no', 'ifsc_code',
                  'beneficiary_name', 'target_amount', 'pitch', 'type',
                  'reward', 'min_investment', 'end_date', 'debt_interest',
                  'debt_period']
        extra_kwargs = {
            "debt_interest": {"required": False},
            "debt_period": {"required": False},
        }


class CampaignListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['name', 'target_amount', 'type',
                  'reward', 'end_date', 'debt_interest',
                  'debt_period']


class CampaignDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['name', 'business_type', 'target_amount', 'pitch', 'type',
                  'reward', 'min_investment', 'end_date', 'debt_interest',
                  'debt_period']