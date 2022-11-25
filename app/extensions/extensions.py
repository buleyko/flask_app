from app.vendors.base.database import (
	AppModel,
	AppSession,
)
from app.vendors.utils.gate import gate

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
# from celery import Celery 
# celery = Celery()


# Mail
# from flsk mail import mail
# mail = mail()
