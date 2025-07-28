from celery import shared_task
from django.utils import timezone
from calendar import monthrange
from .models import Check, HouseCard
from config.celery import app
from notification.tasks import send_expo_push_notification

def get_days_in_month(dt):
    return monthrange(dt.year, dt.month)[1]

import logging
from django.db import transaction

logger = logging.getLogger(__name__)

# @shared_task(bind=True, max_retries=3)
@app.task(bind=True, max_retries=3)
def create_monthly_checks(self):
    today = timezone.localdate()
    if today.day <= 25 and today.day >= 28:
        return 'Not the 25th day of the month'
    

    current_month = today.replace(day=1)

    success, skipped, failed = 0, 0, 0

    for house_card in HouseCard.objects.select_related('user', 'tariff').all():
        try:
            check_exists = Check.objects.filter(
                house_card=house_card,
                created_at__date__gte=current_month
            ).exists()

            if check_exists:
                skipped += 1
                continue

            with transaction.atomic():
                last_check = Check.objects.filter(house_card=house_card).order_by('-created_at').first()

                Check.objects.create(
                    house_card=house_card,
                    username=house_card.user,
                    tariff=house_card.tariff,
                    previous_check=last_check.current_check if last_check else house_card.counter.current_indication,
                    previous_check_date=last_check.current_check_date if last_check else today,
                    period_day_count=get_days_in_month(today)
                )
                success += 1


                send_expo_push_notification.delay(
                    user_id=house_card.user.pk,
                    title="Новый счет за электричество",
                    body=f"Добавлен новый ежемесячный счет на электричество за {today.strftime('%B %Y')}",
                    data={"type": "check_created", "house_card_id": house_card.pk}
                )
        except Exception as e:
            logger.error(f"Failed to create check for HouseCard ID {house_card.pk}: {e}")
            failed += 1
            continue

    return f'Checks created: {success}, Skipped (already exists): {skipped}, Failed: {failed}'