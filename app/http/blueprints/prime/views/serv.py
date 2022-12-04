from flask import (request, redirect, session, jsonify,)
from app.http.blueprints.prime import bp_prime
from app.vendors.helpers.config import cfg


__all__ = ('change_locale', 'options',)



@bp_prime.route('/change-locale/<lang>/', methods=['GET'])
def change_locale(lang):
	session['current_language'] = lang
	return redirect(request.referrer)


@bp_prime.route('/options/', methods=['POST']) 
def options():
	return jsonify({'q':1000})

