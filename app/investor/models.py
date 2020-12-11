from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from campaign.models import Campaign


class Investment(models.Model):
    investor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL,
                                 null=True)
    amount = models.FloatField(
        validators=[MinValueValidator(100), MaxValueValidator(1000000)]
    )
