from flask import g
from flask_login import current_user
from app.extensions import login_manager
from app.extensions import db

__all__ = ('auth_middleware',)


def auth_middleware(app):
	# Get Current User
	from app.models.user import User

	@login_manager.user_loader
	def load_user(userid):
		try:
			return db.get_or_404(User, int(userid))
		except (TypeError, ValueError):
			return None

	# Add Curent User In Request Context
	@app.before_request
	def guser():
		g.user = current_user

	# Add Curent User In Jinja2 Context (In Templates)
	@app.context_processor
	def inject_user():
		try:
			return { 'user': g.user }
		except AttributeError:
			return { 'user': None }