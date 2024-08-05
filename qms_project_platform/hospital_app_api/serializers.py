from rest_framework import serializers
from .models import HospitalSessionModel



class FirebaseHospitalAuthenticationSerializer(serializers.Serializer):
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



class HospitalSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalSessionModel
        fields = ['user', 'token', 'created_at', 'expires_at']


class SecureHospitalForStorageSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)



class SecureHospitalForTelemedicsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureHospitalForReadingMessagesSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureHospitalToUploadToStorageSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)

class SecureHospitalForDownloadingAssetsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True, allow_blank=False)
    session_token = serializers.CharField(max_length=64, required=True, allow_blank=False)


class SecureHospitalForDeletingAssetsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)


class SecureHospitalForSubscriptionClaimsSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    custom_claims = serializers.DictField(required=False)


class SecureHospitalForPhoneSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)  
    verification_code = serializers.CharField(max_length=6, required=True)  




class HospitalPasswordResetSerializer(serializers.Serializer):
    firebase_uid = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)




class SecureHospitalSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    firebase_token = serializers.CharField(max_length=500, required=True)
    session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)




class DeleteHospitalFileSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    firebase_token = serializers.CharField(max_length=500, required=True)
    users_server_session_token = serializers.CharField(max_length=64, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)
    collection_name = serializers.CharField(max_length=100, required=True)
    document_id = serializers.CharField(max_length=100, required=True)



class SecureHospitalForListingFirestoreFilesSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    firebase_token = serializers.CharField(max_length=500)
    session_token = serializers.CharField(max_length=64)