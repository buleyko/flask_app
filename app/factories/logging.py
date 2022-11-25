from app.vendors.utils.logger import setup_logger

__all__ = ('configuration_logger',)


def configuration_logger(app, logger):
	setup_logger(app, logger=logger)