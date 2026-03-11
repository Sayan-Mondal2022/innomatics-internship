from fastapi import FastAPI, Query
from schemas import OrderRequest, CustomerFeedback, OrderItem, BulkOrder

app = FastAPI()

products = [
    {
        "id": 1,
        "name": "Wireless Mouse",
        "price": 499,
        "category": "Electronics",
        "in_stock": True,
    },
    {
        "id": 2,
        "name": "Notebook",
        "price": 99,
        "category": "Stationery",
        "in_stock": True,
    },
    {
        "id": 3,
        "name": "USB Hub",
        "price": 799,
        "category": "Electronics",
        "in_stock": False,
    },
    {
        "id": 4,
        "name": "Pen Set",
        "price": 49,
        "category": "Stationery",
        "in_stock": True,
    },
]

orders = []
order_counter = 1

feedback = []


@app.get("/")
def home():
    return {"message": "Welcome to our E-commerce API"}


@app.get("/products")
def get_all_products():
    return {"products": products, "total": len(products)}


# QUESTION - 1: Filter Products by Minimum Price
@app.get("/products/filter")
def filter_products(
    category: str = Query(None),
    max_price: int = Query(None),
    in_stock: bool = Query(None),
    min_price: int = Query(None),
):
    result = products
    if category:
        result = [p for p in result if p["category"] == category]
    if max_price:
        result = [p for p in result if p["price"] <= max_price]
    if min_price:
        result = [p for p in result if p["price"] >= min_price]
    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]

    return {"filtered_products": result, "count": len(result)}


# QUESTION - 4: Build a Product Summary Dashboard
@app.get("/products/summary")
def get_product_summary():
    in_stock_count = 0
    out_of_stock_count = 0
    total_products = 0
    categories = set()
    most_expensive = {"name": products[0]["name"], "price": products[0]["price"]}
    cheapest = {"name": products[0]["name"], "price": products[0]["price"]}

    for product in products:
        if product["in_stock"] == True:
            in_stock_count += 1
        else:
            out_of_stock_count += 1

        if most_expensive["price"] < product["price"]:
            most_expensive["name"] = product["name"]
            most_expensive["price"] = product["price"]

        if cheapest["price"] > product["price"]:
            cheapest["name"] = product["name"]
            cheapest["price"] = product["price"]

        categories.add(product["category"])

        total_products += 1

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": most_expensive,
        "cheapest": cheapest,
        "categories": list(categories),
    }


# QUESTION - 2: Get Only the Price of a Product
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"name": product["name"], "price": product["price"]}
    return {"error": "Product not found"}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    return {"error": "Product not found"}


@app.post("/orders")
def place_order(order_data: OrderRequest):
    global order_counter
    product = next((p for p in products if p["id"] == order_data.product_id), None)
    if product is None:
        return {"error": "Product not found"}
    if not product["in_stock"]:
        return {"error": f"{product['name']} is out of stock"}
    total_price = product["price"] * order_data.quantity
    order = {
        "order_id": order_counter,
        "customer_name": order_data.customer_name,
        "product": product["name"],
        "quantity": order_data.quantity,
        "delivery_address": order_data.delivery_address,
        "total_price": total_price,
        "status": "confirmed",
    }
    orders.append(order)
    order_counter += 1
    return {"message": "Order placed successfully", "order": order}


def get_product(item: OrderItem) -> dict:
    for product in products:
        if item.product_id == product["id"]:
            return product


# QUESTION - 5: Validate & Place a Bulk Order
@app.post("/orders/bulk")
def bulk_orders(data: BulkOrder):
    confirmed_items = []
    failed_items = []
    total = 0

    for item in data.items:
        product = get_product(item)

        if product and product["in_stock"]:
            total += product["price"] * item.quantity
            confirmed_items.append(
                {
                    "product": product["name"],
                    "qty": item.quantity,
                    "subtotal": product["price"] * item.quantity,
                }
            )
        elif product:
            failed_items.append(
                {
                    "product_id": item.product_id,
                    "reason": f"{product['name']} is out of stock",
                }
            )
        else:
            failed_items.append(
                {"product_id": item.product_id, "reason": "Product Not Found"}
            )

    return {
        "company": data.company_name,
        "confirmed": confirmed_items,
        "failed": failed_items,
        "grand_total": total,
    }


@app.get("/orders")
def get_all_orders():
    return {"orders": orders, "total_orders": len(orders)}


# QUESTION - 3: Accept Customer Feedback
@app.post("/feedback")
def create_feedback(customer_feedback: CustomerFeedback):
    feedback.append(customer_feedback)

    return {
        "message": "Feedback submitted successfully",
        "feedback": customer_feedback,
        "total_feedback": len(feedback),
    }
