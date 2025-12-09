import requests
from typing import TypeVar

from Endpoint import Endpoint

T = TypeVar('T')
def request(endpoint: Endpoint, params) -> T:
    try:
        response = requests.request(
            method=endpoint.method,
            url=endpoint.url,
            params=params,
            timeout=30
        )
        response.raise_for_status()
    except requests.HTTPError as http_error:
        print(f"HTTP error occured: {http_error}")
        raise
    except Exception as error:
        print(f"Other error occured: {error}")
        raise
    else:
        response.encoding = "utf-8"
        return response.json()
        