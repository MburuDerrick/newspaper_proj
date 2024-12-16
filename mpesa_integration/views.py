from django.shortcuts import render

# Create your views here.
import json
import requests
#from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



#from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
#from .utils import simulate_c2b_payment
from .utils import lipa_na_mpesa_online

def subscribe(request):
    """
    Handles subscription requests via Lipa na M-Pesa Online (STK Push).
    """
    if request.method == "POST":
        amount = request.POST.get("amount", 100)  # Default amount is 100
        phone_number = request.POST.get("phone_number")  # Must be entered by the user
        
        if not phone_number:
            return JsonResponse({"error": "Phone number is required"}, status=400)

        try:
            result = lipa_na_mpesa_online(phone_number, amount)
            if result:
                return JsonResponse(result)
            else:
                return JsonResponse({"error": "Payment request failed"}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "subscribe.html")



@csrf_exempt
def mpesa_validation(request):
    """
    Handles M-Pesa Validation requests sent by Safaricom.
    You can add custom logic to validate the transaction before it's processed.
    """
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Log the validation data for debugging purposes (optional)
            print("Validation Request Received:", data)
            
            # Validate payment (custom logic can be added here)
            # Example: Check if the account number exists or the amount is valid
            
            # Respond to Safaricom (0: Accepted, 1: Rejected)
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Validation successful"})
        except Exception as e:
            print(f"Error in validation: {e}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Validation failed"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid request"})


@csrf_exempt
def mpesa_confirmation(request):
    """
    Handles M-Pesa Confirmation requests sent by Safaricom.
    This is triggered after a payment is successfully processed.
    """
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Log the confirmation data for debugging purposes (optional)
            print("Confirmation Request Received:", data)
            
            # Extract relevant data from the payload
            transaction_id = data.get("TransID")
            amount = data.get("TransAmount")
            phone_number = data.get("MSISDN")
            account_number = data.get("BillRefNumber")
            transaction_time = data.get("TransTime")
            
            # Save the transaction to the database (if needed)
            # Example:
            # Payment.objects.create(
            #     transaction_id=transaction_id,
            #     amount=amount,
            #     phone_number=phone_number,
            #     account_number=account_number,
            #     transaction_time=transaction_time
            # )
            
            # Respond to Safaricom
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Confirmation received successfully"})
        except Exception as e:
            print(f"Error in confirmation: {e}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Confirmation failed"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid request"})

