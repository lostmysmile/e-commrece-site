from typing import NoReturn

from flask import jsonify
from sqlalchemy.exc import IntegrityError, OperationalError


class AppError(Exception):
    status_code = 500
    message = "Internal server error"

    def __init__(self, message: str | None = None, context: str | None = None) -> None:
        super().__init__(message)
        if message:
            self.message = (message)
        self.context = (context)

    def to_dict(self):
        data = {"error": self.__class__.__name__,
                "message": self.message, }
        if self.context:
            data["context"] = self.context
        return data

    def http_response(self):
        return self.to_dict(), self.status_code


class ValidationError(AppError):
    status_code = 400
    message = "Invalid input"


class NotFoundError(AppError):
    status_code = 404
    message = "Resource not found"


class ConflictError(AppError):
    status_code = 409
    message = "Conflict occurred"
    code = "CONFLICT"


class DatabaseError(AppError):
    status_code = 500
    message = "Database error"


def handle_error(e: IntegrityError | OperationalError | TypeError) -> NoReturn:
    if isinstance(e, TypeError):
        raise ValidationError("Missing required keys", (e.args[0]))

    error_message = str(e.orig).lower()

    if isinstance(e, IntegrityError):
        if "unique" in error_message:
            raise ConflictError("Input already exists", context=str(e.orig))
        elif "null" in error_message:
            raise ValidationError("Input is null", context=str(e.orig))
        else:
            ConflictError("Integrity constraint violated")
    if isinstance(e, OperationalError):
        raise DatabaseError("Database unavailable", context=str(e.orig))
    raise DatabaseError(message="Unknown database error", context=str(e.orig))
