from typing import Any, Generic, TypeVar

from pydantic import BaseModel, field_serializer, model_serializer

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str
    field: str | None = None

    @field_serializer("field")
    def serialize_field(self, value: str | None) -> str:
        return value or ""


class ResponseInfo(BaseModel, Generic[T]):
    success: bool
    message: str
    status_code: int
    data: T | None = None
    errors: list[ErrorDetail] | None = None

    @model_serializer(mode="wrap")
    def serialize_response(self, handler: Any) -> dict:
        response = handler(self)
        return self._replace_none(response)

    @classmethod
    def _replace_none(cls, value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: cls._replace_none(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [cls._replace_none(item) for item in value]

        if value is None:
            return ""

        return value