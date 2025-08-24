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







# ================== grafic serializer =====================

from rest_framework import serializers
from .models import Check
import calendar
import locale

# Установим русскую локаль для правильного отображения месяца
# try:
#     locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
# except locale.Error:
#     # Fallback, если система не поддерживает ru_RU.UTF-8
#     locale.setlocale(locale.LC_TIME, '')

# class GraphicCheckSerializer(serializers.ModelSerializer):
#     month_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Check
#         fields = ['created_at', 'consumption', 'current_check_date', 'month_name']

#     def get_month_name(self, obj):
#         month = obj.created_at.strftime('%B') 

#         if (month.lower() == 'january'):
#             return 'Январь'
#         elif (month.lower() == 'february'):
#             return 'Февраль'
#         elif (month.lower() == 'march'):
#             return 'Март'
#         elif (month.lower() == 'april'):
#             return 'Апрель'
#         elif (month.lower() == 'may'):
#             return 'Май'
#         elif (month.lower() == 'june'):
#             return 'Июнь'
#         elif (month.lower() == 'july'):
#             return 'Июль'
#         elif (month.lower() == 'august'):
#             return 'Август'
#         elif (month.lower() == 'september'):
#             return 'Сентябрь'
#         elif (month.lower() == 'october'):
#             return 'Октябрь'
#         elif (month.lower() == 'november'):
#             return 'Ноябрь'
#         elif (month.lower() == 'december'):
#             return 'Декабрь'
#         else:
#             return '??????'
        
from rest_framework import serializers
from .models import Check

MONTH_NAMES = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
    5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
    9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}


class GraphicCheckItemSerializer(serializers.ModelSerializer):
    month_name = serializers.SerializerMethodField()

    class Meta:
        model = Check
        fields = ['created_at', 'consumption', 'current_check_date', 'month_name']

    def get_month_name(self, obj):
        m = getattr(obj, 'created_at', None)
        if not m:
            return ''
        return MONTH_NAMES.get(m.month, '')








# ============================ Photo update serializer =========================

class PhotoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ['id', 'counter_photo', 'counter_current_check']
        read_only_fields = ['id']

class CheckVerificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ['counter_current_check']

    def update(self, instance, validated_data):
        instance.counter_current_check = validated_data.get('counter_current_check', instance.counter_current_check)
        instance.current_check = validated_data.get('counter_current_check', instance.counter_current_check)
        instance.consumption = validated_data.get('counter_current_check', instance.counter_current_check) - validated_data.get('previous_check', instance.previous_check)
        instance.verified = True  # Принудительно подтверждаем
        instance.save()
        return instance



class HouseCardShortUnverifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseCard
        fields = ['id', 'house_card']

class UserShortUnverifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class CheckShortListUnverifiedSerializer(serializers.ModelSerializer):
    house_card = HouseCardShortUnverifiedSerializer()
    username = UserShortUnverifiedSerializer()

    class Meta:
        model = Check
        fields = ['id', 'house_card', 'username', 'created_at']

class CheckRetrieveUnverifiedSerializer(serializers.ModelSerializer):
    house_card = HouseCardShortUnverifiedSerializer()
    username = UserShortUnverifiedSerializer()

    class Meta:
        model = Check
        fields = ['id', 'house_card', 'username', 'counter_photo', 'counter_current_check', 'created_at']
