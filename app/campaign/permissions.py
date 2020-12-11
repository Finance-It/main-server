from datetime import datetime

import pytz
from rest_framework.permissions import BasePermission


class IsCampaignAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by


class IsUpdateAllowedOrReadOnly(BasePermission):
    message = "Can't edit after campaign end"

    def has_object_permission(self, request, view, obj):
        return not (request.method == 'POST' and obj.end_date > datetime.now(
            tz=pytz.UTC))
