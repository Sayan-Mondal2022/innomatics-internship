from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class Product(BaseModel):
    product_id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=100)
    sub_category: str = Field(min_length=2, max_length=100)
    quantity: int = Field(gt=0, default=1)
    price: int = Field(ge=0)
    in_stock: bool = True


class UpdateProduct(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    category: str | None = Field(default=None, min_length=2, max_length=100)
    sub_category: str | None = Field(default=None, min_length=2, max_length=100)
    quantity: int | None = Field(default=None, gt=0)
    price: int | None = Field(default=None, gt=0)
    in_stock: bool | None = None


# Customer Data.
class Customer(BaseModel):
    customer_name: str = Field(min_length=2, max_length=50)
    email: EmailStr = Field(min_length=5, max_length=25)
    password: str = Field(min_length=6)
    contact_number: str = Field(min_length=10, max_length=13)
    delivery_address: str = Field(min_length=10, max_length=250)


class CustomerResponse(Customer):
    customer_id: int


# Cart
class CartResponse(BaseModel):
    cart_id: int  # -> This will be allocated directly by DB
    customer_id: (
        int  # -> This will be linking with the customer_id from the Customer table
    )
    created_at: datetime


class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    product_name: str
    quantity: int
    price: int


# Order Table
class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    total_products: int
    total_amount: int
    status: str


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    product_name: str
    quantity: int
    price: int
    sub_total: int  # sub_total = quantity * price
