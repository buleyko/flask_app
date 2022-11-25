from flask import g

__all__ = ('get_json_by_lang', 'set_json_by_lang',)



def get_json_by_lang(val):
	dict_val = val
	lang_value = dict_val.get(g.current_language, None)
	return lang_value if lang_value is not None else dict_val.get('def', None)


def set_json_by_lang(val, v):
	dict_val = val
	if dict_val is None:
		dict_val = {'def': v}
		dict_val[g.current_language] = v
	else:
		dict_val[g.current_language] = v
	return dict_val