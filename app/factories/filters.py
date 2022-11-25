from app.vendors.helpers.filters import (
	by_lang_or_def_filter,
	reverse_filter,
)

__all__ = ('registration_filters',)


def registration_filters(
		app,
		by_lang_or_def_filter = by_lang_or_def_filter,
		reverse_filter = reverse_filter,
	): 
	""" configuration template filters """
	app.jinja_env.filters['by_lang_or_def'] = by_lang_or_def_filter
	app.jinja_env.filters['reverse'] = reverse_filter