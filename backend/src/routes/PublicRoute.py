from fastapi import APIRouter

route = APIRouter(prefix="/api/v1")

@route.get("/health")
def root():
    return {"message": "Hello World"}
