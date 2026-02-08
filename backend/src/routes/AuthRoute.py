from fastapi import APIRouter, HTTPException , Depends
from src.models.User import User as UserModel
from src.models.LoginModel import LoginModel
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer , HTTPBasicCredentials
from src.config.database import db as async_db
from bson import ObjectId
import bcrypt
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

SECRET_KEY = os.getenv("JWT_AUTH")


security = HTTPBearer()

from bson import ObjectId
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("userId")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await authCollection.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


if not SECRET_KEY:
    raise RuntimeError("JWT_AUTH is not set in .env")

routes = APIRouter(prefix="/api/v1/auth")
authCollection = async_db["user"]


# ================= REGISTER =================
@routes.post("/register")
async def register(data: UserModel):

    # Convert Pydantic → dict
    user_data = data.model_dump()

    # Normalize email
    user_data["email"] = user_data["email"].lower()

    # Check email existence
    if await authCollection.find_one({"email": user_data["email"]}):
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash password
    salt = bcrypt.gensalt(12)
    user_data["password"] = bcrypt.hashpw(
        user_data["password"].encode("utf-8"),
        salt
    ).decode("utf-8")

    user_data["created_at"] = datetime.utcnow()

    # Insert user
    result = await authCollection.insert_one(user_data)

    # Create JWT
    token = jwt.encode(
        {"userId": str(result.inserted_id)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "message": "Registered successfully",
        "token": token
    }


# ================= LOGIN =================
@routes.post("/login")
async def login(data: LoginModel):

    user = await authCollection.find_one(
        {"email": data.email.lower()}
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not bcrypt.checkpw(
        data.password.encode("utf-8"),
        user["password"].encode("utf-8")
    ):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create JWT
    token = jwt.encode(
        {"userId": str(user["_id"])},
        SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }


@routes.get("/profile")
async def userProfile(data:str = Depends(get_current_user)):
    return {"message": "User profile endpoint"}