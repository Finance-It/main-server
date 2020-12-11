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
    campaings = Campaign.objects.filter(end_date__lte=curr_time, )
    if campaings.exist:
        for campaign in campaings:
            if campaign.total_amount < campaign.target_amount:
                print('Generate Refund')
                generate_refund(campaign)
    return


def generate_refund(campaign):
    investments = Investment.objects.filter(campaign=campaign, status="PAID")
    if investments.exist:
        for investment in investments:
            payment_id = investment.razorpay_payment_id
            response = razorpay_client.payment.refund(payment_id)
            investment.razorpay_refund_id = response.id
            investment.save()
    return
