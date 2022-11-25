from flask import Blueprint
from flask_login import login_required


__all__ = ('bp_admin',)

def bp_admin():
	''' Base blueprint for admin pages of App '''
	name = 'admin'
	admin = Blueprint(name, __name__, url_prefix='/admin/')

	return admin
