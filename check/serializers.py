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
    counter_photo = serializers.SerializerMethodField()
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
    
    def get_counter_photo(self, obj):
        """
        Возвращает абсолютный URL к фото через request.build_absolute_uri
        """
        request = self.context.get("request")
        if obj.counter_photo and hasattr(obj.counter_photo, "url"):
            url = obj.counter_photo.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None







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


class GraphicCheckAggregatedSerializer(serializers.Serializer):
    average_consumption = serializers.FloatField()
    diff_amount = serializers.FloatField(allow_null=True)
    diff_percent = serializers.FloatField(allow_null=True)
    graphic_evaluate = GraphicCheckItemSerializer(many=True) 







# ============================ Photo update serializer =========================

# class PhotoUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Check
#         fields = ['id', 'counter_photo', 'counter_current_check']
#         read_only_fields = ['id']
from decimal import Decimal, ROUND_HALF_UP
from .tasks import send_expo_push_notification
import math
from django.db import transaction
import logging


# def custom_round(value: Decimal | float) -> float:
#     """
#     Кастомное округление:
#     - дробная часть >= 0.5 → вверх
#     - дробная часть <= 0.4 → вниз
#     - иначе — оставляем как есть
#     """
#     if value is None:
#         return 0.0
#     value = float(value)
#     fraction = value - math.floor(value)
#     if fraction >= 0.5:
#         return math.ceil(value)
#     elif fraction <= 0.4:
#         return math.floor(value)
#     else:
#         return round(value, 2)

class PhotoUpdateSerializer(serializers.ModelSerializer):
    # явные поля, чтобы drf-yasg и DRF однозначно поняли тип
    counter_photo = serializers.ImageField(required=True)
    counter_current_check = serializers.IntegerField(required=True)

    class Meta:
        model = Check
        fields = ['id', 'counter_photo', 'counter_current_check']
        read_only_fields = ['id']

# class CheckVerificationUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Check
#         fields = ['counter_current_check']


#     def validate_counter_current_check(self, value):
#         if value is None:
#             raise serializers.ValidationError("Параметр counter_current_check обязателен.")
#         if value < 0:
#             raise serializers.ValidationError("Показание не может быть отрицательным.")
#         return value

#     def update(self, instance: Check, validated_data):
#         """
#         1) Атомарно обновляем показание и все расчёты;
#         2) Помечаем чек verified=True;
#         3) Асинхронно отправляем push пользователю.
#         """
#         counter = validated_data.get('counter_current_check')
#         if counter is None:
#             return instance

#         old_current_check_date = instance.current_check_date

#         with transaction.atomic():
#             prev = Decimal(instance.previous_check or 0)
#             curr = Decimal(int(counter))

#             if curr < prev:
#                 raise serializers.ValidationError(
#                     "Текущее показание меньше предыдущего. Проверьте данные или свяжитесь с поддержкой."
#                 )

#             consumption = curr - prev

#             # тариф может быть NULL
#             if instance.tariff is None:
#                 kw_cost = Decimal('0')
#                 nds_pct = Decimal('0')
#                 nsp_pct = Decimal('0')
#             else:
#                 kw_cost = Decimal(str(instance.tariff.kw_cost or 0))
#                 nds_pct = Decimal(str(instance.tariff.NDS or 0))
#                 nsp_pct = Decimal(str(instance.tariff.NSP or 0))

#             # Расчёты
#             pay_for_electricity = consumption * kw_cost
#             NDS_total = pay_for_electricity * nds_pct / Decimal('100')
#             NSP_total = pay_for_electricity * nsp_pct / Decimal('100')
#             amount_for_expenses = Decimal(str(instance.amount_for_expenses or 0))
#             total_sum = pay_for_electricity + NDS_total + NSP_total + amount_for_expenses

#             # Применяем кастомное округление
#             consumption_val = custom_round(consumption)
#             pay_val = custom_round(pay_for_electricity)
#             nds_val = custom_round(NDS_total)
#             nsp_val = custom_round(NSP_total)
#             exp_val = custom_round(amount_for_expenses)
#             total_val = custom_round(total_sum)

#             # Присваиваем поля модели
#             instance.counter_current_check = int(curr)
#             instance.current_check = int(curr)
#             instance.consumption = consumption_val
#             instance.pay_for_electricity = pay_val
#             instance.NDS_total = nds_val
#             instance.NSP_total = nsp_val
#             instance.amount_for_expenses = exp_val
#             instance.total_sum = total_val
#             instance.verified = True

