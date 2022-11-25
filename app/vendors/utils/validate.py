from flask import request, g
from collections import namedtuple
from flask_babel import lazy_gettext as _l 
from flask_babel import _
from app.vendors.helpers import validators

__all__ = ('validate',)

Validator = namedtuple('Validator' , 'check message')

validators = {
	'required': Validator(validators.required_check, u'Required field %s'),
	'max':      Validator(validators.max_len_check,  u'Too big %s'),
	'min':      Validator(validators.min_len_check,  u'Too small %s'),
	'unique':   Validator(validators.unique_check,   u'Not unique %s'),
}


def validity_check(value, validator_keychain):
	validator_keys = validator_keychain.split('|')
	validation_errors = []
	for handler_key in validator_keys:
		name, *params = handler_key.split(':')

		if validator := validators.get(name, False):
			if validator.check(value, *params) == False:
				msg = _l(validator.message % ','.join(params))
				validation_errors.append(msg)
		else:
			raise KeyError(f'Validator with name {name} not exist')

	return validation_errors



def validate():
	''' validate date { 'key': 'required|max:80'}'''
	def _validate():
		pass 


	def post(key_validators={}, validators=validators):
		'''
		{
			'name': 'required|min:4|max:16',
			'short_desc': 'required|min:10|max:200',
			'count': 'required|int|int_min:50',
			'images:file:array': 'array_required|array_min:2|required|file_exts:jpg:png',
		}
		'''
		form_values = {}
		form_validation_errors = {}
		is_valid = True

		# request.files.get(key)
		# request.files.getitems('key')

		for key, validator_keychain in key_validators.items():
			key, *postf = key.split(':')

			# if 'file' in key:
			# 	value = request.files.get(key, None)

			value = request.form.get(key, None);

			if value:
				# if isinstance(ini_list1, list):

				validation_errors = validity_check(value=value, validator_keychain=validator_keychain)
				if validation_errors:
					is_valid = False
				form_values[key] = value
				form_validation_errors[key] = validation_errors

				# validator_keys = validator_keychain.split('|')
				# validation_errors = []
				# for handler_key in validator_keys:
				# 	name, *params = handler_key.split(':')

				# 	if validator := validators.get(name, False):
				# 		if validator.check(value, *params) == False:
				# 			msg = _l(validator.message % ','.join(params))
				# 			validation_errors.append(msg)
				# 			is_valid = False
				# 	else:
				# 		raise KeyError(f'Validator with name {name} not exist')

				# form_values[key] = value
				# form_validation_errors[key] = validation_errors

			else:
				raise KeyError(f'Data with name {key} in request post not exist')
		
		if not is_valid:
			g.old = form_values
			g.old_errors = form_validation_errors
		return is_valid



	# def post(key_validators={}, validators=validators):
	# 	form_old_values = {}
	# 	form_validation_errors = {}
	# 	is_valid = True

	# 	# request.files[key]

	# 	for key, validator_keychain in key_validators.items():
	# 		if value := request.form.get(key, None):
	# 			validator_keys = validator_keychain.split('|')
	# 			validation_errors = []
	# 			for handler_key in validator_keys:
	# 				name, *params = handler_key.split(':')
	# 				if validator := validators.get(name, False):
	# 					if validator.check(value, *params) == False:
	# 						msg = _l(validator.message % ','.join(params))
	# 						validation_errors.append(msg)
	# 						is_valid = False
	# 				else:
	# 					raise KeyError(f'Validator with name {name} not exist')
	# 			form_old_values[key] = value
	# 			form_validation_errors[key] = validation_errors
	# 		else:
	# 			raise KeyError(f'Data with name {key} in request post not exist')
		
	# 	if not is_valid:
	# 		g.old = form_old_values
	# 		g.form_errors = form_validation_errors
	# 	return is_valid


	# def get(key_validators={}, validators=validators):
	# 	if request.args.get(key, False):
	# 		pass

	# def json(key_validators={}, validators=validators):
	# 	if request.json.get(key, False):
	# 		pass


	_validate.post = post
	# _validate.get = get
	# _validate.json = json
	return _validate



'''
def fact_gen(num):
    if num == 1:
        fact = 1
    else:
        i = yield from fact_gen(num - 1)
        fact = num * i
    yield fact
    return fact


f = fact_gen(3)

next(f)
Источник: https://egorovegor.ru/python-generators
'''

