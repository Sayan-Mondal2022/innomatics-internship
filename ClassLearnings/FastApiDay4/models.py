from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Product(Base):
    __tablename__ = "new_products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    sub_category = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1)
    in_stock = Column(Boolean, default=True)
