from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List


class Base(DeclarativeBase):
    pass


class ProductStore(Base):
    __tablename__ = "product_store"

    id: Mapped[str] = mapped_column(primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("product.id"), primary_key=True)
    store_id: Mapped[str] = mapped_column(ForeignKey("store.id"), primary_key=True)
    price: Mapped[float]

    product: Mapped["Product"] = relationship(back_populates="stores")
    store: Mapped["Store"] = relationship(back_populates="products")


class Product(Base):
    __tablename__ = "product"

    id: Mapped[str] = mapped_column(primary_key=True)
    brand: Mapped[str]
    type: Mapped[str]
    calories: Mapped[float]
    saturated: Mapped[float]
    carbohydrates: Mapped[float]

    stores: Mapped[List["ProductStore"]] = relationship(back_populates="product")

    def __repr__(self) -> str:
        return f"Product(id={self.id}, brand={self.brand}, type={self.type})"


class Store(Base):
    __tablename__ = "store"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str]
    opening_hours: Mapped[str]

    products: Mapped[List["ProductStore"]] = relationship(back_populates="store")

    def __repr__(self) -> str:
        return f"Store(id={self.id}, name={self.name})"
