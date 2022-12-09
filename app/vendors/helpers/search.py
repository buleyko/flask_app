

def get_search_arguments(request):
	search_arguments = []
	if request.args:
		for key, val in request.args:
			search_arguments = [*search_arguments, *val]
	return search_arguments


def post_search_arguments(request):
	pass
	# request.form.get