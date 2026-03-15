from fastapi import FastAPI, status, HTTPException, Query, Depends
from schemas import Product, Customer, OrderRequest, ProductsResponse
from helper import find_product
from data import products

import models
from sqlalchemy.orm import Session
from database import Base, engine, get_db

app = FastAPI()
Base.metadata.create_all(bind=engine)

cart = []
orders = []


@app.post("/api/products")
def create_product(product: Product, db: Session = Depends(get_db)):

    new_product = models.Product(
        id=product.id,
        name=product.name,
        category=product.category,
        in_stock=product.in_stock,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get(
    "/api/products", response_model=ProductsResponse, status_code=status.HTTP_200_OK
)
def get_products():
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="PRODUCTS NOT FOUND"
        )

    return {
        "message": "Products has been fetched",
        "products": products,
        "total_products": len(products),
    }


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
