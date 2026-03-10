from fastapi import FastAPI, status, Depends, HTTPException
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
    "/api/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(product: ProductCreate, db: Annotated[Session, Depends(get_db)]):
    results = db.execute(
        select(models.Product).where(models.Product.name.ilike(product.name))
    )

    exist_product = results.scalars().first()

    if exist_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product already Exist"
        )

    new_product = models.Product(
        name=product.name,
        description=product.description,
        category=product.category,
        price=product.price,
        quantity=product.quantity,
        in_stock=product.in_stock,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get(
    "/api/products",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
)
def get_products(
    name: str | None = None,
    category: str | None = None,
    in_stock: bool | None = None,
    db: Annotated[Session, Depends(get_db)] = None,
):
    query = select(models.Product)

    if name:
        query = query.where(models.Product.name.ilike(f"%{name}%"))

    if category:
        query = query.where(models.Product.category == category)

    if in_stock is not None:
        query = query.where(models.Product.in_stock == in_stock)

    products = db.execute(query).scalars().all()

    return products


@app.get(
    "/api/products/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
def get_product_by_id(product_id: int, db: Annotated[Session, Depends(get_db)]):
    product = (
        db.execute(select(models.Product).where(models.Product.id == product_id))
        .scalars()
        .first()
    )
    if product:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product doesn't exist"
    )
