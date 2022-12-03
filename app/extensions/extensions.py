from app.vendors.base.database import (
	AppModel,
	AppSession,
)
from app.vendors.helpers.config import cfg

# Auth
from flask_login import LoginManager
login_manager = LoginManager()

# Localization
from flask_babel import Babel
babel = Babel()

# Database
from flask_sqlalchemy import SQLAlchemy 
# db = SQLAlchemy()
db = SQLAlchemy(
	model_class=AppModel,
	session_options={'class_': AppSession}
)

from flask_migrate import Migrate
migrate = Migrate()

# Logger
import logging
logger = logging.getLogger()

# CSRF
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

# Celery
from celery import Celery 
celery = Celery('CeleryApp', broker=cfg('CELERY_BROKER_URL'))

# Mail
# from flask_mail import Mail
# mail = Mail()
