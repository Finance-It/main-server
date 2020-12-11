from datetime import datetime

import pytz
from rest_framework.permissions import BasePermission

from campaign.models import Campaign
from investor.models import Investment


class IsCampaignActive(BasePermission):
    message = "Access denied. Reason: outside contest time"

    def has_permission(self, request, view):
        curr_time = datetime.now(tz=pytz.UTC)
        return Campaign.objects.filter(
            id=request.data['campaign'],
            end_date__gte=curr_time,
        ).count() > 0


class IsInvestorOfInvestment(BasePermission):
    def has_permission(self, request, view):
        return Investment.objects.filter(id=view.kwargs['id'], investor=request.user).exists()