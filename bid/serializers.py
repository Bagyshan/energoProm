from rest_framework import serializers
from .models import Bid, Deal




class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'



class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'