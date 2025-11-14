from django.db import models
from user.models import User

# Create your models here.


# Address models
class District(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GosAdministration(models.Model):
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='administrations'
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Settlement(models.Model):
    administration = models.ForeignKey(
        GosAdministration,
        on_delete=models.CASCADE,
        related_name='settlements'
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Street(models.Model):
    settlement = models.ForeignKey(
        Settlement,
        on_delete=models.CASCADE,
        related_name='streets'
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Address(models.Model):
    street = models.ForeignKey(
        Street,
        on_delete=models.CASCADE,
        related_name='addresses',
        blank=True
    )
    house = models.CharField(blank=True)
    liter = models.CharField(max_length=8, null=True, blank=True)
    apartment = models.CharField(max_length=8, null=True, blank=True)
    apartment_liter = models.CharField(max_length=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




# Counter models
class Executor(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CounterCause(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CounterType(models.Model):
    model = models.CharField(max_length=100)
    significance = models.PositiveSmallIntegerField()
    amperage_range = models.CharField(max_length=50)
    current_transformation_ratio = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Counter(models.Model):
    cause = models.ForeignKey(
        CounterCause,
        on_delete=models.SET_NULL,
        null=True,
        related_name='counters',
        blank=True
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='counters',
        blank=True
    )
    serial_number = models.CharField(max_length=50, blank=True)
    counter_type = models.ForeignKey(
        CounterType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='counters',
        blank=True
    )
    pp_number = models.PositiveIntegerField(blank=True, null=True)
    current_indication = models.PositiveIntegerField(default=0, blank=True)
    year_of_state_inspection = models.PositiveSmallIntegerField(blank=True)
    quarter_of_state_inspection = models.PositiveSmallIntegerField(blank=True)
    energy_sales_seal = models.CharField(max_length=50, null=True, blank=True)
    CRPU_seal = models.CharField(max_length=50, null=True, blank=True)
    seal_on_the_casing = models.CharField(max_length=50, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Tariff models

# class Tariff(models.Model):
#     name = models.CharField(max_length=100)
#     NDS = models.FloatField(default=0, null=True, blank=True)
#     NSP = models.FloatField(default=0, null=True, blank=True)
#     kw_cost = models.FloatField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError

class Tariff(models.Model):
    PRICING_FLAT = 'flat'
    PRICING_TIERED = 'tiered'
    PRICING_CHOICES = [
        (PRICING_FLAT, 'Flat'),
        (PRICING_TIERED, 'Tiered'),
    ]

    name = models.CharField(max_length=100)
    NDS = models.FloatField(default=0, null=True, blank=True)
    NSP = models.FloatField(default=0, null=True, blank=True)
    kw_cost = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0.0'))  # for flat pricing
    pricing_type = models.CharField(max_length=10, choices=PRICING_CHOICES, default=PRICING_FLAT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_energy_charge(self, consumption) -> Decimal:
        """
        Возвращает сумму (Decimal) к оплате за energy consumption (в kWh),
        учитывая тип тарифа (flat или tiered).
        """
        from decimal import Decimal, ROUND_HALF_UP
        if consumption is None:
            return Decimal('0')

        cons = Decimal(str(consumption))
        if cons <= 0:
            return Decimal('0')

        if self.pricing_type == self.PRICING_FLAT:
            return (cons * (self.kw_cost or Decimal('0'))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # TIERED
        bands = list(self.bands.order_by('min_kwh').all())
        total = Decimal('0')
        processed = Decimal('0')  # how many kWh already billed
        for band in bands:
            if cons <= processed:
                break

            band_min = Decimal(str(band.min_kwh))
            band_max = Decimal(str(band.max_kwh)) if band.max_kwh is not None else None
            # start point for this band: the greater of band_min and processed
            start = band_min if band_min > processed else processed

            # if consumption less or equal start -> nothing in this band
            if cons <= start:
                continue

            # compute available capacity in this band (upper bound - start)
            if band_max is not None:
                end = band_max
                band_capacity = end - start
                to_take = cons - start if cons < end else band_capacity
            else:
                # open-ended band (no max) — take all remaining consumption
                to_take = cons - start

            if to_take <= 0:
                continue

            price = Decimal(str(band.price_per_kwh))
            total += (to_take * price)
            processed = start + to_take

        # финальное округление до стотых
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class TariffBand(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='bands')
    # min_kwh inclusive
    min_kwh = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    # max_kwh exclusive (nullable = open ended)
    max_kwh = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    price_per_kwh = models.DecimalField(max_digits=12, decimal_places=4)

    order = models.PositiveSmallIntegerField(default=0)  # для удобства сортировки/админки

    class Meta:
        ordering = ['order', 'min_kwh']

    def clean(self):
        # базовая валидация
        if self.min_kwh is None:
            raise ValidationError("min_kwh is required")
        if self.min_kwh < 0:
            raise ValidationError("min_kwh must be >= 0")
        if self.max_kwh is not None:
            if self.max_kwh <= self.min_kwh:
                raise ValidationError("max_kwh must be greater than min_kwh")

    def __str__(self):
        return f"{self.tariff.name}: {self.min_kwh} - {self.max_kwh or '∞'} @ {self.price_per_kwh}"






# Plot models

class Plot(models.Model):
    code = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=50)
    controller = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # house_card_count

class Route(models.Model):
    route_number = models.PositiveIntegerField()
    plot = models.ForeignKey(
        Plot,
        on_delete=models.CASCADE,
        related_name='routes'
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='routes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # house_card_count




# House Card model

class HouseCard(models.Model):
    house_card = models.CharField(max_length=50, default=0, unique=True)
    old_house_card = models.CharField(max_length=50, default=0, null=True, blank=True, unique=False)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name='house_cards'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='house_cards'
    )
    contract_number = models.CharField(null=True, blank=True)
    contract_date = models.DateField(null=True, blank=True)
    plot = models.ForeignKey(
        Plot,
        on_delete=models.SET_NULL,
        null=True,
        related_name='house_cards'
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        null=True,
        related_name='house_cards'
    )

    counter = models.ForeignKey(
        Counter,
        on_delete=models.SET_NULL,
        null=True,
        related_name='house_cards'
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.SET_NULL,
        null=True,
        related_name='house_cards'
    )

    tp_number = models.PositiveIntegerField(null=True, blank=True)
    household_needs = models.FloatField(null=True, blank=True)
    fact_summer = models.FloatField(null=True, blank=True)
    fact_winter = models.FloatField(null=True, blank=True)
    max_summer = models.FloatField(null=True, blank=True)
    max_winter = models.FloatField(null=True, blank=True)

    overpayment_underpayment = models.FloatField(default=0)
    penalty = models.FloatField(default=0)


    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Counter
    # Tariff
    # Route

# {
#     "district": "район",
#     "gos_administration": "гос. администрация",
#     "settlement": "населенный пункт",
#     "street": "улица",
#     "liter": "литер",
#     "significance": "значность",
#     "amperage_range": "диапазон силы тока",
#     "current_transformation_ratio": "коэффициент трансформации тока",
#     "executor": "исполнитель",
#     "counter_cause": "причина",
#     "counter_type": "тип счетчика",
#     "counter": "счетчик",
#     "current_indication": "текущий показатель",
#     "year_of_state_inspection": "код гос. проверки",
#     "quarter_of_state_inspection": "квартал гос. проверки",
#     "energy_sales_seal": "промба энергосбыта",
#     "CRPU_seal": "пломба ЦРПУ",
#     "seal_on_the_casing": "пломба на кожухе",
#     "plot": "участок",
#     "route": "маршрут",
#     "personal_account": "лицевой счет",
#     "contract_number": "номер договора",
#     "contract_date": "дата заключения договора",
#     "household_needs": "хозяйственные нужды",
#     "fact_summer": "факт (лето)",
#     "fact_winter": "факт (зима)",
#     "max_summer": "макс (лето)",
#     "max_winter": "макс (зима)"
# }