from rest_framework import serializers
from .models import EconsultantSessionModel



class FirebaseEconsultantAuthenticationSerializer(serializers.Serializer):
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



class EconsultantSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconsultantSessionModel
        fields = ['user', 'token', 'created_at', 'expires_at']


class SecureEconsultantForStorageSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)



class SecureEconsultantForTelemedicsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureEconsultantForReadingMessagesSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureEconsultantToUploadToStorageSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)

class SecureEconsultantForDownloadingAssetsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureEconsultantForDeletingAssetsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)


class SecureEconsultantForSubscriptionClaimsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    subscription_claims = serializers.DictField(required=False)


class SecureEconsultantForPhoneSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)  
    verification_code = serializers.CharField(max_length=6, required=True)  




class EconsultantPasswordResetSerializer(serializers.Serializer):
    firebase_uid = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)




class SecureEconsultantSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    firebase_token = serializers.CharField(max_length=500, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)




class DeleteEconsultantFileSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    firebase_token = serializers.CharField(max_length=500, required=True)
    users_server_session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)
    collection_name = serializers.CharField(max_length=100, required=True)
    document_id = serializers.CharField(max_length=100, required=True)



class SecureEconsultantForListingFirestoreFilesSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)