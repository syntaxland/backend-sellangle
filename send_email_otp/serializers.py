from rest_framework import serializers

class EmailOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

class EmailOTPSendSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100, required=False)
