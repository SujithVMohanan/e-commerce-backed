
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterSchema(BaseModel):
    
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    full_name: str | None = Field(
        default=None,
        max_length=150,
    )

    phone_number: str | None = Field(
        default=None,
        max_length=20,
    )


class UserResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id              : uuid.UUID
    email           : EmailStr
    full_name       : str | None
    phone_number    : str | None
    is_active       : bool
    created_at      : datetime
