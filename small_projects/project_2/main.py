from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def say_hi():
    return {
        "message": "Hello!! guys, hope you all are doing well"
    }

@app.post("/products/add")
def add_products(product):
    return {
        "message": "Product has been added"
    }