from .set.auth import auth_middleware
from .set.locale import locale_middleware

__all__ = ('middlewares',)

middlewares = [
	auth_middleware,
	locale_middleware,
]