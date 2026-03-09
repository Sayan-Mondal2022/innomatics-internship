from fastapi import FastAPI, status, Depends
from schemas import ProductCreate, ProductResponse

from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from db import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "This is home page"}

@app.post(
    "/api/products/add",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def add_product(product: ProductCreate, db: Annotated[Session, Depends(get_db)]):
    new_product = models.Product(
        name = product.name,
        description = product.description,
        category = product.category,
        price = product.price,
        quantity = product.quantity,
        in_stock = product.in_stock,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@app.get("/api/products/get", response_model=list[ProductResponse])
def get_products(db: Annotated[Session, Depends(get_db)]):
    results = db.execute(
        select(models.Product)
    )

    products = results.scalars().all()

    return products