# Create your views here.
import json
import os

import razorpay as razorpay
import requests
from django.http import JsonResponse, HttpResponseRedirect
from razorpay.errors import SignatureVerificationError
from requests.auth import HTTPBasicAuth
from rest_framework import permissions
from rest_framework.views import APIView

from investor.models import Investment
from payments.permissions import IsInvestorOfInvestment
from payments.utils import verify_signature


class InvestmentPayment(APIView):
    permission_classes = [permissions.IsAuthenticated, IsInvestorOfInvestment]

    def post(self, request, id):
        investments = Investment.objects.filter(pk=id)
        if not investments.exists():
            return JsonResponse({"details": "Not found"}, status=404)
        investment = investments.first()
        if investment.razorpay_invoice_id is None:
            url = '{}/invoices/'.format(os.environ['RAZORPAY_BASE_URL'])
            data = {
                "type": "link",
                "view_less": 1,
                "amount": int(investment.amount * 100),
                "description": "Payment Link for InvestorId {} campaignId {}".format(
                    investment.investor.id, investment.campaign.id),
                "callback_url": 'http://0.0.0.0:8000/payments/callbacks/investments',
                "callback_method": 'get'
            }
            auth = HTTPBasicAuth(os.environ['RAZORPAY_KEY_ID'],
                                 os.environ['RAZORPAY_KEY_SECRET'])
            res = requests.post(url, data, auth=auth)
            payment = res.json()
            investment.status = 'INITIATED'
            investment.razorpay_invoice_id = payment['id']
            investment.razorpay_payment_link = payment['short_url']
            investment.save()
            return JsonResponse({
                "status": "Success",
                "link": payment['short_url']
            })
        else:
            return JsonResponse(
                {"details": "Payment already initiated / completed"},
                status=400)


razorpay_client = razorpay.Client(auth=(os.environ['RAZORPAY_KEY_ID'],
                                  os.environ['RAZORPAY_KEY_SECRET']))


class CallBackInvestmentPayment(APIView):
    def get(self, request):
        # Verify razorpay sign
        razorpay_payment_id = request.GET.get('razorpay_payment_id', None)
        razorpay_invoice_id = request.GET.get('razorpay_invoice_id', None)
        razorpay_invoice_status = request.GET.get('razorpay_invoice_status', None)
        razorpay_signature = request.GET.get('razorpay_signature', None)

        if not (razorpay_payment_id and razorpay_invoice_id and razorpay_invoice_status and razorpay_signature):
            return JsonResponse({"details": "Bad request"}, status=400)

        signature_payload = razorpay_invoice_id + '|' + '' + '|' + razorpay_invoice_status + '|' + razorpay_payment_id
        is_sign_verified = verify_signature(signature_payload, razorpay_signature, os.environ['RAZORPAY_KEY_SECRET'])

        if not is_sign_verified:
            return JsonResponse({"details": "Invalid request"}, status=400)

        # Save status
        if razorpay_invoice_status == 'paid':
            investment = Investment.objects.filter(razorpay_invoice_id=razorpay_invoice_id).first()
            investment.status = 'PAID'
            investment.razorpay_payment_id = razorpay_payment_id
            investment.save()
            return HttpResponseRedirect(redirect_to='http://0.0.0.0:8000/swagger')
        else:
            return JsonResponse({"details": "Payment failed"},
                                status=400)


# WebHooks:

class RazorpayWebhook(APIView):
    def post(self, request):
        # Verify razorpay sign
        try:
            razorpay_client.utility.verify_webhook_signature(request.body.decode(), request.headers.get('x-razorpay-signature', ''), 'secretbc')
        except SignatureVerificationError:
            return JsonResponse({"details": "Rejected"})

        payload = json.loads(request.body.decode())
        event_type = payload['event']

        if event_type == 'payment.captured':
            payment_entity = payload['payload']['payment']['entity']
            invoice_id = payment_entity['invoice_id']

            investment = Investment.objects.filter(
                razorpay_invoice_id=invoice_id).first()
            if investment.status != 'PAID':
                investment.status = 'PAID'
                investment.razorpay_payment_id = payment_entity['id']
                investment.save()
        else:
            print(event_type)

        return JsonResponse({})
