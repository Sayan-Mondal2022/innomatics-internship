from fastapi import FastAPI, status, HTTPException, Query
from schemas import Product, Customer, OrderRequest
from helper import find_product

app = FastAPI()

products = []
cart = []


@app.post("/api/cart/add", status_code=status.HTTP_201_CREATED)
def add_product_to_cart(
    product_id: int = Query(description="ID of the product added in the CART"),
    quantity: int = Query(default=1, description="How many items?"),
):
    product = find_product(product_id, products)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="PRODUCT NOT FOUND"
        )


@app.get("/api/cart", response_model=list[Product], status_code=status.HTTP_200_OK)
def view_products():
    pass


@app.delete("/api/cart/remove/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int):
    pass


# @app.get
