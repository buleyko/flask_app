from flask import (render_template, redirect, url_for, request, flash, g, current_app,)
from app.vendors.helpers.pagination import get_current_page
from app.http.blueprints.admin import bp_admin
from sqlalchemy.orm.exc import NoResultFound
from flask_login import login_required
from app.vendors.helpers.config import cfg
from flask_babel import lazy_gettext as _l
from flask_babel import _
from app.extensions import logger
from app.extensions import db
from app.vendors.utils.gate import gate
from app.http.blueprints.admin.forms import (
    CreateCategoryForm,
	UpdateCategoryForm,
)
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
	'category_create', 
	'category_store',
	'category_show',
	'category_edit',
	'category_destroy',
)


@bp_admin.route('/category/list/', methods=['GET']) 
@login_required
def category_list():
	gate.allow(['access_admin_pages'], 403)
	select_categories = db.select(Category).order_by(desc('created_at'))
	pagination_categories = db.paginate(select_categories,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('admin/category/list.html',
		pagination_categories = pagination_categories,
	)


@bp_admin.route('/category/create/', methods=['GET']) 
@login_required
def category_create():
	gate.allow(['access_admin_pages'], 403)
	form = CreateCategoryForm()
	form.parent_id.choices = Category.get_category_form_choices()
	return render_template('admin/category/create.html', 
		form = form,
	)


@bp_admin.route('/category/store/', methods=['POST']) 
@login_required
def category_store():
	gate.allow(['access_admin_pages'], 403)
	form = CreateCategoryForm()
	form.parent_id.choices = Category.get_category_form_choices()
	if form.validate_on_submit():
		thumb = None
		if form.thumb.data:
			thumb = Category.resize_thumbnail(form.thumb.data)
			if thumb is None:
				flash(_l(u'Thumbnail not saved', category='warning'))
		category = Category(
			name = form.name.data,
			short_desc = form.short_desc.data,
			is_shown = form.is_shown.data,
			thumb = thumb,
			parent_id = form.parent_id.data,
		)
		if not category.save():
			flash(_l(u'Category not saved', category='warning'))
		return redirect(url_for('admin.category_list'))
	return render_template('admin/category/create.html', 
		form = form
	)


@bp_admin.route('/category/<int:cat_id>/show', methods=['GET']) 
@login_required
def category_show(cat_id):
	gate.allow(['access_admin_pages'], 403)
	select_category = db.select(
			Category, 
			func.count(Article.id).label('articles_count')
		).\
		filter_by(id=cat_id).\
		outerjoin(Category.articles)
	try:
		category = db.session.execute(select_category).one()
	except NoResultFound as e:
		return abort(404)
	return render_template('admin/category/show.html',
		category = category,
	)


@bp_admin.route('/category/<int:cat_id>/edit/', methods=['GET']) 
@login_required
def category_edit(cat_id):
	gate.allow(['access_admin_pages'], 403)
	category = db.get_or_404(Category, int(cat_id))
	form = UpdateCategoryForm(obj=category)
	form.parent_id.choices = Category.get_category_form_choices()
	return render_template('admin/category/edit.html',
		category = category,
		form = form,
	)


@bp_admin.route('/category/<int:cat_id>/update/', methods=['POST']) 
@login_required
def category_update(cat_id):
	gate.allow(['access_admin_pages'], 403)
	category = db.get_or_404(Category, int(cat_id))
	form = UpdateCategoryForm(obj=category)
	form.parent_id.choices = Category.get_category_form_choices()
	if form.validate_on_submit():
		thumb = None
		if form.thumb.data:
			thumb = Category.resize_thumbnail(form.thumb.data)
			if thumb is None:
				flash(_l(u'Thumbnail not saved', category='warning'))
		category.name = form.name.data
		category.short_desc = form.short_desc.data
		category.is_shown = form.is_shown.data
		category.thumb = thumb
		category.parent_id = form.parent_id.data
		db.session.add(category)
		db.session.commit()
		if not category.save():
			flash(_l(u'Category not updated', category='warning'))
		return redirect(url_for('admin.category_list'))
	return render_template('admin/category/edit.html',
		category = category,
		form = form
	)


@bp_admin.route('/category/<int:cat_id>/destroy/', methods=['GET']) 
@login_required
def category_destroy(cat_id):
	gate.allow(['access_admin_pages'], 403)
	category = db.get_or_404(Category, int(cat_id))
	category.destroy()
	return redirect(url_for('admin.category_list'))
