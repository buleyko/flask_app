from six import text_type

def check_user_token(user, token):
	# check user token
	return True

def get_user_uid_token(user):
	# generate - uid by id and token by user.id timestamp user.is_active
	uid = 1
	token = '1q2w3e4r5t'
	return {'uid': uid, 'token':token}
