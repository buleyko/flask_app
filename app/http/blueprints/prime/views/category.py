from flask import (render_template, request, redirect, session, flash, current_app, g, abort, jsonify)
from app.vendors.helpers.pagination import get_current_page
from app.http.blueprints.prime import bp_prime
from sqlalchemy.orm.exc import NoResultFound
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
)

__all__ = (
	'category_list', 
	'category_articles',
)


@bp_prime.route('/category/list/', methods=['GET']) 
def category_list():
	select_categories = db.select(
			Category, 
			func.count(Article.id).label('articles_count')
		).\
		filter_by(is_blocked=False).filter_by(is_shown=True).\
		outerjoin(Category.articles).\
		group_by(Category._name).\
		order_by(desc('created_at'))
	pagination_categories = db.paginate(select_categories,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('prime/category/list.html',
		pagination_categories = pagination_categories,
	)



@bp_prime.route('/category/<int:cat_id>/articles/', methods=['GET']) 
def category_articles(cat_id):
	select_category = db.select(
			Category, 
			func.count(Article.id).label('articles_count')
		).\
		filter_by(id=int(cat_id)).\
		filter_by(is_blocked=False).filter_by(is_shown=True).\
		outerjoin(Category.articles)
	try:
		category = db.session.execute(select_category).one()
	except NoResultFound as e:
		return abort(404)

	select_articles = db.select(
			Article
		).\
		filter_by(category_id=int(cat_id)).\
		filter_by(is_blocked=False).filter_by(is_shown=True)
	pagination_articles = db.paginate(select_articles,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('prime/category/articles.html',
		category = category,
		pagination_articles = pagination_articles,

	)