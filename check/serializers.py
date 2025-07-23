from rest_framework import serializers
from .models import Check
from house_card.models import (
    Street,
    Address,
    Executor,
    Route,
    HouseCard,
    Tariff
)
from user.models import User



class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ['name']

class AddressSerializer(serializers.ModelSerializer):
    street = StreetSerializer()

    class Meta:
        model = Address
        fields = ['street', 'house', 'liter', 'apartment', 'apartment_liter']

class ExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = ['name']

class RouteSerializer(serializers.ModelSerializer):
    executor = ExecutorSerializer()

    class Meta:
        model = Route
        fields = ['route_number', 'executor']

class HouseCardShortSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    route = RouteSerializer()
    
    class Meta:
        model = HouseCard
        fields = [
            'house_card',
            'address',
            'route',
            'overpayment_underpayment',
            'penalty',
        ]

class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'






class CheckSerializer(serializers.ModelSerializer):
    house_card = HouseCardShortSerializer()
    username = UserShortSerializer()
    tariff = TariffSerializer()
    class Meta:
        model = Check
        fields = '__all__'
        read_only_fields = (
            'previous_check',
            'previous_check_date',
            'period_day_count',
            'total_sum',
            'consumption',
            'amount_for_expenses',
            'created_at',
            'updated_at',
        )

