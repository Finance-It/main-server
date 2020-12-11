import os
from datetime import datetime

import pytz
import razorpay
from celery.schedules import crontab
from celery.task import periodic_task

from campaign.models import Campaign
from investor.models import Investment

razorpay_client = razorpay.Client(auth=(os.environ['RAZORPAY_KEY_ID'],
                                        os.environ['RAZORPAY_KEY_SECRET']))


@periodic_task(run_every=crontab(minute=0, hour=0))
def campaign_target_check():
    curr_time = datetime.now(tz=pytz.UTC)

    for campaign in Campaign.objects.filter(end_date__lte=curr_time, ):
        if campaign.total_amount < campaign.target_amount:
            print('Generate Refund')
            generate_refund(campaign)
    return


def generate_refund(campaign):
    investments = Investment.objects.filter(campaign=campaign)

    for investor in investments:
        payment_id = investor.razorpay_payment_id
        response = razorpay_client.payment.refund(payment_id)
        investor.razorpay_refund_id = response.id
        investor.save()
    return
