from flask import render_template
from app.http.blueprints.error import bp_error

__all__ = (
	'forbidden_page', 
	'not_found_error', 
	'method_not_allowed',
	'internal_error',
)


@bp_error.app_errorhandler(400) 
def bad_request(error):
    return render_template("error/400.html", desc="Bad Request"), 400


@bp_error.app_errorhandler(403) 
def forbidden_page(error):
    return render_template("error/403.html", desc="Forbidden page"), 403


@bp_error.app_errorhandler(404) 
def not_found_error(error):
    return render_template('error/404.html', desc="Page not found"), 404


@bp_error.app_errorhandler(405) 
def method_not_allowed(error):
    return render_template("error/405.html", desc="Call wrong method"), 404


@bp_error.app_errorhandler(500) 
def internal_error(error):
    return render_template('error/500.html', desc="Server error"), 500