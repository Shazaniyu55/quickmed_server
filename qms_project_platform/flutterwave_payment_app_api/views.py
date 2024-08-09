import logging
import requests
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from venv import logger
import os
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import auth, firestore
from utils.helpers.users_helper_functions import authenticate_firebase_token, calculate_wallet_balance, calculate_withdrawal_amount
from .serializers import PaymentSuccessSerializer, WalletTopUpSerializer, WalletWithrawalSerializer
from drf_spectacular .utils import extend_schema
import logging
from rest_framework import status


logger = logging.getLogger(__name__)



flutterwave_secret_key = os.getenv("flutterwave_secrete_key")
app_secrete_key = os.getenv("app_secrete_key")
@extend_schema(responses=WalletTopUpSerializer)
@api_view(['POST'])
@csrf_exempt
def wallet_top_up(request, *args, **kwargs):
    try:
       
       tx_ref = request.data.get("tx_ref")
       amount = request.data.get("amount")
       currency = request.data.get("currency")
       email = request.data.get("email")
       phone_number = request.data.get("phone_number")
       name = request.data.get("name")
       
        # firebase_token = request.data.get("firebase_token")
        # user_id = request.data.get("user_id")

        # Convert amount to float and validate
       """try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
       except (ValueError, TypeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)"""

        # Prepare payload
       payload = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": currency,
            "redirect_url": 'http://127.0.0.1:8000/flutterwave/api/payment_success_redirect/',
            "customer": {
                "email": email,
                "phonenumber": phone_number,
                "name": name
            },
            "customizations": {
                "title": "Quickmed Wallet Payment",
                "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
            }
        }

       headers = {
            'Authorization': f'Bearer FLWPUBK_TEST-752f397aab636da73ceec264d04842ab-X',
            'Content-Type': 'application/json',
        }

       response = requests.post("https://api.flutterwave.com/v3/payments", headers=headers, json=payload)

        # Log response details
       logger.info(f"Response Status Code: {response.status_code}")
       logger.info(f"Response Content: {response.text}")

        # Try to parse JSON response
        # try:
        #     response_data = response.json()
        # except requests.exceptions.JSONDecodeError:
        #     logger.error("Failed to decode JSON from response")
        #     response_data = {"error": "Invalid response format"}
        #     return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

       return Response({response}, status=response.status_code)

    except Exception as e:
        logger.exception("An error occurred in wallet_top_up view")
        return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

         
         


       
  
#   try:
#         # serializer = WalletTopUpSerializer(data=request.data)
#         # if not serializer.is_valid():
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # validated_data = serializer.validated_data

        
#         tx_ref = validated_data['tx_ref']
#         amount = validated_data['amount']
#         currency = validated_data['currency']
#         email = validated_data['email']
#         # phone_number = validated_data['phone_number']
#         # name = validated_data['name']
#         # firebase_token = validated_data['firebase_token']
#         # user_id = validated_data['user_id']

       
#         if not authenticate_firebase_token(user_id, firebase_token):
#             return Response({"error": "Invalid Firebase token or user ID"}, status=status.HTTP_401_UNAUTHORIZED)

        
#         payload = {
#             "tx_ref": tx_ref,
#             "amount": amount,
#             "currency": currency,
#             "redirect_url": 'http://127.0.0.1:8000/flutterwave/api/payment_success_redirect/',
#             "customer": {
#                 "email": email,
#                 "phonenumber": phone_number,
#                 "name": name
#             },
#             "customizations": {
#                 "title": "Quickmed Wallet Payment",
#                 "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
#             }
#         }

#         headers = {
#             'Authorization': f'Bearer {flutterwave_secret_key}',
#             'Content-Type': 'application/json',
#         }

    
#         response = requests.post("https://api.flutterwave.com/v3/payments", headers=headers, json=payload)

        
#         if response.ok:
#             return Response(response.json(), status=status.HTTP_200_OK)
#         else:
#             return Response(response.json(), status=response.status_code)
        
#   except Exception as e:
#         logger.exception("An error occurred in wallet_top_up view")
#         return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        








@extend_schema(responses=WalletWithrawalSerializer)
@api_view(['POST'])
@csrf_exempt
def wallet_withdrawal(request, *args, **kwargs):
    try:
        serializer = WalletWithrawalSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Invalid data received for authentication")
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        withdrawal_amount = validated_data.get('withdrawal_amount')
        session_token = validated_data.get('session_token')
        user_id = validated_data.get('user_id')

        db = firestore.client()
        user_doc_ref = db.collection('userswallet').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)

       
        withdrawal_details = calculate_withdrawal_amount(user_id, withdrawal_amount)
        if withdrawal_details:

            return Response(f"Here is this user's details: {withdrawal_details} , kindly allow user make withdrawal from {withdrawal_amount.withdrawal_amount}", status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User wallet not elligible'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def payment_success_redirect(request, *args, **kwargs):
    try:
        serializer = PaymentSuccessSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Invalid data received for authentication")
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        session_token = validated_data.get('session_token')
        user_id = validated_data.get('user_id')
        withdrawal_amount = validated_data.get('withdrawal_amount')
        
        latest_withdrawal_details = calculate_withdrawal_amount(user_id, withdrawal_amount)

        db = firestore.client()
        user_doc_ref = db.collection('userswallet').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')


        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)

        if latest_withdrawal_details.withdrawal_amount == withdrawal_amount:
           return Response(f"response: securely allow the user{user_doc_ref} to be redirected to home or wallet screen", status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User wallet transaction session has being compromised cannot redirect'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



