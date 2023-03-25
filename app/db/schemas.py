from pydantic import BaseModel, root_validator, validator
import re


class ProductIn(BaseModel):
    brand: str
    type: str
    calories: float
    saturated: float
    carbohydrates: float


class ProductModify(BaseModel):
    brand: str | None = None
    type: str | None = None
    calories: float | None = None
    saturated: float | None = None
    carbohydrates: float | None = None

    @root_validator
    def at_least_one(cls, values: dict):
        if not any(values.values()):
            raise ValueError("Wrong parameters")
        return values


class ProductOut(ProductIn):
    id: str


class StoreIn(BaseModel):
    name: str
    address: str
    opening_hours: str

    @validator("opening_hours")
    def format_hours(cls, v: str):
        # pattern hh:mm - hh:mm
        if not re.match(r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", v):
            raise ValueError("Wrong format. Must be hh:mm-hh:mm")
        return v


class StoreOut(StoreIn):
    id: str


class PriceIn(BaseModel):
    price: float


class PriceOut(PriceIn):
    id: str
    product_id: str
    store_id: str


class ProductWithPrice(ProductOut):
    price: float
