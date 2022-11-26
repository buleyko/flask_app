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
)

__all__ = ('category_articles',)




@bp_prime.route('/category/<int:cat_id>/articles/', methods=['GET']) 
def category_articles(cat_id):
	return render_template('prime/category/articles.html')