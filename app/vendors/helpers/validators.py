import re
from flask_babel import lazy_gettext as _l 
from flask_babel import _


__all__ = (
	'email_validation_check',
	'passwd_validation_check',
	'birthdate_validation_check',
	'phone_validation_check',
	'required_check',
	'max_len_check',
	'min_len_check',
	'unique_check',
)



# letter, number or symbol (.-_)
email_regex = re.compile(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$')

def email_validation_check(email, regex=email_regex):
	if re.fullmatch(regex, email) is None:
		return False
	return True



# At least one letter, number or symbol (@$!%*#?&). Min 8 max 16.
passwd_regex = re.compile(r'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*\d)(?=.*?[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$')
# for test only
passwd_regex = re.compile(r'^[ 0-9]+$')
# -------------
def passwd_validation_check(passwd, regex=passwd_regex):
	if re.fullmatch(regex, passwd) is None:
		return False
	return True


# for test only
birthdate_regex = re.compile(r'^[ 0-9]+$')
# -------------
def birthdate_validation_check(date, regex=birthdate_regex):
	if re.fullmatch(regex, date) is None:
		return False
	return True


# for test only
phone_regex = re.compile(r'^[ 0-9]+$')
# -------------
def phone_validation_check(phone, regex=phone_regex):
	if re.fullmatch(regex, phone) is None:
		return False
	return True



def required_check(val, *args, **kwargs):
	if not val:
		return False
	return True

def max_len_check(val, *args, **kwargs):
	if len(val) > int(args[0]):
		return False
	return True

def min_len_check(val, *args, **kwargs):
	if len(val) < int(args[0]):
		return False
	return True

def unique_check(val, *args, **kwargs):
	if not val:
		return False
	return True