from app.vendors.base.app import AppFlask
from app.http.blueprints import blueprints
from app.http.middlewares import middlewares
from app.http.context import handlers
from app.services.manager import commands
from app.extensions import logger
from app.config import Configuration
from app.factories import (
	configuration_app,
	registration_blueprints,
	configuration_logger,
	setup_middlewares,
	configuration_extensions,
	registration_commands,
	registration_filters,
	setup_context,
)

__all__ = ('create_app',)

def create_app():
	''' Creation and configuration flask app instance ''' 
	app = AppFlask(__name__,
		template_folder='resources/templates',
		static_url_path='/',
		static_folder='../public'
	)
	
	with app.app_context():
		configuration_app(app, Configuration())
		registration_blueprints(app, blueprints)
		setup_middlewares(app, middlewares)
		configuration_logger(app, logger)
		registration_commands(app, commands)
		setup_context(app, handlers)
		registration_filters(app)
		configuration_extensions(app)
		
	return app
