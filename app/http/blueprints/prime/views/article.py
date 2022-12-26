from flask import (render_template, request, redirect, session, flash, current_app, g, abort, jsonify)
from app.vendors.helpers.pagination import get_current_page
from sqlalchemy.orm.exc import NoResultFound
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
	ArticleBody,
)

__all__ = (
	'article_list', 
	'article_item',
)



@bp_prime.route('/article/list/', methods=['GET']) 
def article_list():
	select_articles = db.select(
			Article
		).\
		filter_by(is_blocked=False).filter_by(is_shown=True)
	pagination_articles = db.paginate(select_articles,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('prime/article/list.html',
		pagination_articles = pagination_articles,
	)


@bp_prime.route('/article/<int:art_id>/item/', methods=['GET']) 
def article_item(art_id):
	article_select = db.select(
			Article, ArticleBody.body
		).\
		filter_by(id=int(art_id)).\
		filter_by(is_blocked=False).filter_by(is_shown=True).\
		outerjoin(Article.bodies).\
		filter_by(lang=g.current_language)
	try:
		article = db.session.execute(article_select).one()
	except NoResultFound as e:
		return abort(404)

	return render_template('prime/article/item.html',
		article = article,
	)