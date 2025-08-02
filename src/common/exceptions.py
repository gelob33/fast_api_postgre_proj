# List of exception classes

class AppError(Exception):
    """Base class for all app-specific exceptions."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class DatabaseConnectionError(AppError):
    def __init__(self, message="Database connection failed"):
        super().__init__(message, status_code=500)


class BookNotFoundError(AppError):
    def __init__(self, book_id=None, title=None):
        msg = f"Book not found"
        if book_id:
            msg += f" with ID '{book_id}'."
        elif title:
            msg += f" with title '{title}'."
        super().__init__(msg, status_code=404)
