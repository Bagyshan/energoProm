# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Check
from .client import EnergopromClient
from django.dispatch import Signal

client = EnergopromClient()
order_completed = Signal()

@receiver(post_save, sender=Check)
def auto_create_invoice(sender, instance: Check, created, **kwargs):
    if not created:
        return
    if getattr(settings, 'AUTO_CREATE_INVOICE', False):
        amount = instance.total_sum or instance.pay_for_electricity or 0
        if amount:
            try:
                data = client.create_invoice(account=instance.house_card.house_card, total=str(amount))
                instance.payment_requisite = data.get('requisite')
                instance.payment_urls = data.get('urls')
                instance.payment_sum = data.get('sum')
                instance.save(update_fields=['payment_requisite', 'payment_urls', 'payment_sum'])
            except Exception as e:
                # логируем, но не ломаем сохранение чека
                import logging
                logging.getLogger('payments').exception("auto invoice create failed: %s", e)
