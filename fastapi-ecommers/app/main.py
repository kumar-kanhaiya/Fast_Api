from fastapi import FastAPI
from services.products import fetch_all_products

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running . Kanhaiya Kumar Singh "}

@app.get("/products/{id}")
def get_product(id: int):
    return {"product_id": id, "name": "Sample Product", "price": 19.99}


@app.get("/products")
def get_all_products():
    return fetch_all_products()
