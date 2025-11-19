# # services/energoprom_client.py
# from decimal import Decimal
# from typing import List, Optional
# import requests
# from requests import Session
# from config import settings
# import json
# import logging

# logger = logging.getLogger(__name__)

# class EnergopromClient:
#     def __init__(self):
#         self.base = getattr(settings, 'ENERGOPROM_BASE_URL')
#         self.api_key = getattr(settings, 'ENERGOPROM_API_KEY')
#         self.email = getattr(settings, 'ENERGOPROM_EMAIL')
#         self.password = getattr(settings, 'ENERGOPROM_PASSWORD')
#         self.timeout = getattr(settings, 'ENERGOPROM_REQUEST_TIMEOUT', 10)
#         self.session = requests.Session()
#         if self.api_key:
#             self.session.headers.update({'api-key': self.api_key})
#         self._token: Optional[str] = None


#     # def _login_if_needed(self):
#     #     if self._token:
#     #         return
#     #     url = f"{self.base}/login"
#     #     resp = self.session.post(url, data={'email': self.email, 'password': self.password}, timeout=self.timeout)
#     #     resp.raise_for_status()
#     #     j = resp.json()
#     #     token = j.get('token')
#     #     if not token:
#     #         raise RuntimeError('No token returned from energoprom login')
#     #     self._token = token
#     #     self.session.headers.update({'Authorization': f'Bearer {token}'})

#     def _login_if_needed(self):
#         if self._token:
#             return
#         url = f"{self.base}/login"
#         try:
#             resp = self.session.post(
#                 url, 
#                 data={'email': self.email, 'password': self.password}, 
#                 timeout=self.timeout
#             )
#             resp.raise_for_status()
            
#             # Безопасный парсинг JSON
#             try:
#                 j = resp.json()
#             except json.JSONDecodeError as e:
#                 logger.error(f"Invalid JSON response from login: {resp.text}")
#                 raise RuntimeError(f'Invalid JSON response from login: {e}')
                
#             token = j.get('token')
#             if not token:
#                 raise RuntimeError('No token returned from energoprom login')
#             self._token = token
#             self.session.headers.update({'Authorization': f'Bearer {token}'})
            
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Login request failed: {e}")
#             raise

#     def _safe_json_response(self, response):
#         """Безопасно парсит JSON ответ"""
#         try:
#             return response.json()
#         except json.JSONDecodeError as e:
#             logger.error(f"Invalid JSON response: {response.text}")
#             logger.error(f"Response headers: {response.headers}")
#             logger.error(f"Response status: {response.status_code}")
#             raise RuntimeError(f'Invalid JSON response from API: {e}')

#     def preview(self, account: str, total: Decimal) -> dict:
#         self._login_if_needed()
#         url = f"{self.base}/invoice/preview"
#         try:
#             resp = self.session.post(
#                 url, 
#                 data={'account': str(account), 'total': str(total)}, 
#                 timeout=self.timeout
#             )
#             resp.raise_for_status()
#             return self._safe_json_response(resp)
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Preview request failed for account {account}: {e}")
#             raise

#     def create_invoice(self, account: str, total: Decimal) -> dict:
#         self._login_if_needed()
#         url = f"{self.base}/invoice/create"
#         try:
#             resp = self.session.post(
#                 url, 
#                 data={'account': str(account), 'total': str(total)}, 
#                 timeout=self.timeout
#             )
#             resp.raise_for_status()
#             return self._safe_json_response(resp)
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Create invoice request failed for account {account}: {e}")
#             raise

#     def payment_history(self, account: str) -> List[dict]:
#         self._login_if_needed()
#         url = f"{self.base}/payment/history"
#         try:
#             resp = self.session.post(
#                 url, 
#                 data={'account': str(account)}, 
#                 timeout=self.timeout
#             )
#             resp.raise_for_status()
#             return self._safe_json_response(resp)
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Payment history request failed for account {account}: {e}")
#             raise

#     def get_pdf(self, requisite: str) -> bytes:
#         self._login_if_needed()
#         url = f"{self.base}/pdf/{requisite}"
#         try:
#             resp = self.session.post(url, timeout=self.timeout)
#             resp.raise_for_status()
            
#             # Проверяем, что это действительно PDF
#             content_type = resp.headers.get('content-type', '')
#             if 'application/pdf' not in content_type:
#                 logger.warning(f"Unexpected content type for PDF: {content_type}")
                
#             return resp.content
            
#         except requests.exceptions.RequestException as e:
#             logger.error(f"PDF download failed for requisite {requisite}: {e}")
#             raise


# client = EnergopromClient()







