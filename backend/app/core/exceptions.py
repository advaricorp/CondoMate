class CondoMateException(Exception):
    """Base exception for all CondoMate errors."""
    pass

class TenantLimitExceeded(CondoMateException):
    """Raised when a tenant has reached its user limit."""
    pass

class UserNotFound(CondoMateException):
    """Raised when a user is not found."""
    pass

class TenantNotFound(CondoMateException):
    """Raised when a tenant is not found."""
    pass

class InvalidCredentials(CondoMateException):
    """Raised when user credentials are invalid."""
    pass

class UserAlreadyExists(CondoMateException):
    """Raised when trying to create a user that already exists."""
    pass

class InvalidToken(CondoMateException):
    """Raised when a JWT token is invalid."""
    pass

class TokenExpired(CondoMateException):
    """Raised when a JWT token has expired."""
    pass

class UnauthorizedAccess(CondoMateException):
    """Raised when a user tries to access unauthorized resources."""
    pass

class DatabaseError(CondoMateException):
    """Raised when a database operation fails."""
    pass 