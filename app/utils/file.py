import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


def save_single_file(file):
    filename = secure_filename(file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        filename = str(uuid.uuid4()) + file_ext
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return filename
