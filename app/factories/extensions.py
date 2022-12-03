from app.extensions import (
	login_manager, 
	babel,
	db, 
	migrate,
	csrf,
	mail,
)

__all__ = ('configuration_extensions',)



def configuration_extensions(
		app, 
		login_manager = login_manager,
		babel = babel,
		db = db,
		migrate = migrate,
		csrf = csrf,
		mail = mail,
	): 
	""" Configuration of extensions from app.config """
	db.init_app(app)

	migrate.init_app(app, db)

	login_manager.init_app(app)
	login_manager.login_view = app.config['LOGIN_VIEW']
	login_manager.login_message = app.config['LOGIN_MESSAGE']

	babel.init_app(app)

	csrf.init_app(app)

	mail.init_app(app)