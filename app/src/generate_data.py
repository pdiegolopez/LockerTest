from app.db.models import Product, Store, ProductStore
import pandas as pd
import random
from uuid import uuid4

OPENING_HOURS = ["09:00-18:00", "10:00-20:00"]
PRODUCT_TYPES = ["TYPE 1", "TYPE 2", "TYPE 3", "TYPE 4"]


class DataGenerator:
    products = []
    stores = []
    products_stores = []

    @classmethod
    def generate_products(cls, quantity: int) -> None:
        for i in range(quantity):
            p = Product(
                id=str(uuid4()),
                brand=f"Brand {int(quantity*random.random())}",
                type=random.choice(PRODUCT_TYPES),
                calories=100*random.random(),
                saturated=random.random(),
                carbohydrates=random.random()
            )
            cls.products.append(p)

    @classmethod
    def generate_stores(cls, quantity: int) -> None:
        for i in range(quantity):
            s = Store(
                id=str(uuid4()),
                name=f"Name {i}",
                address=f"Address {i}",
                opening_hours=random.choice(OPENING_HOURS)
            )
            cls.stores.append(s)

    @classmethod
    def generate_products_for_stores(cls, max_products_per_store: int, max_price: float) -> None:
        for store in cls.stores:
            store_quantity = int(max_products_per_store*random.random())
            products = random.sample(cls.products, k=store_quantity)
            for product in products:
                ps = ProductStore(
                    id=str(uuid4()),
                    product_id=product.id,
                    store_id=store.id,
                    price=round(max_price*random.random(), 2)
                )
                ps.product = product
                ps.store = store
                cls.products_stores.append(ps)

    @classmethod
    def generate(cls, product_quantity: int = 100, store_quantity: int = 10,
                 max_products_per_store: int = 30, max_price: float = 100) -> None:
        cls.generate_products(product_quantity)
        cls.generate_stores(store_quantity)
        cls.generate_products_for_stores(max_products_per_store, max_price)

    @classmethod
    def products_to_df(cls):
        data = []
        for product in cls.products:
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

    @classmethod
    def products_to_csv(cls):
        products_df = cls.products_to_df()
        products_df.to_csv("../data/products.csv", index=False)

    @classmethod
    def stores_to_df(cls):
        data = []
        for store in cls.stores:
            data.append({
                "id": store.id,
                "name": store.name,
                "address": store.address,
                "opening_hours": store.opening_hours
            })
        stores_df = pd.DataFrame(columns=["id", "name", "address", "opening_hours"], data=data)
        return stores_df

    @classmethod
    def stores_to_csv(cls):
        stores_df = cls.stores_to_df()
        stores_df.to_csv("../data/stores.csv", index=False)

    @classmethod
    def products_stores_to_df(cls):
        data = []
        for ps in cls.products_stores:
            data.append({
                "id": ps.id,
                "product_id": ps.product_id,
                "store_id": ps.store_id,
                "price": ps.price
            })
        products_stores_df = pd.DataFrame(columns=["id", "product_id", "store_id", "price"], data=data)
        return products_stores_df

    @classmethod
    def products_stores_to_csv(cls):
        products_stores_df = cls.products_stores_to_df()
        products_stores_df.to_csv("../data/product_stores.csv", index=False)

    @classmethod
    def to_csv(cls):
        cls.products_to_csv()
        cls.stores_to_csv()
        cls.products_stores_to_csv()


if __name__ == "__main__":
    DataGenerator.generate()
    DataGenerator.to_csv()
