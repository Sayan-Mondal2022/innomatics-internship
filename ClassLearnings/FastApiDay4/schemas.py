from pydantic import BaseModel, Field


class Product(BaseModel):
    product_id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2)
    in_stock: bool = True


class Customer(BaseModel):
    customer_name: str = Field(min_length=2, max_length=20)
    delivery_address: str = Field(min_length=10, max_length=250)


class OrderRequest(Customer):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=10)


# class CartResponse:
