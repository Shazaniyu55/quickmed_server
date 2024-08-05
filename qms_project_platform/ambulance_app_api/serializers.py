from rest_framework import serializers
from .models import AmbulanceSessionModel



class FirebaseAmbulanceAuthenticationSerializer(serializers.Serializer):
    firebase_id_token = serializers.CharField(max_length=1024, required=True, allow_blank=False)
    otp = serializers.CharField(max_length=10, required=True, allow_blank=False)
    phone_number = serializers.CharField(max_length=20, required=True, allow_blank=False)

    def validate(self, attrs):
        firebase_id_token = attrs.get('firebase_id_token')
        otp = attrs.get('otp')
        phone_number = attrs.get('phone_number')

       
        if not firebase_id_token:
            raise serializers.ValidationError("Firebase ID token is required")
        if not otp:
            raise serializers.ValidationError("OTP is required")
        if not phone_number:
            raise serializers.ValidationError("Phone number is required")
        
        return attrs



class AmbulanceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbulanceSessionModel
        fields = ['user', 'token', 'created_at', 'expires_at']


class SecureAmbulanceForStorageSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)



class SecureAmbulanceForTelemedicsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureAmbulanceForReadingMessagesSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureAmbulanceToUploadToStorageSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)

class SecureAmbulanceForDownloadingAssetsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureAmbulanceForDeletingAssetsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)


class SecureAmbulanceForSubscriptionClaimsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    custom_claims = serializers.DictField(required=False)


class SecureAmbulanceForPhoneSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)  
    verification_code = serializers.CharField(max_length=6, required=True)  




class AmbulancePasswordResetSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
    session_token = serializers.CharField(max_length=64, required=True)



class SecureAmbulanceSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    firebase_token = serializers.CharField(max_length=500, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)




class DeleteAmbulanceFileSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    firebase_token = serializers.CharField(max_length=500, required=True)
    users_server_session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)
    collection_name = serializers.CharField(max_length=100, required=True)
    document_id = serializers.CharField(max_length=100, required=True)



class SecureAmbulanceForListingFirestoreFilesSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)