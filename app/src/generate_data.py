from app.db.models import Product, Store, ProductStore
from loguru import logger
import os
import pandas as pd
import random
from uuid import uuid4

DATA_STORAGE = os.environ.get("APP_DATA_STORAGE")

OPENING_HOURS = ["09:00-18:00", "10:00-20:00"]
PRODUCT_TYPES = ["TYPE 1", "TYPE 2", "TYPE 3", "TYPE 4"]


class DataGenerator:
    def __init__(self):
        self.products = []
        self.stores = []
        self.products_stores = []

    def generate_products(self, quantity: int) -> None:
        for i in range(quantity):
            p = Product(
                id=str(uuid4()),
                brand=f"Brand {int(quantity*random.random())}",
                type=random.choice(PRODUCT_TYPES),
                calories=100*random.random(),
                saturated=random.random(),
                carbohydrates=random.random()
            )
            self.products.append(p)

    def generate_stores(self, quantity: int) -> None:
        for i in range(quantity):
            s = Store(
                id=str(uuid4()),
                name=f"Name {i}",
                address=f"Address {i}",
                opening_hours=random.choice(OPENING_HOURS)
            )
            self.stores.append(s)

    def generate_products_for_stores(self, max_products_per_store: int, max_price: float) -> None:
        for store in self.stores:
            store_quantity = int(max_products_per_store*random.random())
            products = random.sample(self.products, k=store_quantity)
            for product in products:
                ps = ProductStore(
                    id=str(uuid4()),
                    product_id=product.id,
                    store_id=store.id,
                    price=round(max_price*random.random(), 2)
                )
                ps.product = product
                ps.store = store
                self.products_stores.append(ps)

    def generate(self, product_quantity: int = 50, store_quantity: int = 10,
                 max_products_per_store: int = 20, max_price: float = 100) -> None:
        logger.info("Generating random data.")
        self.generate_products(product_quantity)
        self.generate_stores(store_quantity)
        self.generate_products_for_stores(max_products_per_store, max_price)

    def products_to_df(self):
        data = []
        for product in self.products:
            data.append({
                "id": product.id,
                "brand": product.brand,
                "type": product.type,
                "calories": product.calories,
                "saturated": product.saturated,
                "carbohydrates": product.carbohydrates
            })
        products_df = pd.DataFrame(columns=["id", "brand", "type", "calories", "saturated", "carbohydrates"], data=data)
        return products_df

    def products_to_csv(self):
        products_df = self.products_to_df()
        products_df.to_csv(os.path.join(DATA_STORAGE, "products.csv"), index=False)

    def stores_to_df(self):
        data = []
        for store in self.stores:
            data.append({
                "id": store.id,
                "name": store.name,
                "address": store.address,
                "opening_hours": store.opening_hours
            })
        stores_df = pd.DataFrame(columns=["id", "name", "address", "opening_hours"], data=data)
        return stores_df

    def stores_to_csv(self):
        stores_df = self.stores_to_df()
        stores_df.to_csv(os.path.join(DATA_STORAGE, "stores.csv"), index=False)

    def products_stores_to_df(self):
        data = []
        for ps in self.products_stores:
            data.append({
                "id": ps.id,
                "product_id": ps.product_id,
                "store_id": ps.store_id,
                "price": ps.price
            })
        products_stores_df = pd.DataFrame(columns=["id", "product_id", "store_id", "price"], data=data)
        return products_stores_df

    def products_stores_to_csv(self):
        products_stores_df = self.products_stores_to_df()
        products_stores_df.to_csv(os.path.join(DATA_STORAGE, "product_stores.csv"), index=False)

    def to_csv(self):
        logger.info("Saving csv files.")
        self.products_to_csv()
        self.stores_to_csv()
        self.products_stores_to_csv()


if __name__ == "__main__":
    data_generator = DataGenerator()
    data_generator.generate()
    data_generator.to_csv()
