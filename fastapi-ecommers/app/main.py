from fastapi import FastAPI, HTTPException , Query
from services.products import fetch_all_products
from services.products import fetch_product_by_id

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running . Kanhaiya Kumar Singh "}

# @app.get("/products/{id}")
# def get_product(id: int):
#     return fetch_product_by_id(id)


@app.get("/productsAll")
def get_all_products():
    return fetch_all_products()


@app.get("/products")
def list_products(
    name: str = Query(
        "",
        min_length=1,
        max_length=50,
        description="Search by product name (case insensitive)"
    ),
    sort_by_price : bool = Query(
        False,
        description="Sort products by price in ascending order"
    ),
    limit : int = Query(
        default=0,
        ge=1,
        le=100,
        description="Limit the number of products returned"
    )
):
    products = fetch_all_products()

    if name.strip():
        needle = name.strip().lower()
        products = [
            p for p in products
            if needle in p.get("name", "").lower()
        ]

        if not products:
            raise HTTPException(
                status_code=404,
                detail=f"No product found matching name={name}"
            )
        
        if sort_by_price:
            products.sort(key=lambda x: x.get("price", 0))
        if limit > 0:
            products = products[:limit]

    return {
        "total": len(products),
        "products": products
    }

