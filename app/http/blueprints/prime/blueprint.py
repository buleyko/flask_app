from flask import Blueprint

__all__ = ('bp_prime',)


def bp_prime():
	''' Base blueprint for prime pages of App '''
	name = 'prime'
	prime = Blueprint(name, __name__, url_prefix='/')

	return prime