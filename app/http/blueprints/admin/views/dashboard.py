from flask import render_template
from app.http.blueprints.admin import bp_admin
from flask_login import login_required
from app.vendors.utils.gate import gate

__all__ = ('dashboard',)


@bp_admin.route('/dashboard/', methods=['GET']) 
@login_required
def dashboard():
	gate.allow(['access_admin_pages'], 403)
	return render_template('admin/dashboard.html')