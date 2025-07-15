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
    apartment = models.PositiveIntegerField(null=True, blank=True)
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

class Tariff(models.Model):
    name = models.CharField(max_length=100)
    NDS = models.FloatField(default=0, null=True, blank=True)
    NSP = models.FloatField(default=0, null=True, blank=True)
    kw_cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    personal_account = models.PositiveIntegerField()
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
    contract_number = models.PositiveIntegerField()
    contract_date = models.DateField()
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

    tp_number = models.PositiveIntegerField()
    household_needs = models.FloatField(null=True, blank=True)
    fact_summer = models.FloatField(null=True, blank=True)
    fact_winter = models.FloatField(null=True, blank=True)
    max_summer = models.FloatField(null=True, blank=True)
    max_winter = models.FloatField(null=True, blank=True)


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