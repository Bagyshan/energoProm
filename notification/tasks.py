from celery import shared_task
from exponent_server_sdk import PushClient, PushMessage, PushServerError
from requests.exceptions import RequestException
from .models import ExpoPushToken
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

    for token_obj in tokens:
        if not token_obj.token.startswith('ExponentPushToken'):
            continue

        message = PushMessage(
            to=token_obj.token,
            title=title,
            body=body,
            sound="default",
            data=data or {}
        )
        messages.append(message)

    try:
        tickets = client.publish_multiple(messages)
        for ticket, token_obj in zip(tickets, tokens):
            if ticket.get('status') == 'error':
                error = ticket.get('details', {}).get('error')
                logger.error(f"Expo error: {error} for token {token_obj.token}")
                if error == 'DeviceNotRegistered':
                    token_obj.delete()
    except PushServerError as exc:
        logger.exception(f"PushServerError while sending to user {user_id}: {exc.errors}")
    except RequestException as exc:
        logger.exception(f"RequestException while sending to user {user_id}: {str(exc)}")
    except Exception as exc:
        logger.exception(f"Unhandled error while sending to user {user_id}: {str(exc)}")

