# from celery import shared_task
# from exponent_server_sdk import PushClient, PushMessage, PushServerError
# from requests.exceptions import RequestException
# from .models import ExpoPushToken
# import logging

# logger = logging.getLogger(__name__)

# @shared_task
# def send_expo_push_notification(user_id, title, body, data=None):
#     tokens = ExpoPushToken.objects.filter(user_id=user_id)

#     if not tokens.exists():
#         logger.warning(f"No Expo tokens for user {user_id}")
#         return

#     client = PushClient()
#     messages = []

#     for token_obj in tokens:
#         if not token_obj.token.startswith('ExponentPushToken'):
#             continue

#         message = PushMessage(
#             to=token_obj.token,
#             title=title,
#             body=body,
#             sound="default",
#             data=data or {}
#         )
#         messages.append(message)

#     try:
#         tickets = client.publish_multiple(messages)
#         for ticket, token_obj in zip(tickets, tokens):
#             if ticket.get('status') == 'error':
#                 error = ticket.get('details', {}).get('error')
#                 logger.error(f"Expo error: {error} for token {token_obj.token}")
#                 if error == 'DeviceNotRegistered':
#                     token_obj.delete()
#     except PushServerError as exc:
#         logger.exception(f"PushServerError while sending to user {user_id}: {exc.errors}")
#     except RequestException as exc:
#         logger.exception(f"RequestException while sending to user {user_id}: {str(exc)}")
#     except Exception as exc:
#         logger.exception(f"Unhandled error while sending to user {user_id}: {str(exc)}")

from celery import shared_task
from exponent_server_sdk import (
    PushClient, PushMessage, PushServerError,
    PushResponseError, DeviceNotRegisteredError
)
from requests.exceptions import RequestException
from .models import ExpoPushToken, PushNotificationLog
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_expo_push_notification(user_id, title, body, data=None):
    tokens = ExpoPushToken.objects.filter(user_id=user_id)

    if not tokens.exists():
        logger.warning(f"No Expo tokens for user {user_id}")
        return

    client = PushClient()
    messages = []
    logs = []

    logger.info(f"Preparing push messages for user {user_id}")

    for token_obj in tokens:
        if not token_obj.token.startswith('ExponentPushToken'):
            logger.warning(f"Skipping invalid token: {token_obj.token}")
            continue

        message = PushMessage(
            to=token_obj.token,
            title=title,
            body=body,
            sound="default",
            data=data or {}
        )
        messages.append((message, token_obj))

        # создаём лог "pending"
        logs.append(PushNotificationLog(
            user=token_obj.user,
            token=token_obj.token,
            title=title,
            body=body,
            data=data,
            status="pending"
        ))

    PushNotificationLog.objects.bulk_create(logs)

    try:
        logger.info(f"Sending {len(messages)} push notifications to Expo for user {user_id}")
        tickets = client.publish_multiple([m for m, _ in messages])

        for ticket, (msg, token_obj) in zip(tickets, messages):
            log = PushNotificationLog.objects.filter(
                user=token_obj.user, token=token_obj.token, status="pending"
            ).order_by('-created_at').first()

            if ticket.get('status') == 'ok':
                logger.info(f"Push sent successfully to {token_obj.token}, ticket_id={ticket['id']}")
                if log:
                    log.ticket_id = ticket.get('id')
                    log.status = "sent"
                    log.save()
            else:
                error = ticket.get('details', {}).get('error')
                logger.error(f"Expo error: {error} for token {token_obj.token}")
                if error == 'DeviceNotRegistered':
                    token_obj.delete()
                    logger.warning(f"Deleted invalid token {token_obj.token}")
                if log:
                    log.status = "error"
                    log.error_message = error
                    log.save()

    except PushServerError as exc:
        logger.exception(f"PushServerError while sending to user {user_id}: {exc.errors}")
    except RequestException as exc:
        logger.exception(f"RequestException while sending to user {user_id}: {str(exc)}")
    except Exception as exc:
        logger.exception(f"Unhandled error while sending to user {user_id}: {str(exc)}")


@shared_task
def check_expo_receipts():
    client = PushClient()
    logs = PushNotificationLog.objects.filter(status="sent", ticket_id__isnull=False)

    ticket_ids = [log.ticket_id for log in logs]
    if not ticket_ids:
        return

    logger.info(f"Checking receipts for {len(ticket_ids)} tickets")

    try:
        receipts = client.get_receipts(ticket_ids)

        for ticket_id, receipt in receipts.items():
            log = PushNotificationLog.objects.filter(ticket_id=ticket_id).first()
            if not log:
                continue

            if receipt["status"] == "ok":
                log.status = "delivered"
                log.save()
                logger.info(f"Push delivered successfully for ticket {ticket_id}")
            else:
                log.status = "error"
                log.error_message = receipt.get("message")
                log.save()
                logger.error(f"Push delivery failed for ticket {ticket_id}: {receipt}")
    except Exception as exc:
        logger.exception(f"Error while checking receipts: {str(exc)}")
