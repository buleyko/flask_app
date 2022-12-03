# from flask import (current_app, g,)
# import smtplib, ssl
# from email.mime.text import MIMEText
# from app.extensions import celery
# from app.vendors.helpers.config import cfg



# @celery.task
# def send_async_email(email_data):
# 	# sender = email_data['sender']
# 	# receivers = email_data['receivers']
# 	# msg = email_data['text']

# 	# if cfg('MAIL_USE_SSL'):
# 	# 	try:
# 	# 		context = ssl.create_default_context()
# 	# 		with smtplib.SMTP_SSL(cfg('MAIL_SERVER'), cfg('MAIL_PORT'), context=context) as server:
# 	# 			server.login(cfg('MAIL_USERNAME'), cfg('MAIL_PASSWORD'))
# 	# 			server.sendmail(sender, receivers, msg.as_string())
# 	# 	except Exception as e: 
# 	# 		print(e)
# 	# if cfg('MAIL_USE_TLS'):
# 	# 	try:
# 	# 		context = ssl.create_default_context()
# 	# 		with smtplib.SMTP(cfg('MAIL_SERVER'), cfg('MAIL_PORT')) as server:
# 	# 			server.ehlo()
# 	# 			server.starttls(context=context)
# 	# 			server.ehlo()
# 	# 			server.login(cfg('MAIL_USERNAME'), cfg('MAIL_PASSWORD'))
# 	# 			server.sendmail(sender, receivers, msg.as_string())
# 	# 	except Exception as e: 
# 	# 		print(e)
# 	# 	finally:
# 	# 		server.quit() 

# 	# sender = 'admin@example.com'
# 	# receivers = ['info@example.com']

# 	port = 1025
# 	msg = MIMEText('This is test mail')

# 	msg['Subject'] = 'Test mail'
# 	msg['From'] = 'admin@example.com'
# 	msg['To'] = 'info@example.com'

# 	with smtplib.SMTP('localhost', port) as server:
# 		# server.login('username', 'password')
# 		server.sendmail(sender, receivers, msg.as_string())
# 		print("Successfully sent email")

 
