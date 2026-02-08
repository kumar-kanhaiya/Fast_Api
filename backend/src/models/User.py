from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    email: EmailStr = Field(..., description="Email is required")
    name: str = Field(..., description="Name is required")
    password: str = Field(..., description="Password is required")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    address: Optional[str] = None
    phone: Optional[str] = None
