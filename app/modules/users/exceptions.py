
from app.core.exceptions import AppException


class UserAlreadyExistsError(AppException):

    def __init__(self):
        super().__init__(
            message="An account with this email already exists",
            status_code=409,
            code="USER_ALREADY_EXISTS",
            field="email",
        )
