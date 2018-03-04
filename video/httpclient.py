import time
import random
from typing import Optional, Union

import requests
from requests.exceptions import RequestException

SMART_PHONE_USER_AGENT = (
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) '
    'AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1'
)


def get(url: str, params: Optional[dict] = None, is_sp: bool = False, retry: int = 3, **kwargs) -> requests.Response:
    """Sends a GET request.
    """
    kwargs.setdefault('timeout', 5)
    headers = kwargs.get('headers') or {}  # type: dict
    headers.setdefault('Pragma', 'no-cache')
    headers.setdefault('Cache-Control', 'no-cache')
    if is_sp:
        headers.setdefault('User-Agent', SMART_PHONE_USER_AGENT)
    kwargs['headers'] = headers
    try:
        return requests.get(url, params=params, **kwargs)
    except RequestException:
        if retry > 0:
            time.sleep(1 + random.random() * 2)
            return get(url, params=params, retry=retry - 1, **kwargs)
        raise


def post(url: str, data: Union[None, dict, bytes, str] = None, json: Optional[dict] = None,
         is_sp: bool = False, retry: int = 3, **kwargs) -> requests.Response:
    """Sends a POST request.
    """
    kwargs.setdefault('timeout', 5)
    headers = kwargs.get('headers') or {}  # type: dict
    headers.setdefault('Pragma', 'no-cache')
    headers.setdefault('Cache-Control', 'no-cache')
    if is_sp:
        headers.setdefault('User-Agent', SMART_PHONE_USER_AGENT)
    kwargs['headers'] = headers
    try:
        return requests.post(url, data=data, json=json, **kwargs)
    except RequestException:
        if retry > 0:
            time.sleep(1 + random.random() * 2)
            return post(url, data=data, json=json, retry=retry - 1, **kwargs)
        raise


def head(url, is_sp: bool = False, **kwargs) -> requests.Response:
    """Sends a HEAD request.
    """
    kwargs.setdefault('timeout', 5)
    headers = kwargs.get('headers') or {}  # type: dict
    headers.setdefault('Pragma', 'no-cache')
    headers.setdefault('Cache-Control', 'no-cache')
    if is_sp:
        headers.setdefault('User-Agent', SMART_PHONE_USER_AGENT)
    kwargs['headers'] = headers
    return requests.head(url, **kwargs)
