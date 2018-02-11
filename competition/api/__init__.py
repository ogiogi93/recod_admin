
import requests
from django.utils.lru_cache import lru_cache
from requests_oauthlib import OAuth2Session

from recod_admin.settings import STATIC_SETTINGS


TOORNAMENT_API_ACCESS_TOKEN_URL = 'https://api.toornament.com/oauth/v2/token'


@lru_cache(maxsize=1)
def get_toornament_access_token():
    """
    Toornament APIのアクセストークンを取得する
    :rtype str:
    """
    query = {
        'grant_type': 'client_credentials',
        'client_id': STATIC_SETTINGS['TOORNAMENT_CLIENT_ID'],
        'client_secret': STATIC_SETTINGS['TOORNAMENT_SECRET_ID']
    }
    response = requests.post(url=TOORNAMENT_API_ACCESS_TOKEN_URL, data=query).json()
    return response['access_token']


@lru_cache(maxsize=1024)
def authorized_session():
    """
    Oauth2認証済のセッションか作成する
    :rtype OAuth2Session:
    """
    oauth = OAuth2Session()
    oauth.headers['X-Api-Key'] = STATIC_SETTINGS['TOORNAMENT_API_KEY']
    oauth.headers['Authorization'] = get_toornament_access_token()
    return oauth


