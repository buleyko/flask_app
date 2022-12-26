from flask import (render_template, request, redirect, session, flash, current_app, g, jsonify)
from app.vendors.helpers.pagination import get_current_page
from app.http.blueprints.prime import bp_prime
from flask_babel import lazy_gettext as _l
from app.vendors.helpers.config import cfg
from app.extensions import db
from sqlalchemy import (
	func, 
	desc,
)
from app.models import (
	Category,
	Article,
	Tag,
)

__all__ = ('home',)




@bp_prime.route('/', methods=['GET']) 
def home():
	select_categories = db.select(
			Category, 
			func.count(Article.id).label('articles_count')
		).\
		filter_by(is_blocked=False).filter_by(is_shown=True).\
		outerjoin(Category.articles).\
		group_by(Category._name).\
		order_by(desc('articles_count')).\
		limit(cfg('CATEGORIES_ON_HOMEPAGE'))
	categories = db.session.execute(select_categories).all()

	# select_articles = db.select(
	# 		Article
	# 	).\
	# 	filter_by(is_blocked=False).filter_by(is_shown=True).\
	# 	filter(Article._name.comparator.contains('Zxcv')).\
	# 	distinct()

	select_articles = db.select(
			Article
		).\
		filter_by(is_blocked=False).filter_by(is_shown=True)
	if search_name := session.get('search_name', False):
		select_articles = select_articles.filter(
			Article._name.comparator.contains(search_name.strip())
		)
	select_articles = select_articles.distinct()

	pagination_articles = db.paginate(select_articles,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('prime/home.html',
		categories = categories,
		pagination_articles = pagination_articles,
	)
