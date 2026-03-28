from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

# Create your models here.
class Bid(models.Model):
    name = models.CharField(_("Название"), max_length=250)
    description = models.TextField(_("Описание"))
    icon = models.ImageField(_("Иконка"), upload_to='bid_icon/')

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Заявка')
        verbose_name_plural = _('Заявки')

class Deal(models.Model):
    DEAL_STATUS_CHOICES = {
        'new': 'новая',
        'in progress': 'в процессе',
        'completed': 'выполнена',
        'cancelled': 'отменена'
    }

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='deals',
        verbose_name=_("Пользователь")
    )
    bid = models.ForeignKey(
        Bid,
        on_delete=models.SET_NULL,
        related_name='deals',
        null=True,
        verbose_name=_("Заявка")
    )
    date_of_deal = models.DateField(_("Дата сделки"))
    address = models.TextField(_("Адрес"))
    status = models.CharField(_("Статус"), choices=DEAL_STATUS_CHOICES)
    phone_number = models.CharField(_("Номер телефона"), max_length=13)
    description = models.TextField(_("Описание"))

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        verbose_name = _('Сделка')
        verbose_name_plural = _('Сделки')