#             # Подготовка к следующему периоду
#             instance.previous_check = int(curr)
#             instance.previous_check_date = old_current_check_date

#             instance.save()

#         # Push-уведомление пользователю
#         try:
#             title = "Чек подтверждён — требуется оплата"
#             body = (
#                 f"Чек подготовлен. Потребление: {consumption_val:.2f} kW. "
#                 f"К оплате: {total_val:.2f}."
#             )
#             data = {
#                 "check_id": instance.id,
#                 "total_sum": str(total_val),
#                 "consumption": str(consumption_val),
#             }
#             send_expo_push_notification.delay(instance.username_id, title, body, data)
#         except Exception:
#             logging.exception("Не удалось поставить в очередь задачу отправки push-уведомления.")

#         return instance




# serializers.py (часть)
from decimal import Decimal
import math
from django.db import transaction
import logging
from rest_framework import serializers

def custom_round(value: Decimal | float) -> float:
    if value is None:
        return 0.0
    value = float(value)
    fraction = value - math.floor(value)
    if fraction >= 0.5:
        return float(math.ceil(value))
    elif fraction <= 0.4:
        return float(math.floor(value))
    else:
        return round(value, 2)

class CheckVerificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ['counter_current_check']

    def validate_counter_current_check(self, value):
        if value is None:
            raise serializers.ValidationError("Параметр counter_current_check обязателен.")
        if value < 0:
            raise serializers.ValidationError("Показание не может быть отрицательным.")
        return value

    def update(self, instance: Check, validated_data):
        counter = validated_data.get('counter_current_check')
        if counter is None:
            return instance

        # old_current_check_date = instance.current_check_date
        previous_check_date = instance.previous_check_date

        with transaction.atomic():
            prev = Decimal(str(instance.previous_check or 0))
            curr = Decimal(str(int(counter)))

            if curr < prev:
                raise serializers.ValidationError(
                    "Текущее показание меньше предыдущего. Проверьте данные или свяжитесь с поддержкой."
                )

            consumption = curr - prev  # Decimal

            # --- получение тарифной логики ---
            if instance.tariff is None:
                energy_charge = Decimal('0')
                nds_pct = Decimal('0')
                nsp_pct = Decimal('0')
            else:
                nds_pct = Decimal(str(instance.tariff.NDS or 0))
                nsp_pct = Decimal(str(instance.tariff.NSP or 0))
                # ВАЖНО: единая точка расчёта
                energy_charge = instance.tariff.calculate_energy_charge(consumption)

            # остальные элементы
            amount_for_expenses = Decimal(str(instance.amount_for_expenses or 0))

            # НДС и НСП считаем от energy_charge (бизнес-правило: можно менять)
            NDS_total = (energy_charge * nds_pct / Decimal('100')).quantize(Decimal('0.01'))
            NSP_total = (energy_charge * nsp_pct / Decimal('100')).quantize(Decimal('0.01'))

            total_sum = (energy_charge + NDS_total + NSP_total + amount_for_expenses).quantize(Decimal('0.01'))

            # Применяем кастомное округление (ваша функция возвращает float)
            consumption_val = custom_round(consumption)
            pay_val = custom_round(energy_charge)
            nds_val = custom_round(NDS_total)
            nsp_val = custom_round(NSP_total)
            exp_val = custom_round(amount_for_expenses)
            total_val = custom_round(total_sum)

            # Сохраняем в instance
            instance.counter_current_check = int(curr)
            instance.current_check = int(curr)
            instance.consumption = consumption_val
            instance.pay_for_electricity = pay_val
            instance.NDS_total = nds_val
            instance.NSP_total = nsp_val
            instance.amount_for_expenses = exp_val
            instance.total_sum = total_val
            instance.verified = True

            # Подготовка к следующему периода
            instance.previous_check = int(prev)
            instance.previous_check_date = previous_check_date

            instance.save()

        # Push notification (как у вас было)
        try:
            title = "Чек подтверждён — требуется оплата"
            body = (
                f"Чек подготовлен. Потребление: {consumption_val:.2f} kW. "
                f"К оплате: {total_val:.2f}."
            )
            data = {
                "check_id": instance.id,
                "total_sum": str(total_val),
                "consumption": str(consumption_val),
            }
            send_expo_push_notification.delay(instance.username_id, title, body, data)
        except Exception:
            logging.exception("Не удалось поставить в очередь задачу отправки push-уведомления.")

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
