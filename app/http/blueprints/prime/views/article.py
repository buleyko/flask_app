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

__all__ = ('article_item',)




@bp_prime.route('/article/<int:art_id>/item/', methods=['GET']) 
def article_item(art_id):
	return render_template('prime/article/item.html')