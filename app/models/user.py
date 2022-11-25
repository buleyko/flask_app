from flask_login import UserMixin
from app.vendors.base.model import BaseModel
from app.extensions import db
from hashlib import md5
from werkzeug.security import (
	generate_password_hash, 
	check_password_hash,
)
from app.vendors.mixins.model import (
	ValidMixin,
	TimestampsMixin,
)

__all__ = ('User')



class User(BaseModel, UserMixin, ValidMixin, TimestampsMixin): 
	__tablename__ = 'users'
	
	id = db.Column(
		db.Integer, 
		primary_key=True
	)
	username = db.Column(
		db.String(120), 
		unique=True,
		nullable=False,
	) 
	email = db.Column(
		db.String(120), 
		unique=True, 
		nullable=False,
	) 
	password = db.Column(
		db.String(120), 
		unique=False, 
		nullable=False,
	)
	permissions = db.Column(
		db.JSON, 
		unique=False,
		default = list,
	) 

	def __repr__(self):
		return f'User: {self.username}'


	def set_passwd(self, password):
		''' Set User Password By MD5 '''
		self.password = generate_password_hash(password)

	def check_passwd(self, password):
		''' Check User Password '''
		return check_password_hash(self.password, password)

	def can(self, perm_keys):
		if not (set(self.permissions) & set(perm_keys)):
			return False 
		return True