# services/energoprom_client.py
from decimal import Decimal
from typing import List, Optional, Dict, Any
import requests
import json
import logging
import time
from datetime import datetime, timedelta
from config import settings
import jwt  # pip install PyJWT

logger = logging.getLogger(__name__)

class EnergopromClient:
    def __init__(self):
        self.base = getattr(settings, 'ENERGOPROM_BASE_URL')
        self.api_key = getattr(settings, 'ENERGOPROM_API_KEY')
        self.email = getattr(settings, 'ENERGOPROM_EMAIL')
        self.password = getattr(settings, 'ENERGOPROM_PASSWORD')
        self.timeout = getattr(settings, 'ENERGOPROM_REQUEST_TIMEOUT', 10)
        
        self.session = requests.Session()
        self._token: Optional[str] = None
        self._token_expires: Optional[datetime] = None
        
        # Базовые заголовки
        if self.api_key:
            self.session.headers.update({'api-key': self.api_key})
        
        self.session.headers.update({
            'User-Agent': 'EnergopromClient/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })

    def _is_token_valid(self) -> bool:
        """Проверяет, действителен ли текущий токен"""
        if not self._token or not self._token_expires:
            return False
        
        # Добавляем запас в 2 минуты до истечения срока
        return datetime.now() < (self._token_expires - timedelta(minutes=2))

    def _parse_token_expiry(self, token: str) -> Optional[datetime]:
        """Парсит JWT токен для получения времени истечения"""
        try:
            # Декодируем без проверки подписи, только чтобы получить expiry
            payload = jwt.decode(token, options={"verify_signature": False})
            if 'exp' in payload:
                return datetime.fromtimestamp(payload['exp'])
            else:
                # Если нет exp, устанавливаем дефолтное время (1 час)
                logger.warning("JWT token doesn't have 'exp' claim, using default 1 hour expiry")
                return datetime.now() + timedelta(hours=1)
        except jwt.InvalidTokenError as e:
            logger.warning(f"Could not parse token expiry: {e}")
            # Если не смогли распарсить, устанавливаем дефолтное время (1 час)
            return datetime.now() + timedelta(hours=1)

    def _perform_login(self) -> None:
        """Выполняет логин и получает новый токен"""
        url = f"{self.base}/login"
        
        login_data = {
            'email': self.email,
            'password': self.password
        }
        
        try:
            logger.info(f"Performing login to {url}")
            
            # Временно убираем старый токен для запроса логина
            original_headers = self.session.headers.copy()
            if 'Authorization' in self.session.headers:
                del self.session.headers['Authorization']
            
            resp = self.session.post(
                url, 
                json=login_data,
                timeout=self.timeout
            )
            
            # Восстанавливаем заголовки
            self.session.headers.update(original_headers)
            
            # Проверяем статус
            if resp.status_code == 401:
                raise RuntimeError('Invalid credentials for energoprom login')
            elif resp.status_code == 403:
                raise RuntimeError('Access forbidden for energoprom login')
            elif resp.status_code != 200:
                raise RuntimeError(f'Login failed with status {resp.status_code}: {resp.text}')
            
            # Безопасный парсинг JSON
            try:
                response_data = resp.json()
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON response from login: {resp.text}")
                raise RuntimeError(f'Invalid JSON response from login: {e}')
            
            # Извлекаем токен из ответа (согласно вашему формату)
            token = response_data.get('token')
            
            if not token:
                logger.error(f"No token in response: {response_data}")
                raise RuntimeError('No token returned from energoprom login')
            
            # Сохраняем токен
            self._token = token
            self._token_expires = self._parse_token_expiry(token)
            
            # Обновляем заголовки сессии
            self.session.headers.update({'Authorization': f'Bearer {token}'})
            
            logger.info(f"Successfully logged in, token expires at {self._token_expires}")
            
        except requests.exceptions.Timeout:
            logger.error("Login request timed out")
            raise RuntimeError('Login request timed out')
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to energoprom API")
            raise RuntimeError('Cannot connect to energoprom API')
        except requests.exceptions.RequestException as e:
            logger.error(f"Login request failed: {e}")
            raise RuntimeError(f'Login request failed: {e}')

    def _ensure_auth(self) -> None:
        """Гарантирует, что у нас есть действительный токен"""
        if not self._is_token_valid():
            logger.info("Token expired or invalid, performing login")
            self._perform_login()
        else:
            logger.debug("Token is still valid")

    def _safe_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Выполняет запрос с автоматической аутентификацией и retry логикой"""
        max_retries = 2
        
        for attempt in range(max_retries + 1):
            try:
                # Перед каждым запросом проверяем аутентификацию
                self._ensure_auth()
                
                # Выполняем запрос
                response = self.session.request(method, url, **kwargs)
                
                # Если получили 401 - токен недействителен, сбрасываем и пробуем снова
                if response.status_code == 401 and attempt < max_retries:
                    logger.warning(f"Received 401, token invalid. Retrying (attempt {attempt + 1}/{max_retries})")
                    self._token = None
                    self._token_expires = None
                    continue
                
                return response
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed on attempt {attempt + 1}: {e}")
                if attempt == max_retries:
                    raise
        
        raise RuntimeError(f"Request failed after {max_retries} retries")

    def _safe_json_response(self, response: requests.Response) -> Dict[str, Any]:
        """Безопасно парсит JSON ответ"""
        # Сначала проверяем статус
        if response.status_code != 200:
            raise RuntimeError(f'API returned status {response.status_code}: {response.text}')
        
        try:
            return response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response. Status: {response.status_code}")
            logger.error(f"Response text: {response.text[:500]}...")
            logger.error(f"Response headers: {dict(response.headers)}")
            
            # Если получили HTML вместо JSON - это может быть страница логина
            if response.text.strip().startswith('<!DOCTYPE html') or '<html' in response.text.lower():
                raise RuntimeError('Received HTML response instead of JSON - possible authentication issue')
            
            raise RuntimeError(f'Invalid JSON response from API: {e}')

    def preview(self, account: str, total: Decimal) -> dict:
        """Предварительный просмотр инвойса"""
        url = f"{self.base}/invoice/preview"
        
        data = {
            'account': str(account),
            'total': float(total)  # Конвертируем Decimal в float для JSON
        }
        
        try:
            logger.info(f"Making preview request for account {account}, total {total}")
            response = self._safe_request('POST', url, json=data, timeout=self.timeout)
            return self._safe_json_response(response)
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Preview HTTP error for account {account}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Preview request failed for account {account}: {e}")
            raise

    def create_invoice(self, account: str, total: Decimal) -> dict:
        """Создание инвойса"""
        url = f"{self.base}/invoice/create"
        
        data = {
            'account': str(account),
            'total': float(total)  # Конвертируем Decimal в float для JSON
        }
        
        try:
            logger.info(f"Making create_invoice request for account {account}, total {total}")
            response = self._safe_request('POST', url, json=data, timeout=self.timeout)
            return self._safe_json_response(response)
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Create invoice HTTP error for account {account}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Create invoice request failed for account {account}: {e}")
            raise

    def payment_history(self, account: str) -> List[dict]:
        """История платежей"""
        url = f"{self.base}/payment/history"
        
        data = {
            'account': str(account)
        }
        
        try:
            logger.info(f"Making payment_history request for account {account}")
            response = self._safe_request('POST', url, json=data, timeout=self.timeout)
            result = self._safe_json_response(response)
            
            # Гарантируем, что возвращаем список
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and 'payments' in result:
                return result['payments']
            else:
                logger.warning(f"Unexpected payment history response format: {result}")
                return []
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Payment history HTTP error for account {account}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Payment history request failed for account {account}: {e}")
            raise

    def get_pdf(self, requisite: str) -> bytes:
        """Получение PDF"""
        url = f"{self.base}/pdf/{requisite}"
        
        try:
            logger.info(f"Making get_pdf request for requisite {requisite}")
            response = self._safe_request('GET', url, timeout=self.timeout)
            
            # Проверяем статус
            if response.status_code != 200:
                raise RuntimeError(f'PDF request failed with status {response.status_code}')
            
            # Проверяем, что это действительно PDF
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' not in content_type:
                logger.warning(f"Unexpected content type for PDF: {content_type}")
                # Но все равно возвращаем контент, так как это может быть правильный PDF
                
            return response.content
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"PDF download HTTP error for requisite {requisite}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"PDF download failed for requisite {requisite}: {e}")
            raise

    def get_token_info(self) -> Dict[str, Any]:
        """Возвращает информацию о текущем токене (для отладки)"""
        return {
            'has_token': bool(self._token),
            'token_expires': self._token_expires.isoformat() if self._token_expires else None,
            'is_token_valid': self._is_token_valid(),
            'time_until_expiry': str(self._token_expires - datetime.now()) if self._token_expires else None,
        }

    def test_connection(self) -> bool:
        """Тестирует подключение к API"""
        try:
            # Простой запрос для проверки аутентификации
            self._ensure_auth()
            logger.info("Connection test successful")
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False


# Глобальный инстанс клиента
client = EnergopromClient()