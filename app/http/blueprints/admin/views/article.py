from flask import (render_template, redirect, url_for, request, flash, g, abort, current_app,)
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
	Category,
	Article,
	ArticleBody,
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
	categories = db.session.execute(
		db.select(Category).order_by(desc('created_at'))
	).scalars().all()
	return render_template('admin/article/create.html',
		categories = categories,
	)


@bp_admin.route('/article/store/', methods=['POST']) 
@login_required
def article_store():
	gate.allow(['access_admin_pages'], 403)
	categories = db.session.execute(
		db.select(Category).order_by(desc('created_at'))
	).scalars().all()
	if request.validate.post({
			'name': 'required|min:4',
			'short_desc': 'required|min:10|max:200',
			'body': 'required',
		}):
		thumb = None
		if 'thumb' in request.files and request.files['thumb'].filename != '':
			thumb = Article.resize_thumbnail(request.files['thumb'])
			if thumb is None:
				flash(_l(u'Thumbnail not saved', category='warning'))
		is_shown = True if request.form.get('is_shown') == 'on' else False
		is_blocked = True if request.form.get('is_blocked') == 'on' else False
		article = Article(
			name =        request.form.get('name', ''),
			short_desc =  request.form.get('short_desc', ''),
			is_shown =    is_shown,
			is_blocked =  is_blocked,
			thumb =       thumb,
			category_id = request.form.get('category_id'),
		)
		article.bodies.append(
			ArticleBody(
				lang=g.current_language, 
				body=request.form.get('body', '')
			)
		)
		article.save()
		return redirect(url_for('admin.article_list'))
	return render_template('admin/article/create.html',
		categories = categories,
	)


@bp_admin.route('/article/<int:art_id>/show', methods=['GET']) 
@login_required
def article_show(art_id):
	gate.allow(['access_admin_pages'], 403)
	article_select = db.select(
			Article, ArticleBody.body
		).\
		filter_by(id=int(art_id)).\
		outerjoin(Article.bodies).\
		filter_by(lang=g.current_language)
	try:
		article = db.session.execute(article_select).one()
	except NoResultFound as e:
		return abort(404)

	return render_template('admin/article/show.html',
		article = article,
	)


@bp_admin.route('/article/<int:art_id>/edit/', methods=['GET']) 
@login_required
def article_edit(art_id):
	gate.allow(['access_admin_pages'], 403)
	article = db.get_or_404(Article, int(art_id))
	categories = db.session.execute(
		db.select(Category).order_by(desc('created_at'))
	).scalars().all()
	return render_template('admin/article/edit.html',
		article = article,
		categories = categories,
	)


@bp_admin.route('/article/<int:art_id>/update/', methods=['POST']) 
@login_required
def article_update(art_id):
	gate.allow(['access_admin_pages'], 403)
	article = db.get_or_404(Article, int(art_id))
	categories = db.session.execute(
		db.select(Category).order_by(desc('created_at'))
	).scalars().all()
	if request.validate.post({
			'name': 'required|min:4',
			'short_desc': 'required|min:10|max:200',
		}):
		thumb = None
		if 'thumb' in request.files and request.files['thumb'].filename != '':
			thumb = Article.resize_thumbnail(request.files['thumb'])
			if thumb is None:
				flash(_l(u'Thumbnail not saved', category='warning'))
		is_shown = True if request.form.get('is_shown') == 'on' else False
		is_blocked = True if request.form.get('is_blocked') == 'on' else False
		
		article.name =       request.form.get('name', ''),
		article.short_desc = request.form.get('short_desc', '')
		article.is_shown =   is_shown
		article.is_blocked = is_blocked
		article.category_id = request.form.get('category_id')
		
		article.save()
		article_body = db.one_or_404(
			db.select(ArticleBody).filter_by(article_id=int(art_id).filter_by(lang=g.current_language))
		)
		article_body.body = request.form.get('article_body', '')
		article_body.save()
		return redirect(url_for('admin.article_list'))
	return render_template('admin/article/edit.html',
		article = article,
		categories = categories,
	)


@bp_admin.route('/article/<int:art_id>/destroy/', methods=['GET']) 
@login_required
def article_destroy(art_id):
	gate.allow(['access_admin_pages'], 403)
	article = db.get_or_404(Article, int(art_id))
	article.destroy()
	return redirect(url_for('admin.article_list'))
