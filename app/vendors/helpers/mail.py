from flask import request
from email.mime.text import MIMEText
from app.vendors.helpers.config import cfg



def get_mail_body(user, mail_data, html_template=None):
	msg = MIMEText('This is test mail')
	msg['Subject'] = mail_data['subject']
	msg['From'] = mail_data['sender']
	msg['To'] = mail_data['to']
	msg['registration_link'] = f'{request.url}{get_user_uid_token(user)}'
	return msg


def get_register_mail(user, html_template=None):
	subject = 'register subject'
	mail_data = {
		'sender': cfg('MAIL_DEFAULT_SENDER'),
		'receivers': [user.email],
		'subject': subject,
	}
	mail_data['text'] = get_mail_body(user, mail_data, html_template)
	return mail_data