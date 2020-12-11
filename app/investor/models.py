from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Investment(models.Model):
    STATUSES = [
        ('PAID', 'PAID'),
        ('PENDING', 'PENDING'),
        ('INITIATED', 'PAYMENT LINK GENERATED'),
        ('NOTPAID', 'NOTPAID'),
        ('REFUND_INITIATED', 'REFUND_INITIATED'),
        ('REFUND_SUCCESS', 'REFUND_SUCCESS')
    ]

    id = models.AutoField(primary_key=True)
    investor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    campaign = models.ForeignKey(to='campaign.Campaign',
                                 on_delete=models.SET_NULL,
                                 null=True, related_name='investments')
    amount = models.FloatField(
        validators=[MinValueValidator(100), MaxValueValidator(1000000)]
    )
    status = models.CharField(max_length=20, choices=STATUSES,
                              default='PENDING')
    razorpay_invoice_id = models.CharField(max_length=20, null=True)
    razorpay_payment_link = models.CharField(max_length=100, null=True)
    razorpay_payment_id = models.CharField(max_length=20, null=True)
    razorpay_refund_id = models.CharField(max_length=20, null=True)

