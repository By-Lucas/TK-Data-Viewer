import sys
import time
import json
import base64
import typing
import requests
from loguru import logger
from decouple import config


logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)


class ConnectionApi:
    
    def __init__(self) -> None:
        self._base_url = config('BASE_URL')
        self._base_url_token = config('BASE_URL_TOKEN')
        self.client_id = config('CLIENT_ID')
        self.client_secret = config('CLIENT_SECRET')
        
        
    def _make_request(self, method: str, endpoints: str, data: typing.Dict) -> None:
        self._headers = {
            'authorization': f'Bearer {self.get_token()}',
            'Content-Type': 'application/json'
        }
        if method:
            try:
                response = requests.request(method.upper(), self._base_url_token + endpoints, params=data, headers=self._headers)
            except Exception as e:
                logger.error(f'Erro de conexão ao fazer {method} request para {endpoints}: {e}')
                raise Exception(f'Erro de conexão ao fazer {method} request para {endpoints}: {e}')
        else:
            ValueError()
        
        if response.status_code >= 200 and response.status_code <= 204:
            return response
        else:
            logger.error(f"Erro ao fazer {method} pedido para {endpoints}: {response.json()} (Erro de codigo {response.status_code})")
            raise Exception(f"Erro ao fazer {method} pedido para {endpoints}: {response.json()} (Erro de codigo {response.status_code})")

    def get_token(self):
        # Verifica se o token atual ainda é válido
        if hasattr(self, 'token_expires_at') and time.time() < self.token_expires_at:
            print('usando token existente')
            return self.access_token
        
        print('Criando novo token')
        # Cria um novo token
        auth = base64.b64encode((f"{self.client_id}:{self.client_secret}").encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {"grant_type": "client_credentials"}
        response = requests.request("POST", f'{self._base_url}/auth/oauth/v2/token-jwt', headers=headers, data=payload)
        # Armazena o token e a data de expiração
        token_data = json.loads(response.content)
        self.access_token = token_data['access_token']
        self.token_expires_at = time.time() + token_data['expires_in']
        return self.access_token
