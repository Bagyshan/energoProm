from rest_framework import serializers
from .models import ExpoPushToken

class ExpoPushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpoPushToken
        fields = ['token', 'device_type']

    def create(self, validated_data):
        user = self.context['request'].user
        token, _ = ExpoPushToken.objects.update_or_create(
            user=user,
            token=validated_data['token'],
            defaults={'device_type': validated_data['device_type']}
        )
        return token
