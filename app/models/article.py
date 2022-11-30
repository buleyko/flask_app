from flask import g
from app.extensions import db
from sqlalchemy.orm import relationship
from app.vendors.helpers.config import cfg
from app.vendors.base.model import BaseModel
from app.vendors.helpers.model import (
	get_json_by_lang,
	set_json_by_lang,
)
from app.vendors.mixins.model import (
	ValidMixin,
	TimestampsMixin,
	ThumbnailMixin,
)
from sqlalchemy import (
	func, 
	desc,
)

__all__ = ('Article')



class Article(BaseModel, ValidMixin, TimestampsMixin, ThumbnailMixin): 
	__tablename__ = 'articles'
	
	id = db.Column(
		db.Integer, 
		primary_key=True
	)
	_name = db.Column('name',
		db.JSON, 
		unique=False,
		default = dict,
	) 
	_short_desc = db.Column('short_desc',
		db.JSON, 
		unique=False, 
		default = dict,
	)
	thumb = db.Column(
		db.String(255),
		unique=False,
		nullable=True,
	)
	bodies = relationship(
		'ArticleBody', 
		back_populates='article'
	)
	comments = relationship(
		'Comment', 
		back_populates='article'
	)
	category_id = db.Column(
		db.Integer, 
		db.ForeignKey('categories.id')
	)
	category = relationship(
		'Category', 
		back_populates='articles'
	)

	@property
	def name(self):
		return get_json_by_lang(self._name)

	@name.setter
	def name(self, v):
		self._name = set_json_by_lang(self._name, v)

	@property
	def short_desc(self):
		return get_json_by_lang(self._short_desc)

	@short_desc.setter
	def short_desc(self, v):
		self._short_desc = set_json_by_lang(self._short_desc, v)


	def __repr__(self):
		return f'Article: {self.name}'



class ArticleBody(BaseModel):
	__tablename__ = 'article_bodies'

	id = db.Column(
		db.Integer, 
		primary_key=True
	)
	lang = db.Column(
		db.String(10), 
		unique=False,
		nullable=False,
	) 
	body = db.Column(
		db.Text, 
		unique=False, 
		nullable=False,
	)
	article_id = db.Column(
		db.Integer, 
		db.ForeignKey('articles.id'),
	)
	article = relationship(
		'Article', 
		back_populates='bodies',
	)