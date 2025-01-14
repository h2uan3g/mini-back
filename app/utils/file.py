import os
import uuid
from docx import Document
from docx.shared import Inches
from flask import current_app, url_for
from werkzeug.utils import secure_filename
from wtforms.validators import ValidationError



def save_file(images, pathname="UPLOAD_FOLDER"):
    save_file = ""
    if images:
        if len(images) > 0 and isinstance(images, (list, tuple)):
            for index, image_data in enumerate(images):
                single_file = save_single_file(image_data, pathname)
                save_file += single_file
                if index != len(images) - 1:
                    save_file += ","
        else:
            save_file = save_single_file(images, pathname)
    return save_file


def delete_file(pre_image):
    if pre_image is not None and len(pre_image) > 0:
        if "," in pre_image:
            pre_images = pre_image.split(",")
            for img in pre_images:
                os.remove(current_app.config["UPLOAD_FOLDER"] + "/" + img)
        else:
            os.remove(current_app.config["UPLOAD_FOLDER"] + "/" + pre_image)


def save_single_file(file, basepath='UPLOAD_FOLDER'):
    file_name = secure_filename(file.filename)
    if file_name != "":
        file_ext = os.path.splitext(file_name)[1]
        filename = str(uuid.uuid4()) + file_ext
        file.save(os.path.join(current_app.config[basepath], filename))
        return filename


def validate_file(form, field):
    if not field.data:
        raise ValidationError("文件为空.")

    for data in field.data:
        # 获取文件的 MIME 类型
        mime_type = data.content_type

        # 检查是否是允许的 MIME 类型
        allowed_mime_types = ["image/jpeg", "image/jpg", "image/png", "image/gif"]
        if mime_type not in allowed_mime_types:
            raise ValidationError("仅支持格式JPEG、PNG、GIF")


def add_image_watermark_docx(source_file, watermark_file, target_text="签名"):
    doc = Document(os.path.join(current_app.config["UPLOAD_FOLDER_DOCS"], source_file))
    image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], watermark_file)
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            print(run.text)
            if target_text in run.text:
                run.text = run.text.replace(target_text, f"{target_text}\n")
                paragraph.add_run("\t")
                run_cell = paragraph.add_run()
                run_cell.add_picture(image_path, width=Inches(0.9), height=Inches(0.8))
    out_file = f"{source_file}-sign.docx"
    doc.save(os.path.join(current_app.config["UPLOAD_FOLDER_DOCS"], out_file))
    return url_for("static", filename=f"docs/{out_file}", _external=True)
