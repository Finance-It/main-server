import os
from datetime import datetime

import pytz
import razorpay
import requests
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from requests.auth import HTTPBasicAuth

from campaign.models import Campaign
from investor.models import Investment

razorpay_client = razorpay.Client(auth=(os.environ['RAZORPAY_KEY_ID'],
                                        os.environ['RAZORPAY_KEY_SECRET']))
logger = get_task_logger(__name__)


@periodic_task(run_every=crontab())
def campaign_target_check():
    curr_time = datetime.now(tz=pytz.UTC)
    campaings = Campaign.objects.filter(end_date__lte=curr_time, )
    if campaings.exists():
        for campaign in campaings:
            if campaign.total_amount < campaign.target_amount:
                logger.info('Generate Refund')
                generate_refund(campaign)
            else:
                logger.info("Campaign Success")
                transfer_to_campaign(campaign)
    return


def generate_refund(campaign):
    investments = Investment.objects.filter(campaign=campaign, status="PAID")
    if investments.exists():
        for investment in investments:
            payment_id = investment.razorpay_payment_id
            response = razorpay_client.payment.refund(payment_id, int(
                investment.amount * 100))
            investment.razorpay_refund_id = response['id']
            investment.status = 'REFUND_INITIATED'
            investment.save()
    return


def transfer_to_campaign(campaign):
    if campaign.status != 'ACTIVE':
        return

    url = '{}/transfers'.format(os.environ['RAZORPAY_BASE_URL'])
    data = {
        "account": campaign.razorpay_payout_acc_id,
        "amount": int(campaign.total_amount * 100),
        "currency": "INR"
    }
    auth = HTTPBasicAuth(os.environ['RAZORPAY_KEY_ID'],
                         os.environ['RAZORPAY_KEY_SECRET'])
    res = requests.post(url, json=data, auth=auth)
    if res.status_code == 200:
        campaign.status = 'TRANSFER_INITIATED'
        campaign.save()