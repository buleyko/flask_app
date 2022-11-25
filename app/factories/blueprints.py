
__all__ = ('registration_blueprints',)


def registration_blueprints(app, blueprints): 
	''' Registration blueprints '''
	for blueprint in blueprints:
		app.register_blueprint(blueprint)