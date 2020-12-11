from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
from django.db.models import Sum

from investor.models import Investment


class Campaign(models.Model):
    id = models.AutoField(primary_key=True)
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
    pitch = models.TextField()
    type = models.CharField(max_length=20)
    reward = models.TextField(null=True, blank=True)
    min_investment = models.FloatField(
        validators=[MinValueValidator(100), MaxValueValidator(1000000)]
    )
    end_date = models.DateTimeField()
    debt_interest = models.FloatField(null=True, blank=True)
    debt_period = models.IntegerField(null=True, blank=True)
    debt_amount_received = models.FloatField(default=0)
    virtual_acc_no = models.CharField(max_length=20, null=True, blank=True)
    virtual_acc_name = models.CharField(max_length=40, null=True, blank=True)
    virtual_acc_ifsc = models.CharField(max_length=20, null=True, blank=True)
    razorpay_virtual_acc_id = models.CharField(max_length=20, null=True, blank=True)

    @property
    def total_amount(self):
        investments = Investment.objects.filter(campaign=self, status='PAID')
        return investments.aggregate(Sum('amount'))['amount__sum']
