from app.db.db import engine
from app.db.models import Product, Store, ProductStore
from app.db.schemas import PriceIn, PriceOut
from app.db.schemas import ProductIn, ProductModify, ProductOut, ProductWithPrice
from app.db.schemas import StoreIn, StoreOut
from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from pydantic.schema import List
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import uuid4
import uvicorn

ALREADY_EXISTS = "Already exists"
RESOURCE_NOT_FOUND = "Resource not found"

app = FastAPI(responses={422: {"description": "Invalid parameters"}})


@app.get("/", status_code=HTTPStatus.OK)
async def root():
    return {"message": "Ok"}


@app.post("/products/", status_code=HTTPStatus.CREATED, response_model=ProductOut,
          responses={409: {"description": ALREADY_EXISTS}})
async def create_product(product: ProductIn):
    idx = str(uuid4())
    p = Product(**product.dict(), id=idx)
    with Session(engine) as session:
        try:
            session.add(p)
            session.commit()
        except IntegrityError:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=ALREADY_EXISTS)
    response = {**product.dict(), "id": idx}
    return response


@app.put("/product/{product_id}", status_code=HTTPStatus.OK, response_model=ProductOut,
         responses={404: {"description": RESOURCE_NOT_FOUND}})
async def modify_product(product_id: str, partial_product: ProductModify):
    query_select = select(Product).where(Product.id == product_id)
    query_update = update(Product).where(Product.id == product_id).values(**partial_product.dict(exclude_none=True))
    with Session(engine) as session:
        p = session.scalar(query_select)
        if not p:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=RESOURCE_NOT_FOUND)
        session.execute(query_update)
        session.commit()


@app.post("/stores/", status_code=HTTPStatus.CREATED, response_model=StoreOut,
          responses={409: {"description": ALREADY_EXISTS}})
async def create_store(store: StoreIn):
    idx = str(uuid4())
    p = Store(**store.dict(), id=idx)
    with Session(engine) as session:
        try:
            session.add(p)
            session.commit()
        except IntegrityError:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=ALREADY_EXISTS)
    response = {**store.dict(), "id": idx}
    return response


@app.post("/stores/{store_id}/products/{product_id}/", status_code=HTTPStatus.CREATED, response_model=PriceOut,
          responses={404: {"description": RESOURCE_NOT_FOUND}, 409: {"description": ALREADY_EXISTS}})
async def create_price(store_id: str, product_id: str, price: PriceIn):
    query_select_store = select(Store).where(Store.id == store_id)
    query_select_product = select(Product).where(Product.id == product_id)
    query_select_product_store = select(ProductStore).where(ProductStore.product_id == product_id,
                                                            ProductStore.store_id == store_id)
    with Session(engine) as session:
        p = session.scalar(query_select_product)
        s = session.scalar(query_select_store)
        if not p or not s:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=RESOURCE_NOT_FOUND)
        ps = session.scalar(query_select_product_store)
        if ps:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=ALREADY_EXISTS)
        idx = str(uuid4())
        ps = ProductStore(id=idx, product_id=product_id, store_id=store_id, price=price.price)
        session.add(ps)
        session.commit()
    response = {**price.dict(), "product_id": product_id, "store_id": store_id, "id": idx}
    return response


@app.get("/stores/{store_id}/products/", status_code=HTTPStatus.OK, response_model=List[ProductWithPrice])
async def get_products_for_store(store_id: str):
    query_ps = select(ProductStore).where(ProductStore.store_id == store_id)
    with Session(engine) as session:
        list_ps = session.scalars(query_ps).all()
        data = []
        for ps in list_ps:
            data.append(ProductWithPrice(
                id=ps.product.id,
                brand=ps.product.brand,
                type=ps.product.type,
                calories=ps.product.calories,
                saturated=ps.product.saturated,
                carbohydrates=ps.product.carbohydrates,
                price=ps.price
            ))
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
