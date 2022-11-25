
__all__ = ('by_lang_or_def_filter', 'reverse_filter',)


def by_lang_or_def_filter(val, lang):
    res = val.get(str(lang), None)
    if res is None:
    	res = val.get('def', None)
    return res


def reverse_filter(val):
    return val[::-1]