from generate_data import DataGenerator
from loguru import logger
import pandas as pd
import requests
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000/"


class DataLoader:

    def __init__(self):
        self.data_generator = DataGenerator()
        self.products = None
        self.stores = None
        self.products_stores: pd.DataFrame | None = None

    def generate_random_data(self) -> None:
        self.data_generator.generate()
        self.products = self.data_generator.products_to_df()
        self.stores = self.data_generator.stores_to_df()
        self.products_stores = self.data_generator.products_stores_to_df()

    @staticmethod
    def post_data(url: str, body: dict):
        response = requests.post(url, json=body)
        if response.status_code != 201:
            raise ConnectionError(f"Error loading data.")
        return response.json()

    def insert_products(self) -> None:
        url = urljoin(BASE_URL, "products/")
        for _, row in self.products.iterrows():
            body = row.to_dict()
            auto_id = body.pop("id", None)
            response = self.post_data(url, body)
            # Replace auto generated id for real db id in products_stores df
            self.products_stores["product_id"] = self.products_stores["product_id"].str.replace(auto_id, response["id"])

    def insert_stores(self) -> None:
        url = urljoin(BASE_URL, "stores/")
        for _, row in self.stores.iterrows():
            body = row.to_dict()
            auto_id = body.pop("id", None)
            response = self.post_data(url, body)
            # Replace auto generated id for real db id in products_stores df
            self.products_stores["store_id"] = self.products_stores["store_id"].str.replace(auto_id, response["id"])

    def insert_products_stores(self) -> None:
        for _, row in self.products_stores.iterrows():
            body = row.to_dict()
            product_id = body.pop("product_id")
            store_id = body.pop("store_id")
            body.pop("id", None)
            url = urljoin(BASE_URL, f"stores/{store_id}/products/{product_id}/")
            self.post_data(url, body)

    def run(self) -> None:
        logger.info("Starting process")
        self.generate_random_data()
        self.insert_products()
        self.insert_stores()
        self.insert_products_stores()
        logger.info("Ending process")


if __name__ == "__main__":
    data_loader = DataLoader()
    data_loader.run()
