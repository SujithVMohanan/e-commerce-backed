
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.security import hash_password
from app.modules.users.exceptions import UserAlreadyExistsError
from app.modules.users.models import User
from app.modules.users.repository import get_user_by_email
from app.modules.users.schemas import UserRegisterSchema




async def register_user(
    session: AsyncSession,
    user_data: UserRegisterSchema,
) -> User:

    email = str(user_data.email).lower()

    try:
        async with session.begin():

            existing_user = await get_user_by_email(
                session,
                email,
            )

            if existing_user:
                raise UserAlreadyExistsError(
                    "An account with this email already exists."
                )

            user = User(
                email=email,
                password_hash=hash_password(
                    user_data.password
                ),
                full_name=user_data.full_name,
                phone_number=user_data.phone_number,
            )

            session.add(user)

            await session.flush()
            await session.refresh(user)

        return user

    except IntegrityError as exc:
        raise UserAlreadyExistsError(
            "An account with this email already exists."
        ) from exc
