from typing import Optional
from datetime import datetime
from django.utils.crypto import constant_time_compare


def _parse_date_ddmmyyyy(text: Optional[str]):
    if not text:
        return None
    for fmt in ('%d.%m.%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(text, fmt).date()
        except Exception:
            continue
    return None