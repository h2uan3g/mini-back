from datetime import datetime
import json
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.document.forms import DocumentForm
from app.models import Document
from app.utils.file import (
    add_image_watermark_docx,
    add_image_watermark_pdf,
    convert_word_to_html,
    delete_file,
    save_file,
)
from app.utils.numbers import decimal_default
from app.utils.restful import ok, params_error

from .. import db
from . import doc


@doc.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    pagination = Document.query.paginate(page=page, per_page=10)
    titles = [("row_number", "序号"), ("title", "标题"), ("updated_at", "更新时间")]
    docs_orgin = pagination.items
    docs = [
        {
            "row_number": doc.row_number,
            "id": doc.id,
            "title": doc.title,
            "updated_at": doc.updated_at,
        }
        for doc in docs_orgin
    ]
    return render_template(
        "document/index.html", pagination=pagination, titles=titles, docs=docs
    )


@doc.route("/<int:doc_id>/detail", methods=["GET", "POST"])
@doc.route("/detail", methods=["GET", "POST"])
@login_required
def doc_view(doc_id=None):
    status = 0
    if doc_id is None:
        document = Document()
        status = 2
    else:
        document = Document.query.get(doc_id)
        if document is None:
            flash("数据查询失败")
            return redirect(url_for(".index"))
        if request.args.get("status", "0") == "1":
            status = 1
    form = DocumentForm()
    if form.validate_on_submit():
        source = form.source.data
        watermark = form.watermark.data
        source_file = save_file(source, "UPLOAD_FOLDER_DOCS")
        watermark_file = save_file(watermark, "UPLOAD_FOLDER")
        # 处理水印
        if len(source) > 0:
            if source[0].filename.endswith("pdf"):
                out_file = add_image_watermark_pdf(source_file, watermark_file)
            else:
                out_file = add_image_watermark_docx(source_file, watermark_file)
        else:
            return params_error(message="请上传文件")
        document.title = form.title.data
        document.create_time = datetime.now()
        document.update_time = datetime.now()
        document.source_url = url_for(
            "static", filename=f"docs/{source_file}", _external=True
        )
        document.water_url = url_for(
            "static", filename=f"docs/{watermark_file}", _external=True
        )
        document.result_url = out_file
        db.session.add(document)
        db.session.commit()
        return ok(
            message="ok", data={"result": out_file, "redirect": url_for(".index")}
        )
    elif form.errors:
        flash(f"请检查输入:", form.errors)
        return params_error(message=form.errors)

    form.title.data = document.title
    return render_template(
        "document/d_edit.html",
        document=json.dumps(document.to_json()),
        status=status,
        type=type,
        form=form,
    )


@doc.route("/result/<filename>")
@login_required
def doc_result(filename):
    content = convert_word_to_html(filename)
    return ok(message="ok", data=content)


@doc.route("/delete/<int:doc_id>", methods=["DELETE"])
@login_required
def doc_delete(doc_id):
    document = Document.query.get(doc_id)
    if document is None:
        return params_error(message="数据查询失败")
    if document.result_url is not None:
        result_file_name = document.result_url.split("/")[-1]
        delete_file(result_file_name, "UPLOAD_FOLDER_DOCS")
    if document.source_url is not None:
        source_file_name = document.source_url.split("/")[-1]
        delete_file(source_file_name, "UPLOAD_FOLDER_DOCS")
    if document.water_url is not None:
        water_file_name = document.water_url.split("/")[-1]
        delete_file(water_file_name)
    db.session.delete(document)
    db.session.commit()
    return ok(message="ok", data={"redirect": url_for(".index")})
