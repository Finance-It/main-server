from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Campaign(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    business_type = models.CharField(max_length=32)
    account_no = models.IntegerField()
    ifsc_code = models.CharField(max_length=12)
    beneficiary_name = models.TextField()
    target_amount = models.FloatField(
        validators=[MinValueValidator(500), MaxValueValidator(100000000)]
    )
    status = models.CharField(max_length=32)
    type = models.CharField(max_length=20)
    pitch = models.TextField()
    reward = models.TextField(null=True, blank=True)
    min_investment = models.FloatField(
        validators=[MinValueValidator(100), MaxValueValidator(1000000)]
    )
    end_date = models.DateTimeField()
    debt_interest = models.FloatField()
    debt_period = models.IntegerField()

