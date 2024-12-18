import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename
from wtforms.validators import ValidationError


def save_file(images):
    save_file = ""
    if images:
        if len(images) > 0 and isinstance(images, (list, tuple)):
            for index, image_data in enumerate(images):
                single_file = save_single_file(image_data)
                save_file += single_file
                if index != len(images) - 1:
                    save_file += ','
    return save_file


def delete_file(pre_image):
    if pre_image is not None and len(pre_image) > 0:
        if ',' in pre_image:
            pre_images = pre_image.split(',')
            for img in pre_images:
                os.remove(current_app.config['UPLOAD_FOLDER'] + '/' + img)
        else:
            os.remove(current_app.config['UPLOAD_FOLDER'] + '/' + pre_image)


def save_single_file(file):
    file_name = secure_filename(file.filename)
    if file_name != '':
        file_ext = os.path.splitext(file_name)[1]
        filename = str(uuid.uuid4()) + file_ext
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return filename


def validate_file(form, field):
    if not field.data:
        raise ValidationError('文件为空.')

    for data in field.data:
        # 获取文件的 MIME 类型
        mime_type = data.content_type

        # 检查是否是允许的 MIME 类型
        allowed_mime_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if mime_type not in allowed_mime_types:
            raise ValidationError('仅支持格式JPEG、PNG、GIF')
