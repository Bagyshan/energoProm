from django.db import models
from house_card.models import HouseCard
from user.models import User
from house_card.models import Tariff

# Create your models here.
class Check(models.Model):
    house_card = models.ForeignKey(
        HouseCard,
        on_delete=models.CASCADE,
        related_name='checks',
        default=0
    )
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='checks'
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.SET_NULL,
        related_name='checks',
        null=True
    )
    consumption = models.FloatField(null=True, blank=True)
    amount_for_expenses = models.FloatField(null=True, blank=True)
    previous_check = models.PositiveIntegerField(default=0)
    previous_check_date = models.DateField(default='2025-01-01')
    current_check = models.PositiveIntegerField(null=True, blank=True)
    current_check_date = models.DateField(auto_now=True, null=True, blank=True)
    period_day_count = models.PositiveSmallIntegerField(default=0)
    NDS_total = models.FloatField(default=0, null=True, blank=True)
    NSP_total = models.FloatField(default=0, null=True, blank=True)
    pay_for_electricity = models.FloatField(default=0, null=True, blank=True)
    total_sum = models.FloatField(null=True, blank=True)
    
    counter_photo = models.ImageField(upload_to='counter_photo/', null=True)
    counter_current_check = models.PositiveIntegerField(null=True)
    verified = models.BooleanField(default=False, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)