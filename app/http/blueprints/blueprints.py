from .prime.prime import bp_prime
from .admin.admin import bp_admin 
from .error.error import bp_error
from .auth.auth import bp_auth

__all__ = ('blueprints',)

blueprints = [
	bp_prime,
	bp_admin,
	bp_error,
	bp_auth,
]