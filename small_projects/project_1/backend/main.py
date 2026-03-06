from fastapi import FastAPI
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    in_stock: bool

app = FastAPI()

products = []

@app.get("/")
def home():
    return "message: This is home page"

@app.post("/products/add")
def add_product(product: Product):
    products.append(product)

    return {
        "message": "product has been added"
    }

@app.get("/products/get")
def get_products():
    return {
        "message" : "Products has been fetched",
        "products": products
    }