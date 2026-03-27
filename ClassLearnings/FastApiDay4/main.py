from fastapi import FastAPI, status, HTTPException, Query, Depends
from schemas import (
    Product,
    UpdateProduct,
    Customer,
    CustomerResponse,
)
from helper import find_product
from data import products
import models
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import Base, engine, get_db

# Try using argon2 instead
import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    # Convert → SHA256 (FIXED LENGTH = 64 chars)
    sha256_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    # Pass STRING to bcrypt (not bytes)
    return pwd_context.hash(sha256_hash)


app = FastAPI()
Base.metadata.create_all(bind=engine)

cart = []
orders = []


@app.get(
    "/api/customers",
    status_code=status.HTTP_200_OK,
    response_model=list[CustomerResponse],
)
def get_all_customers(db: Session = Depends(get_db)):
    customers = db.execute(select(models.Customer)).scalars().all()

    if not customers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customers Not Found"
        )

    return customers


@app.post(
    "/api/customers",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomerResponse,
)
def create_new_customer(customer: Customer, db: Session = Depends(get_db)):
    customers = db.execute(select(models.Customer)).scalars().all()

    new_customer = models.Customer(
        customer_id=len(customers) + 1,
        customer_name=customer.customer_name,
        email=customer.email,
        password=customer.password,
        contact_number=customer.contact_number,
        delivery_address=customer.delivery_address,
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@app.post(
    "/api/products",
    status_code=status.HTTP_201_CREATED,
    responses={400: {"description": "Bad Request"}},
    response_model=Product,
)
def create_product(product: Product, db: Session = Depends(get_db)):
    existing_product = (
        db.execute(
            select(models.Product).where(
                models.Product.product_id == product.product_id
            )
        )
        .scalars()
        .first()
    )

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exist"
        )

    new_product = models.Product(
        product_id=product.product_id,
        name=product.name,
        category=product.category,
        sub_category=product.sub_category,
        quantity=product.quantity,
        price=product.price,
        in_stock=product.in_stock,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return (
        db.execute(
            select(models.Product).where(
                models.Product.product_id == product.product_id
            )
        )
        .scalars()
        .first()
    )


@app.get(
    "/api/products",
    response_model=list[Product],
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Bad Request"},
        404: {"description": "Products Not Found"},
    },
)
def get_all_products(db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="DB is not connected"
        )

    products = db.execute(select(models.Product)).scalars().all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Products Not Found"
        )

    return products


@app.patch(
    "/api/products/{product_id}",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Product Not Found"},
    },
)
def update_product(product_id: int, data: UpdateProduct, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="DB is not connected"
        )

    product = (
        db.execute(
            select(models.Product).where(models.Product.product_id == product_id)
        )
        .scalars()
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found"
        )

    update_data = data.model_dump(exclude_unset=True)
    print(update_data)

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


@app.delete("/api/products/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="DB is not connected"
        )

    product = (
        db.execute(
            select(models.Product).where(models.Product.product_id == product_id)
        )
        .scalars()
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {"message": "Product has been Deleted"}


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


# @app.get
