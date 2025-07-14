from rest_framework import serializers

from .models import (
    District,
    GosAdministration,
    Settlement,
    Street,
    Address,

    Executor,
    CounterCause,
    CounterType,
    Counter,

    Tariff, 

    Plot,
    Route, 

    HouseCard,
)
from django.contrib.auth import get_user_model

User = get_user_model()



class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class GosAdministrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GosAdministration
        fields = '__all__'

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'

class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'house', 'liter', 'apartment', 'apartment_liter',
            'created_at', 'updated_at', 'street'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']






class ExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'

class CounterCauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterCause
        fields = '__all__'

class CounterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterType
        fields = '__all__'

class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counter
        fields = [
            'id', 'serial_number', 'pp_number', 'current_indication',
            'year_of_state_inspection', 'quarter_of_state_inspection',
            'energy_sales_seal', 'CRPU_seal', 'seal_on_the_casing',
            'registered_at', 'updated_at', 'cause', 'executor', 'counter_type'
        ]
        read_only_fields = ['id', 'registered_at', 'updated_at']





class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'






class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'






class HouseCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseCard
        fields = '__all__'


class HouseCardCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    counter = CounterSerializer()

    class Meta:
        model = HouseCard
        fields = [
            'personal_account', 'contract_number', 'contract_date',
            'tp_number', 'household_needs', 'fact_summer', 'fact_winter',
            'max_summer', 'max_winter', 'address', 'user', 'plot',
            'route', 'counter', 'tariff'
        ]

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        counter_data = validated_data.pop('counter')

        # Создание вложенных объектов
        address = Address.objects.create(**address_data)
        counter = Counter.objects.create(**counter_data)

        # Создание основной записи
        house_card = HouseCard.objects.create(
            address=address,
            counter=counter,
            **validated_data
        )
        return house_card
    

class HouseCardDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    counter = CounterSerializer()

    class Meta:
        model = HouseCard
        fields = [
            'id', 'personal_account', 'contract_number', 'contract_date',
            'tp_number', 'household_needs', 'fact_summer', 'fact_winter',
            'max_summer', 'max_winter', 'address', 'user', 'plot',
            'route', 'counter', 'tariff', 'registered_at', 'updated_at'
        ]

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        counter_data = validated_data.pop('counter', None)

        if address_data:
            address_serializer = AddressSerializer(instance.address, data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address_serializer.save()

        if counter_data:
            counter_serializer = CounterSerializer(instance.counter, data=counter_data)
            counter_serializer.is_valid(raise_exception=True)
            counter_serializer.save()

        return super().update(instance, validated_data)