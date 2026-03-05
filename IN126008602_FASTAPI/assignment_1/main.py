from fastapi import FastAPI

app = FastAPI()

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook','price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub','price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set','price':  49, 'category': 'Stationery',  'in_stock': True },
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True}, 
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
]

@app.get("/")
def home():
    return {"message": "Welcome to my E-commerce Store"}

@app.get("/products")
def get_all_products():
    if not products:
        return {
            "error": "No products found"
        }
        
    return {
        "products": products, 
        "total": len(products)
    }
    

@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    data = []
    
    for product in products:
        if product["category"] == category_name:
            data.append(product)

    if not data:
        return {"error": "No products found in this category"}
    
    return {
        "category": category_name,
        "products" : data,
        "total": len(data)
    }
    

@app.get("/products/instock")
def get_products_instock():
    data = []
    
    for product in products:
        if product["in_stock"] == True:
            data.append(product)
            
    if not data:
        return {
            "error": "Inventory is empty"
        }
        
    return {
        "in_stock_products": data,
        "count": len(data)
    }
    

@app.get("/store/summary")
def get_store_summary():
    in_stock_count = 0
    out_of_stock_count = 0
    total_products = 0
    categories = set()
    
    for product in products:
        if product["in_stock"] == True:
            in_stock_count += 1
        else:
            out_of_stock_count += 1
            
        categories.add(product["category"])
            
        total_products += 1
        
    store_name = "My E-commerce Store"
    
    return {
        "store_name": store_name,
        "total_products": total_products,
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock_count,
        "categories": list(categories)
    }
    
def match_keyword(keyword: str, products: list[dict]):
    result = []
    
    for product in products:
        if keyword in product["name"].lower():
            result.append(product)
            
    return result

@app.get("/products/search/{keyword}")
def search_product_by_name(keyword: str):
    matches = match_keyword(keyword.lower(), products)
    
    if not matches:
        return {
            "message": "No products matched your search"
        }
    
    return {
        "matched products": matches,
        "count": len(matches)
    }
    

@app.get("/products/deals")
def get_product_deals():
    lowest = products[0]
    highest = products[0]
    
    for product in products[1:]:
        if lowest["price"] > product["price"]:
            lowest = product
        
        if highest["price"] < product["price"]:
            highest = product
            
    return {
        "best_deal" : lowest,
        "premium_pick": highest
    }