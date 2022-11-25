from flask import Blueprint

__all__ = ('bp_error',)

def bp_error():
	''' Base blueprint for error pages of App '''
	name = 'error'
	error = Blueprint(name, __name__, url_prefix='/error/')

	return error