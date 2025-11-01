# services/energoprom_client.py
from decimal import Decimal
from typing import List, Optional
import requests
from requests import Session
from config import settings

class EnergopromClient:
    def __init__(self):
        self.base = getattr(settings, 'ENERGOPROM_BASE_URL')
        self.api_key = getattr(settings, 'ENERGOPROM_API_KEY')
        self.email = getattr(settings, 'ENERGOPROM_EMAIL')
        self.password = getattr(settings, 'ENERGOPROM_PASSWORD')
        self.timeout = getattr(settings, 'ENERGOPROM_REQUEST_TIMEOUT', 10)
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({'api-key': self.api_key})
        self._token: Optional[str] = None


    def _login_if_needed(self):
        if self._token:
            return
        url = f"{self.base}/login"
        resp = self.session.post(url, data={'email': self.email, 'password': self.password}, timeout=self.timeout)
        resp.raise_for_status()
        j = resp.json()
        token = j.get('token')
        if not token:
            raise RuntimeError('No token returned from energoprom login')
        self._token = token
        self.session.headers.update({'Authorization': f'Bearer {token}'})


    def preview(self, account: str, total: Decimal) -> dict:
        self._login_if_needed()
        url = f"{self.base}/invoice/preview"
        resp = self.session.post(url, data={'account': str(account), 'total': str(total)}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()


    def create_invoice(self, account: str, total: Decimal) -> dict:
        self._login_if_needed()
        url = f"{self.base}/invoice/create"
        resp = self.session.post(url, data={'account': str(account), 'total': str(total)}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()


    def payment_history(self, account: str) -> List[dict]:
        self._login_if_needed()
        url = f"{self.base}/payment/history"
        resp = self.session.post(url, data={'account': str(account)}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()


    def get_pdf(self, requisite: str) -> bytes:
        self._login_if_needed()
        url = f"{self.base}/pdf/{requisite}"
        resp = self.session.post(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.content