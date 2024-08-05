from rest_framework import serializers

class WalletTopUpSerializer(serializers.Serializer):
    tx_ref = serializers.CharField(required=False, max_length=50)
    amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    currency = serializers.ChoiceField(choices=["NGN", "USD", "EUR"], required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.RegexField(regex=r'^\+?1?\d{9,15}$', required=True, error_messages={'invalid': 'Enter a valid phone number.'})
    name = serializers.CharField(required=True, max_length=100)
    firebase_token = serializers.CharField(required=False, max_length=100)
    user_id = serializers.CharField(required=False, max_length=100)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class WalletWithrawalSerializer(serializers.Serializer):
    withdrawal_amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    session_token = serializers.CharField(required=True, max_length=100)
    user_id = serializers.CharField(required=True, max_length=100)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value



class PaymentSuccessSerializer(serializers.Serializer):
    withdrawal_amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    session_token = serializers.CharField(required=True, max_length=100)
    user_id = serializers.CharField(required=True, max_length=100)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value



