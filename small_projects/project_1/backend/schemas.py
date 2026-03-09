from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class Product(BaseModel):
    name: str = Field(min_length=5, max_length=25)
    description: str = Field(min_length=5, max_length=100)
    category: str = Field(min_length=5, max_length=15)
    
    price: float 
    quantity: int
    
    in_stock: bool = True

class ProductCreate(Product):
    pass

class ProductResponse(Product):
    model_config = ConfigDict(from_attributes=True)

    id: int