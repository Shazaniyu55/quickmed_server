import logging
import jwt
import os
import firebase_admin
from rest_framework.decorators import api_view
from django.http import JsonResponse
from venv import logger
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from firebase_admin import auth, firestore
from utils.helpers.users_helper_functions import authenticate_firebase_token, authenticate_phone_number, delete_file_from_firestore, reset_user_password, verify_otp
from .serializers import AmbulancePasswordResetSerializer, AmbulanceSessionSerializer, DeleteAmbulanceFileSerializer, FirebaseAmbulanceAuthenticationSerializer, SecureAmbulanceForDeletingAssetsSerializer, SecureAmbulanceForDownloadingAssetsSerializer, SecureAmbulanceForListingFirestoreFilesSerializer, SecureAmbulanceForPhoneSerializer, SecureAmbulanceForReadingMessagesSerializer, SecureAmbulanceForStorageSerializer, SecureAmbulanceForSubscriptionClaimsSerializer, SecureAmbulanceForTelemedicsSerializer, SecureAmbulanceToUploadToStorageSerializer
from drf_spectacular .utils import extend_schema




app_secrete_key = os.getenv("app_secrete_key")
@extend_schema(responses=FirebaseAmbulanceAuthenticationSerializer)
@api_view(['POST'])
def authenticate_ambulance(request):
    logger = logging.getLogger(__name__)
    logger.info("Received authentication request payload")

    serializer = FirebaseAmbulanceAuthenticationSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error("Invalid data received for authentication")
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    firebase_id_token = validated_data.get('firebase_id_token')
    otp = validated_data.get('otp')
    phone_number = validated_data.get('phone_number')

    try:
        logger.info("Verifying Firebase ID token")
        authenticated_firebase_token = auth.verify_id_token(firebase_id_token)
        user_id = authenticated_firebase_token['uid']
        logger.info(f"User authenticated: {user_id}")

        if not verify_otp(user_id, otp, phone_number):
            logger.error('OTP verification failed')
            return JsonResponse({'error': 'OTP verification failed'}, status=status.HTTP_401_UNAUTHORIZED)

        token_payload = {
            'user_id': user_id,
        }

        session_token = jwt.encode(token_payload, app_secrete_key, algorithm='HS256')
        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        user_doc_ref.set({'session_token': session_token})

       
        return JsonResponse({'success': f"User securely authenticated {True}", 'user_id': user_id, 'session_token': session_token}, status=status.HTTP_200_OK)

    except auth.ExpiredIdTokenError:
        logger.error('Firebase authentication error: ID token has expired')
        return JsonResponse({'error': 'ID token has expired'}, status=status.HTTP_401_UNAUTHORIZED)

    except auth.InvalidIdTokenError:
        logger.error('Firebase authentication error: Invalid ID token')
        return JsonResponse({'error': 'Invalid ID token'}, status=status.HTTP_401_UNAUTHORIZED)

    except auth.FirebaseAuthError as e:
        logger.error(f'Firebase authentication error: {e}')
        return JsonResponse({'error': f'Firebase authentication error: {e.code}'}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        logger.exception(f'Unexpected error during authentication: {e}')
        return JsonResponse({'error': 'Unexpected error during authentication'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@extend_schema(responses=AmbulanceSessionSerializer)
@api_view(['POST'])
@csrf_exempt
def secure_ambulance_for_messaging(request):
    logger.info("Received request to secure user for messaging")
    
    serializer = AmbulanceSessionSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error("Invalid data received for authentication")
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    user_id = validated_data.get('user_id')
    session_token = validated_data.get('session_token')
    


    if not user_id or not session_token:
        logger.error("User ID or session token missing in request data")
        return JsonResponse({'error': 'User ID or session token missing'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        
        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)

        return JsonResponse({'response': 'Proceed to start messaging'}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    



@extend_schema(responses=SecureAmbulanceForStorageSerializer)
@api_view(['POST'])
@csrf_exempt
def secure_ambulance_for_storage(request):
    logger.info("Received request to secure users for storage")
    
    serializer = AmbulanceSessionSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error("Invalid data received for securing users for storage")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    user_id = validated_data.get('user_id')
    firebase_token = validated_data.get('firebase_token')
    session_token = validated_data.get('session_token')
    
    if not authenticate_firebase_token(user_id, firebase_token):
        logger.error("Invalid Firebase token for the user")
        return Response({'error': 'Invalid Firebase token for the user'}, status=status.HTTP_401_UNAUTHORIZED)
    

    try:

        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(True, {'response': 'Proceed to store data'}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
    





@extend_schema(responses=SecureAmbulanceForTelemedicsSerializer)
@api_view(['POST'])
def secure_ambulance_for_telemedics(request):
    
    serializer = SecureAmbulanceForTelemedicsSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    user_id = serializer.validated_data.get('user_id')
    session_token = serializer.validated_data.get('session_token')

    try:

        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response(True, {'response': 'Proceed to start telemedics'}, status=status.HTTP_200_OK)





@extend_schema(responses=SecureAmbulanceForReadingMessagesSerializer)
@api_view(['POST'])
@csrf_exempt
def secure_ambulance_for_reading_messages(request):
    serializer = SecureAmbulanceForReadingMessagesSerializer(data=request.data)
    
    if not serializer.is_valid():
        logger.error("Invalid data received for securing users for messaging")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = request.data.get('user_id')
    session_token = request.data.get('session_token')
    
    try:

        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response(True, {'response': 'Proceed to reading messages'}, status=status.HTTP_200_OK)






@extend_schema(responses=SecureAmbulanceToUploadToStorageSerializer)
@csrf_exempt
@api_view(['POST'])
def secure_ambulance_to_upload_to_storage(request):
    logger.info("Received request to secure users for storage")
    serializer = SecureAmbulanceToUploadToStorageSerializer(data=request.data)
    
    if not serializer.is_valid():
        logger.error("Invalid data received for securing users for storage")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    user_id = validated_data.get('user_id')
    firebase_token = validated_data.get('firebase_token')
    session_token = validated_data.get('session_token')

    try:

        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response(True, {'response': f"User {firebase_token}Proceed to upload data"}, status=status.HTTP_200_OK)











@extend_schema(responses=SecureAmbulanceForDownloadingAssetsSerializer)
@api_view(['POST'])
@csrf_exempt
def secure_ambulance_for_downloading_assets(request):
    logger.info("Received request to secure users for downloading")
    serializer = SecureAmbulanceForDownloadingAssetsSerializer(data=request.data)
    
    if not serializer.is_valid():
        logger.error("Invalid data received for securing users for downloading")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = request.data.get('user_id')
    session_token = request.data.get('session_token')
    
    try:

        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response(True, {'response': f"User {user_id}Proceed to downloading assets"}, status=status.HTTP_200_OK)

    

    





@extend_schema(responses=SecureAmbulanceForDeletingAssetsSerializer)
@api_view(['POST'])
@csrf_exempt
def secure_ambulance_for_deleting_assets(request):
    logger.info("Received request to secure users for storage")
    
    serializer = SecureAmbulanceForDeletingAssetsSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error("Invalid data received for securing users for storage")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    user_id = validated_data.get('user_id')
    firebase_token = validated_data.get('firebase_token')
    session_token = validated_data.get('session_token')
    
    try:

        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response(True, {'response': f"User {firebase_token}Proceed to deleting assets"}, status=status.HTTP_200_OK)

    


    

@extend_schema(responses=SecureAmbulanceForPhoneSerializer)
@api_view(['POST'])
@csrf_exempt
def secure_ambulance_for_phone_number_verification(request):
    logger.info("Received request to secure users for downloading")
    serializer = SecureAmbulanceForPhoneSerializer(data=request.data)
    
    if not serializer.is_valid():
        logger.error("Invalid data received for securing users for downloading")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = serializer.validated_data.get('user_id')
    session_token = serializer.validated_data.get('session_token')
    phone_number = serializer.validated_data.get('phone_number')
    verification_code = serializer.validated_data.get('verification_code')
    
    try:
        
        if not verify_otp(phone_number, verification_code):
            logger.error("Invalid phone number verification code")
            return Response({'error': 'Invalid phone number verification code'}, status=status.HTTP_401_UNAUTHORIZED)
        
       
        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return Response({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        
        session_token = auth.verify_id_token(user_id)
        if session_token['phone_number'] != phone_number:
            logger.error("Phone number mismatch in custom claims")
            return Response({'error': 'Phone number mismatch in custom claims'}, status=status.HTTP_401_UNAUTHORIZED)
    except auth.InvalidIdTokenError:
        logger.error("Invalid ID token")
        return Response({'error': 'Invalid ID token'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        logger.exception(f"Error verifying ID token: {e}")
        return Response({'error': 'Error verifying ID token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
   
   
    return Response(user_id, status=status.HTTP_200_OK)




@extend_schema(responses=AmbulancePasswordResetSerializer)
@api_view(['POST'])
@csrf_exempt
def ambulance_password_reset(request):
    logger.info("Received request to reset user's password")


    serializer = AmbulancePasswordResetSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error("Invalid data received for password reset")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_id = serializer.validated_data.get('firebase_uid')
    new_password = serializer.validated_data.get('new_password')
    session_token = serializer.validated_data.get('session_token')


    try:
        success, message = reset_user_password(user_id, new_password)
        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response(True, {'response': f"User {message}Proceed to upload data"}, status=status.HTTP_200_OK)

    





@extend_schema(responses=DeleteAmbulanceFileSerializer)
@api_view(['POST'])
@csrf_exempt
def ambulance_delete_file_from_firestore(request):
    api_key = request.headers.get('X-API-Key')

    if api_key != app_secrete_key:
            logger.error("Invalid api_key")
            return JsonResponse({'error': 'Invalid api_key'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = DeleteAmbulanceFileSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error("Invalid data received for deleting file")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    user_id = validated_data.get('user_id')
    firebase_token = validated_data.get('firebase_token')
    session_token = validated_data.get('session_token')
    phone_number = validated_data.get('phone_number')
    collection_name = validated_data.get('collection_name')
    document_id = validated_data.get('document_id')
    
    try:
        
        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    
   
        if not authenticate_phone_number(user_id, phone_number):
            logger.error("Invalid phone number")
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_401_UNAUTHORIZED)
        
        delete_file_from_firestore(collection_name, document_id)
        
    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(True, {'response': f"User {firebase_token}Proceed to upload data"}, status=status.HTTP_200_OK)
        



@extend_schema(responses=SecureAmbulanceForSubscriptionClaimsSerializer)
@api_view(['POST'])
@csrf_exempt
def secure_ambulance_for_subscription_claims(request):
    logger.info("Received request to secure users for downloading")
    serializer = SecureAmbulanceForSubscriptionClaimsSerializer(data=request.data)
    
    if not serializer.is_valid():
        logger.error("Invalid data received for securing users for downloading")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = serializer.validated_data.get('user_id')
    session_token = serializer.validated_data.get('session_token')
    subscription_claims = serializer.validated_data.get('custom_claims')
    
    try:

        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response(True, {'response': f"User {subscription_claims} Proceed to subscription claims"}, status=status.HTTP_200_OK)



    






@extend_schema(responses=SecureAmbulanceForListingFirestoreFilesSerializer)
@api_view(['POST'])
@csrf_exempt
def secure_ambulance_for_listing_firestore_files(request):
    logger.info("Received request to secure users for listing firstore files")
    
    serializer = SecureAmbulanceForListingFirestoreFilesSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error("Invalid data received for securing users for storage")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    user_id = validated_data.get('user_id')
    firebase_token = validated_data.get('firebase_token')
    session_token = validated_data.get('session_token')
    
    try:


        db = firestore.client()
        user_doc_ref = db.collection('users').document(user_id)
        stored_session = user_doc_ref.get().to_dict().get('session_token')

        if session_token != stored_session:
            logger.error("Invalid session token")
            return JsonResponse({'error': 'Invalid session token'}, status=status.HTTP_401_UNAUTHORIZED)
                
        if not authenticate_firebase_token(user_id, firebase_token):
           logger.error("Invalid Firebase token for the user")
           return Response({'error': 'Invalid Firebase token for the user'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.exception(f"Error validating session token: {e}")
        return JsonResponse({'error': 'Error validating session token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response(True, {'response': f"User {session_token}Proceed to upload data"}, status=status.HTTP_200_OK)










