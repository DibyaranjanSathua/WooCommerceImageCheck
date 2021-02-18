"""
File:           woocommerce_api.py
Author:         Dibyaranjan Sathua
Created on:     18/02/21, 10:09 pm
"""
import os
from woocommerce import API


class WooCommerceAPI:
    """ WooCommerce API """
    BASE_URL = "https://catercentral.com.au"

    def __init__(self, username: str, password: str):
        self._username: str = username
        self._password: str = password
        timeout = os.environ.get("API_TIMEOUT") or 600
        self._wcapi = API(
            url=WooCommerceAPI.BASE_URL,
            consumer_key=username,
            consumer_secret=password,
            version="wc/v3",
            timeout=timeout
        )
        print(f"API timeout set to {timeout}")

    def get_all_products(self, page: int = 1):
        """ Get a list of all products """
        success = False
        endpoint = "products"
        params = {"per_page": 2, "page": page}
        response = self._wcapi.get(endpoint=endpoint, params=params)
        if response.status_code == 200:
            success = True
        return response.json(), success


if __name__ == "__main__":
    from config import config
    obj = WooCommerceAPI(
        username=config.WooCommerceAPICred.USERNAME,
        password=config.WooCommerceAPICred.PASSWORD
    )
    result, success = obj.get_all_products()
    print(result)
