from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    sub_category = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Integer, nullable=False)
    in_stock = Column(Boolean, default=True)


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(50), nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String)
    contact_number = Column(String(13), unique=True, nullable=False)
    delivery_address = Column(String(250), nullable=False)
