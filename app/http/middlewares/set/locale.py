from app.extensions import babel 
from flask import session, request, g
from app.vendors.helpers.config import cfg

__all__ = ('locale_middleware',)


def locale_middleware(app): 
	''' Set app locale '''
	@babel.localeselector 
	def get_locale():
		return g.current_language

	@app.before_request 
	def lang():
		current_language = session.get('current_language', None)
		if current_language is None or current_language not in cfg('ACCEPT_LANGUAGES'):
			current_language = request.accept_languages.best_match(cfg('ACCEPT_LANGUAGES'))
		g.current_language = current_language

	@app.context_processor 
	def inject_lang():
		return { 'current_language': g.current_language }