from flask import (request, redirect, session, jsonify,)
from app.http.blueprints.prime import bp_prime
from app.vendors.helpers.config import cfg
from app.tasks import long_task

__all__ = ('change_locale', 'options',)



@bp_prime.route('/change-locale/<lang>/', methods=['GET'])
def change_locale(lang):
	session['current_language'] = lang
	return redirect(request.referrer)


@bp_prime.route('/options/', methods=['POST']) 
def options():
	return jsonify({'q':1000})


@bp_prime.route('/longtask', methods=['POST'])
def longtask():
	task = long_task.apply_async()
	return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@bp_prime.route('/status/<task_id>')
def taskstatus(task_id):
	task = long_task.AsyncResult(task_id)
	if task.state == 'PENDING':
		# job did not start yet
		response = {
			'state': task.state,
			'current': 0,
			'total': 1,
			'status': 'Pending...'
		}
	elif task.state != 'FAILURE':
		response = {
			'state': task.state,
			'current': task.info.get('current', 0),
			'total': task.info.get('total', 1),
			'status': task.info.get('status', '')
		}
		if 'result' in task.info:
			response['result'] = task.info['result']
	else:
		# something went wrong in the background job
		response = {
			'state': task.state,
			'current': 1,
			'total': 1,
			'status': str(task.info),  # this is the exception raised
		}
	return jsonify(response)