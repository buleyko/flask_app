from app.extensions import celery
from flask_mail import Message


def tasks_configure(app, celery=celery): 

	@celery.task
	def send_mail_task(arg1, arg2):
		# some long running task here
		res = arg1 * arg2
		return res



	@celery.task
	def send_async_email(email_data):
		"""Background task to send an email with Flask-Mail."""
		msg = Message(
			email_data['subject'],
			sender=None,# app.config['MAIL_DEFAULT_SENDER'],
			recipients=[email_data['to']]
		)
		msg.body = email_data['body']
		# mail.send(msg)
		with app.app_context():
			mail.send(msg)