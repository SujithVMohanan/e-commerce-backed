
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import ResponseInfo
from app.db.dependencies import get_db
from app.modules.users.schemas import (
    UserRegisterSchema,
    UserResponseSchema,
)
from app.modules.users.service import register_user


router = APIRouter()


@router.post(
    "/register",
    response_model=ResponseInfo[UserResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    user_data: UserRegisterSchema,
    session: AsyncSession = Depends(get_db),
):

    user = await register_user(
        session=session,
        user_data=user_data,
    )

    return ResponseInfo[UserResponseSchema](
        success=True,
        message="User registered successfully",
        status_code=status.HTTP_201_CREATED,
        data=user,
        errors=None,
    )
