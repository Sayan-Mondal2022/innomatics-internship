from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    in_stock: bool = True


class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=100)
    delivery_address: str = Field(min_length=10)
