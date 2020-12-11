from datetime import datetime

import pytz
from rest_framework.permissions import BasePermission

from campaign.models import Campaign


class IsCampaignActive(BasePermission):
    message = "Access denied. Reason: outside contest time"

    def has_permission(self, request, view):
        curr_time = datetime.now(tz=pytz.UTC)
        return Campaign.objects.filter(
            id=request.data['campaign'],
            end_date__gte=curr_time,
        ).count() > 0
