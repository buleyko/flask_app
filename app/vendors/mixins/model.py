from flask import (current_app, g,)
from app.extensions import db
from datetime import datetime
from app.extensions import logger
from app.vendors.helpers.config import cfg
from app.vendors.helpers.image import resize_image
from pathlib import Path

__all__ = ('ValidMixin', 'TimestampsMixin',)



class ValidMixin:
	is_blocked = db.Column(
		db.Boolean(0), 
		default=False, 
		nullable=True,
	) 
	is_shown = db.Column(
		db.Boolean(1), 
		default=False, 
		nullable=True,
	)

class TimestampsMixin:
	created_at = db.Column(
		db.DateTime, 
		default=datetime.utcnow, 
		nullable=True,
	) 
	updated_at = db.Column(
		db.DateTime, 
		onupdate=datetime.utcnow, 
		nullable=True,
	)


class ThumbnailMixin:

	@property
	def thumbUrl(self):
		if self.thumb:
			return '{0}/{1}'.format(cfg('UPLOAD_FOLDER'), self.thumb)
		else:
			return cfg('IMAGE_PLACEHOLDER')
	
	@staticmethod
	def resize_thumbnail(image_file, 
			thumb_size = cfg('THUMBNAIL_WIDTH'), 
			file_allowed_exts = cfg('ALLOWED_IMAGE_EXTENSIONS'), 
			ext_path = '',
			file_name = ''
		):
		''' Resize image to thumbnail width, 
			image_file: form.<image_name>.data or request.files[<image_name>] ''' 
		if image_file.filename == '':
			return None
		file_ext = image_file.filename.split('.')[-1]
		if file_ext not in file_allowed_exts:
			return None
		try:
			thumb_path = Path(cfg('UPLOAD_PATH_FOLDER')) / ext_path
			filename = image_file.filename if not file_name else f'{file_name}.{file_ext}'
			img_thumb_path = thumb_path / filename
			image_file.save(img_thumb_path)
			new_thumb = resize_image(img_thumb_path, thumb_size)
			new_thumb.save(img_thumb_path)
			return str(Path(ext_path) / filename)
		except:
			return None


