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
    campaigns = Campaign.objects.filter(end_date__lte=curr_time, )
    if campaigns.exists():
        for campaign in campaigns:
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

    # TODO: create a linked account and return account id

    if campaign.razorpay_virtual_acc_id is None:
        url = '{}/beta/accounts'.format(os.environ['RAZORPAY_BASE_URL'])
        data = {
            "name": '{} {}'.format(campaign.created_by.first_name,
                                   campaign.created_by.last_name),
            "email": campaign.created_by.email,
            "tnc_accepted": True,
            "account_details": {
                "business_name": campaign.business_name,
                "business_type": campaign.business_type
            },
            "bank_account": {
                "ifsc_code": campaign.ifsc_code,
                "beneficiary_name": campaign.beneficiary_name,
                "account_number": campaign.account_no
            }
        }
        auth = HTTPBasicAuth(os.environ['RAZORPAY_KEY_ID'],
                             os.environ['RAZORPAY_KEY_SECRET'])
        res = requests.post(url, json=data, auth=auth)
        payload = res.json()
        if 'error' in payload:
            print(payload)
            return
        campaign.razorpay_payout_acc_id = payload['id']
        campaign.save()

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
