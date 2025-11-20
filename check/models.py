from django.db import models
from house_card.models import HouseCard
from user.models import User
from house_card.models import Tariff
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Check(models.Model):
    house_card = models.ForeignKey(
        HouseCard,
        on_delete=models.CASCADE,
        related_name='checks',
        default=0,
        verbose_name=_("Лицевой счет")
    )
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='checks',
        verbose_name=_("Пользователь")
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.SET_NULL,
        related_name='checks',
        null=True,
        verbose_name=_("Тариф")
    )
    consumption = models.DecimalField(_("Потребление"), max_digits=10, decimal_places=2, null=True, blank=True)
    amount_for_expenses = models.DecimalField(_("Сумма за потребление"), max_digits=10, decimal_places=2, null=True, blank=True)
    previous_check = models.PositiveIntegerField(_("Предыдущие показания"), default=0)
    previous_check_date = models.DateField(_("Дата предыдущих показаний"), default='2025-01-01')
    current_check = models.PositiveIntegerField(_("Текущие показания"), null=True, blank=True)
    current_check_date = models.DateField(_("Дата текущих показаний"), auto_now=True, null=True, blank=True)
    period_day_count = models.PositiveSmallIntegerField(_("Количество дней в периоде"), default=0)
    NDS_total = models.DecimalField(_("Сумма НДС"), max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    NSP_total = models.DecimalField(_("Сумма НсП"), max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    pay_for_electricity = models.DecimalField(_("Оплата за электроэнергию"), max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    total_sum = models.DecimalField(_("Общая сумма"), max_digits=10, decimal_places=2, null=True, blank=True)

    counter_photo = models.ImageField(_("Фото счетчика"), upload_to='counter_photo/', null=True, blank=True)
    counter_current_check = models.PositiveIntegerField(_("Текущие показания счетчика"), null=True, blank=True)
    verified = models.BooleanField(_("Проверено"), default=False, blank=True)

    paid = models.BooleanField(_("Оплачено"), default=False, blank=True)
    paid_at = models.DateTimeField(_("Дата оплаты"), null=True, blank=True)

    payment_requisite = models.CharField(_("Платежные реквизиты"), max_length=64, null=True, blank=True, db_index=True)
    payment_urls = models.JSONField(_("Ссылки на платежи"), null=True, blank=True)
    payment_sum = models.DecimalField(_("Сумма платежа"), max_digits=12, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)



class PaymentTransaction(models.Model):
    check_fk = models.ForeignKey(Check, on_delete=models.CASCADE, related_name='payments')
    requisite = models.CharField(max_length=64)
    txn_id = models.CharField(max_length=128, null=True, blank=True)
    source = models.CharField(max_length=128, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['requisite']),
            models.Index(fields=['txn_id']),
        ]

    def __str__(self):
        return f"PaymentTransaction(check={self.check_fk}, txn={self.txn_id}, amount={self.amount})"
