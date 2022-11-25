from flask import (render_template, redirect, url_for, request, flash, g, current_app,)
from app.vendors.helpers.pagination import get_current_page
from app.http.blueprints.admin import bp_admin
from sqlalchemy.orm.exc import NoResultFound
from flask_login import login_required
from app.vendors.helpers.config import cfg
from app.extensions import logger
from app.extensions import db
from app.vendors.utils.gate import gate
from sqlalchemy import (
	func, 
	desc,
)
from app.models import (
	article,
	Article,
)

__all__ = (
	'article_list', 
	'article_create', 
	'article_store',
	'article_show',
	'article_edit',
	'article_destroy',
)


@bp_admin.route('/article/list/', methods=['GET']) 
@login_required
def article_list():
	gate.allow(['access_admin_pages'], 403)
	select_articles = db.select(Article).order_by(desc('created_at'))
	pagination_articles = db.paginate(select_articles,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('admin/article/list.html',
		pagination_articles = pagination_articles,
	)


@bp_admin.route('/article/create/', methods=['GET']) 
@login_required
def article_create():
	gate.allow(['access_admin_pages'], 403)
	return render_template('admin/article/create.html')


@bp_admin.route('/article/store/', methods=['POST']) 
@login_required
def article_store():
	gate.allow(['access_admin_pages'], 403)
	if request.validate.post({
			'name': 'required|min:4',
			'short_desc': 'required|min:10|max:200',
		}):
		# create new article
		return redirect(url_for('admin.article_list'))
	return render_template('admin/article/create.html')


@bp_admin.route('/article/<int:art_id>/show', methods=['GET']) 
@login_required
def article_show(art_id):
	gate.allow(['access_admin_pages'], 403)
	article = db.get_or_404(article, int(art_id))
	return render_template('admin/article/show.html',
		article = article,
	)


@bp_admin.route('/article/<int:art_id>/edit/', methods=['GET']) 
@login_required
def article_edit(art_id):
	gate.allow(['access_admin_pages'], 403)
	article = db.get_or_404(article, int(art_id))
	return render_template('admin/article/edit.html',
		article = article,
	)


@bp_admin.route('/article/<int:art_id>/update/', methods=['POST']) 
@login_required
def article_update(art_id):
	gate.allow(['access_admin_pages'], 403)
	article = db.get_or_404(article, int(art_id))
	if request.validate.post({
			'name': 'required|min:4',
			'short_desc': 'required|min:10|max:200',
		}):
		# update article
		return redirect(url_for('admin.article_list'))
	return redirect(url_for('admin.article_list'))


@bp_admin.route('/article/<int:art_id>/destroy/', methods=['GET']) 
@login_required
def article_destroy(art_id):
	gate.allow(['access_admin_pages'], 403)
	article = db.get_or_404(article, int(art_id))
	article.destroy()
	return redirect(url_for('admin.article_list'))
