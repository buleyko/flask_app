from flask import g


__all__ = ('injects_context', )



def injects_context(app):
	# Add Curent User In Jinja2 Context (In Templates)
	@app.context_processor
	def inject_old():
		try:
			return { 
				'old': g.old, 
				'old_errors': g.old_errors
			}
		except AttributeError:
			return { 
				'old': None, 
				'old_errors': None,
			}