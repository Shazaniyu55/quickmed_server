from rest_framework import serializers
from .models import UserSessionModel



class FirebaseUsersAuthenticationSerializer(serializers.Serializer):
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



class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSessionModel
        fields = ['user', 'token', 'created_at', 'expires_at']


class SecureUsersForStorageSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)



class SecureUsersForTelemedicsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureUsersForReadingMessagesSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureUsersToUploadToStorageSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)

class SecureUsersForDownloadingAssetsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureUsersForDeletingAssetsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)


class SecureUsersForSubscriptionClaimsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    custom_claims = serializers.DictField(required=False)


class SecureUsersForPhoneSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)  
    verification_code = serializers.CharField(max_length=6, required=True)  




class UsersPasswordResetSerializer(serializers.Serializer):
    firebase_uid = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)




class SecureUsersSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    firebase_token = serializers.CharField(max_length=500, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)




class UsersDeleteFileSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    firebase_token = serializers.CharField(max_length=500, required=True)
    users_server_session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)
    collection_name = serializers.CharField(max_length=100, required=True)
    document_id = serializers.CharField(max_length=100, required=True)



class SecureUsersForListingFirestoreFilesSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)


class SecureUsersForLogoutSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    session_token = serializers.CharField(max_length=64)