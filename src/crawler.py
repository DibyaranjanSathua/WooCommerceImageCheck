"""
File:           crawl.py
Author:         Dibyaranjan Sathua
Created on:     18/02/21, 10:28 pm
"""
from typing import Optional
import time
import requests
from src.woocommerce_api import WooCommerceAPI
from config import config


class Crawler:
    """ Crawl all the WooCOmmerce Products and check if the image exist """

    def __init__(self):
        self._api: Optional[WooCommerceAPI] = None
        self._session = requests.session()
        self._output_file = "woocommerce_missing_images.txt"

    def api_setup(self):
        """ Setup WooCommerce API object """
        self._api = WooCommerceAPI(
            username=config.WooCommerceAPICred.USERNAME,
            password=config.WooCommerceAPICred.PASSWORD,
        )

    def crawl(self):
        """ Crawl list of products """
        self.api_setup()
        page = 1
        products, success = self._api.get_all_products(page=page)
        with open(self._output_file, mode="w") as fh_:
            while products:
                print(f"Procesing products from page {page}")
                for product in products:
                    sku = product.get("sku")
                    name = product.get("name")
                    print(f"Checking for product SKU: {sku} Name: {name}")
                    images = product.get("images")
                    if images:
                        for image in images:
                            url = image["src"]
                            if not self.check_url_alive(url):
                                msg = f"--> Image url {url} doesn't exist for product " \
                                      f"SKU: {sku} Name: {name}"
                                print(msg)
                                fh_.write(f"{msg}\n")

                # Sleep for sometime
                time.sleep(2)
                page += 1
                products, success = self._api.get_all_products(page=page)

    def check_url_alive(self, url):
        """ Check if the image url exist """
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        response = self._session.get(url=url, headers=headers)
        if response.status_code == requests.codes.ok:
            return True
        else:
            return False
