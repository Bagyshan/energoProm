# services/energoprom_client.py
from decimal import Decimal
from typing import List, Optional
import requests
from requests import Session
from config import settings
import json
import logging

logger = logging.getLogger(__name__)

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


    # def _login_if_needed(self):
    #     if self._token:
    #         return
    #     url = f"{self.base}/login"
    #     resp = self.session.post(url, data={'email': self.email, 'password': self.password}, timeout=self.timeout)
    #     resp.raise_for_status()
    #     j = resp.json()
    #     token = j.get('token')
    #     if not token:
    #         raise RuntimeError('No token returned from energoprom login')
    #     self._token = token
    #     self.session.headers.update({'Authorization': f'Bearer {token}'})

    def _login_if_needed(self):
        if self._token:
            return
        url = f"{self.base}/login"
        try:
            resp = self.session.post(
                url, 
                data={'email': self.email, 'password': self.password}, 
                timeout=self.timeout
            )
            resp.raise_for_status()
            
            # Безопасный парсинг JSON
            try:
                j = resp.json()
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON response from login: {resp.text}")
                raise RuntimeError(f'Invalid JSON response from login: {e}')
                
            token = j.get('token')
            if not token:
                raise RuntimeError('No token returned from energoprom login')
            self._token = token
            self.session.headers.update({'Authorization': f'Bearer {token}'})
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Login request failed: {e}")
            raise

    def _safe_json_response(self, response):
        """Безопасно парсит JSON ответ"""
        try:
            return response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {response.text}")
            logger.error(f"Response headers: {response.headers}")
            logger.error(f"Response status: {response.status_code}")
            raise RuntimeError(f'Invalid JSON response from API: {e}')

    def preview(self, account: str, total: Decimal) -> dict:
        self._login_if_needed()
        url = f"{self.base}/invoice/preview"
        try:
            resp = self.session.post(
                url, 
                data={'account': str(account), 'total': str(total)}, 
                timeout=self.timeout
            )
            resp.raise_for_status()
            return self._safe_json_response(resp)
        except requests.exceptions.RequestException as e:
            logger.error(f"Preview request failed for account {account}: {e}")
            raise

    def create_invoice(self, account: str, total: Decimal) -> dict:
        self._login_if_needed()
        url = f"{self.base}/invoice/create"
        try:
            resp = self.session.post(
                url, 
                data={'account': str(account), 'total': str(total)}, 
                timeout=self.timeout
            )
            resp.raise_for_status()
            return self._safe_json_response(resp)
        except requests.exceptions.RequestException as e:
            logger.error(f"Create invoice request failed for account {account}: {e}")
            raise

    def payment_history(self, account: str) -> List[dict]:
        self._login_if_needed()
        url = f"{self.base}/payment/history"
        try:
            resp = self.session.post(
                url, 
                data={'account': str(account)}, 
                timeout=self.timeout
            )
            resp.raise_for_status()
            return self._safe_json_response(resp)
        except requests.exceptions.RequestException as e:
            logger.error(f"Payment history request failed for account {account}: {e}")
            raise

    def get_pdf(self, requisite: str) -> bytes:
        self._login_if_needed()
        url = f"{self.base}/pdf/{requisite}"
        try:
            resp = self.session.post(url, timeout=self.timeout)
            resp.raise_for_status()
            
            # Проверяем, что это действительно PDF
            content_type = resp.headers.get('content-type', '')
            if 'application/pdf' not in content_type:
                logger.warning(f"Unexpected content type for PDF: {content_type}")
                
            return resp.content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"PDF download failed for requisite {requisite}: {e}")
            raise


client = EnergopromClient()