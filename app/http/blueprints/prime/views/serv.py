from flask import (request, redirect, session, jsonify, g)
from app.http.blueprints.prime import bp_prime
from app.vendors.helpers.config import cfg


__all__ = ('change_locale', 'options', 'article_image_upload',)



@bp_prime.route('/change-locale/<lang>/', methods=['GET'])
def change_locale(lang):
	session['current_language'] = lang
	return redirect(request.referrer)


@bp_prime.route('/options/', methods=['POST']) 
def options():
	return jsonify({'success':'Stub: change application settings'})


@bp_prime.route('/search/', methods=['POST'])
def search():
	session.pop('search_name', default=None)
	if search_value := request.form.get('search_name', None):
		session['search_name'] = search_value
		# g.search = search_value
	return redirect(request.referrer)


from app.models import Article
@bp_prime.route('/upload-article-image/', methods=['POST']) 
def article_image_upload():
	image_path = Article.upload_body_image(request.files['image'])
	print(image_path)
	return jsonify({'img':image_path})