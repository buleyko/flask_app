from flask import request, redirect, session
from app.http.blueprints.prime import bp_prime
from app.vendors.helpers.config import cfg

__all__ = ('change_locale',)



@bp_prime.route('/change-locale/<lang>/', methods=['GET'])
def change_locale(lang):
	session['current_language'] = lang
	return redirect(request.referrer)