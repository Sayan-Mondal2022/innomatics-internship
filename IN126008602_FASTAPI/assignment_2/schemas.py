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


class OrderItem(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(ge=1, le=50)


class BulkOrder(BaseModel):
    company_name: str = Field(min_length=2)
    contact_email: str = Field(min_length=5)
    items: list[OrderItem] = Field(min_length=1)


class CustomerFeedback(BaseModel):
    customer_name: str = Field(min_length=2)
    product_id: int = Field(gt=0)
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=300)
