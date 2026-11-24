
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.modules.users.exceptions import UserAlreadyExistsError
from app.modules.users.schemas import (
    UserRegisterSchema,
    UserResponseSchema,
)
from app.modules.users.service import register_user


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    user_data: UserRegisterSchema,
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await register_user(
            session=session,
            user_data=user_data,
        )

        return user

    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
