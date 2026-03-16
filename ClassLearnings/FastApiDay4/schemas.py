from pydantic import BaseModel, Field


class Product(BaseModel):
    product_id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=100)
    sub_category: str = Field(min_length=2, max_length=100)
    quantity: int = Field(gt=0, default=1)
    in_stock: bool = True


class ProductResponse(Product):
    product_id: int = Field(gt=0)


class UpdateProduct(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    category: str | None = Field(default=None, min_length=2, max_length=100)
    sub_category: str | None = Field(default=None, min_length=2, max_length=100)
    quantity: int | None = Field(default=None, gt=0)
    in_stock: bool | None = None


class ProductsResponse(BaseModel):
    message: str
    products: list[Product]
    total_products: int


class Customer(BaseModel):
    customer_name: str = Field(min_length=2, max_length=20)
    delivery_address: str = Field(min_length=10, max_length=250)


class OrderRequest(Customer):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=10)


# class CartResponse:
