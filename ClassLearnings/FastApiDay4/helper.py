# Function to check teh existence of the product.
def find_product(product_id: int, products: list):
    for product in products:
        if product.id == product_id:
            return product

    return None
