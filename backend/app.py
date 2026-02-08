from fastapi import FastAPI
from src.routes.PublicRoute import route as PublicRoute
from src.routes.AuthRoute import routes as AuthRoutes

# cors error resolve
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

#add midleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

app.include_router(PublicRoute)
app.include_router(AuthRoutes)
