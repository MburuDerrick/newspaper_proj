import requests
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt

import logging
import base64
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_mpesa_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    if settings.MPESA_ENV == 'production':
        url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    response.raise_for_status()
    return response.json()['access_token']




def register_urls(request):
    access_token = generate_mpesa_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    if settings.MPESA_ENV == 'production':
        url = "https://api.safaricom.co.ke/mpesa/c2b/v1/registerurl"

    payload = {
        "ShortCode": settings.MPESA_PAYBILL,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://ff3d-102-167-236-16.ngrok-free.app/mpesa/confirmation/",
        "ValidationURL": "https://ff3d-102-167-236-16.ngrok-free.app/mpesa/validation/",
        #"ConfirmationURL": request.build_absolute_uri(reverse('mpesa_confirmation')),
        #"ValidationURL": request.build_absolute_uri(reverse('mpesa_validation')),
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


    response = requests.post(url, json=payload, headers=headers)
    return response.json()



def generate_lipa_na_mpesa_password():
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = f"{shortcode}{passkey}{timestamp}"
    encoded_password = base64.b64encode(password.encode()).decode()
    return encoded_password, timestamp


def simulate_c2b_payment(amount, account_number, phone_number):
    try:
        access_token = generate_mpesa_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
        payload = {
            "ShortCode": "600247",
            "CommandID": "CustomerPayBillOnline",
            "Amount": amount,
            "Msisdn": phone_number,
            "BillRefNumber": account_number,
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error simulating payment: {e}")
        return None

def lipa_na_mpesa_online(phone_number, amount):
    try:
        access_token = generate_mpesa_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        if settings.MPESA_ENV == 'production':
            url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        password, timestamp = generate_lipa_na_mpesa_password()

        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://ff3d-102-167-236-16.ngrok-free.app/mpesa/confirmation/",
            "AccountReference": "SUB123",
            "TransactionDesc": "Payment for subscription"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in Lipa na M-Pesa Online Payment: {e}")
        return None
