from flask import Blueprint

__all__ = ('bp_auth',)

def bp_auth():
	''' Base blueprint for auth pages of App '''
	name = 'auth'
	auth = Blueprint(name, __name__, url_prefix='/auth/')

	return auth