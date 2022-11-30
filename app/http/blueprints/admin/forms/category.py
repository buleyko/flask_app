from flask_wtf import FlaskForm
from app.vendors.helpers.config import cfg
from flask_babel import lazy_gettext as _l 
from flask_babel import _
from app.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check,
)
from wtforms.validators import ( 
	ValidationError, 
	DataRequired, 
	Email, 
	Length, 
)
from wtforms import ( 
	StringField, 
	TextAreaField,
	FileField,
	BooleanField, 
	SelectField,
	SubmitField, 
)


__all__ = ('CreateCategoryForm', 'UpdateCategoryForm',)


class CreateCategoryForm(FlaskForm):
	name = StringField(_(u'Name'),
		validators=[
			DataRequired(_(u'Field is required')), 
		])
	short_desc = TextAreaField(_(u'Short description'))
	thumb = FileField(_(u'Thumbnail'))
	is_blocked = BooleanField(_(u'Blocked'))
	is_shown = BooleanField(_(u'Shown'))
	parent_id = SelectField(_(u'Parent'))
	submit = SubmitField(_(u'Create'))


class UpdateCategoryForm(FlaskForm):
	name = StringField(_(u'Name'),
		validators=[
			DataRequired(_(u'Field is required')), 
		])
	short_desc = TextAreaField(_(u'Short description'))
	thumb = FileField(_(u'Thumbnail'))
	is_blocked = BooleanField(_(u'Blocked'))
	is_shown = BooleanField(_(u'Shown'))
	parent_id = SelectField(_(u'Parent'))
	submit = SubmitField(_(u'Update'))
