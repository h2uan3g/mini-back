import json
import os
from datetime import datetime

from flask import (
    render_template,
    send_from_directory,
    url_for,
    request,
    current_app,
    flash,
    redirect,
)
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.models.resouce import NewsType
from app.utils.file import delete_file, save_file

from . import workbench
from .forms import NewsTypeForm, TopImageForm, NewsForm
from .. import db
from ..models import TopImage, News
from ..utils import save_single_file, params_error, ok


@workbench.route("/", methods=["GET"])
@login_required
def index():
    topImages = TopImage.query.all()
    form = TopImageForm()
    titles = [("row_number", "序号"), ("title", "标题"), ("image", "图片")]
    items_list = [
        {
            "row_number": image.row_number,
            "id": image.id,
            "image": (
                url_for("static", filename=f"images/{image.image}", _external=True)
                if image
                else ""
            ),
            "title": image.title,
        }
        for image in topImages
    ]
    return render_template(
        "workbench/index.html",
        form=form,
        titles=titles,
        topImages=items_list,
        show_type=0,
    )


@workbench.route("/<int:top_image_id>/detail", methods=["GET", "POST"])
@workbench.route("/detail", methods=["GET", "POST"])
@login_required
def top_image_detail(top_image_id=None):
    status = 0
    if top_image_id == None:
        topImage = TopImage()
        status = 2
    else:
        topImage = TopImage.query.get(top_image_id)
        if topImage is None:
            flash("数据查询失败")
            return redirect(url_for(".index"))
        if request.args.get("status", "0") == "1":
            status = 1
    form = TopImageForm()
    if form.validate_on_submit():
        image = form.image.data 
        image_file = save_file(image, "UPLOAD_FOLDER")
        if status == 1:
            pre_image = topImage.image
            delete_file(pre_image)
        topImage.image = image_file
        topImage.title = form.title.data
        db.session.add(topImage)
        db.session.commit()
        return ok(data={"redirect": url_for(".index")})
    elif form.errors:
        return params_error(message=f"{form.errors}")
    form.title.data = topImage.title
    form.image.data = topImage.image
    return render_template(
        "workbench/top_image_edit.html",
        topImage=json.dumps(topImage.to_json()),
        status=status,
        form=form,
    )


@workbench.route("/<int:top_image_id>/delete", methods=["DELETE"])
@login_required
def top_image_delete(top_image_id):
    top_image = TopImage.query.get(top_image_id)
    if top_image is None:
        return params_error(message="数据查询失败")
    delete_file(top_image.image)
    db.session.delete(top_image)
    db.session.commit()
    return ok(data={"redirect": url_for(".index")})


@workbench.route("/news", methods=["GET"])
@login_required
def news():
    news = News.query.all()
    form = NewsForm()
    titles = [("row_number", "序号"), ("type", "类型"), ("title", "标题"), ("auth", "作者"), ("updated_at", "修改时间")]
    news_list = [
        {
            "row_number": heal.row_number,
            "id": heal.id,
            "image": (
                url_for("static", filename=f"images/{heal.coverImage}", _external=True)
                if heal.coverImage
                else ""
            ),
            "type": NewsType.query.get(heal.newstype_id).name if NewsType.query.get(heal.newstype_id) else "",
            "auth": heal.auth,
            "updated_at": heal.updated_at,
            "title": heal.title,
        }
        for heal in news
    ]
    return render_template(
        "workbench/index.html", form=form, titles=titles, data=news_list, show_type=1
    )


@workbench.route("/news/<int:news_id>/detail", methods=["GET", "POST"])
@workbench.route("/news/detail", methods=["GET", "POST"])
@login_required
def news_detail(news_id=None):
    status = 0
    if news_id is None:
        news = News()
        status = 2
    else:
        news = News.query.get(news_id)
        if news is None:
            flash("数据查询失败")
            return redirect(url_for(".index"))
        if request.args.get("status", "0") == "1":
            status = 1
    form = NewsForm()
    if form.validate_on_submit():
        image = form.image.data
        image_file = save_file(image, "UPLOAD_FOLDER")
        if status == 1:
            pre_image = news.coverImage
            delete_file(pre_image)
        news.coverImage = image_file
        news.newstype_id = form.type.data
        news.auth = form.auth.data
        news.title = form.title.data
        news.updated_at = datetime.now()
        news.body = form.body.data
        db.session.add(news)
        db.session.commit()
        return ok(data={"redirect": url_for(".news")})
    elif form.errors:
        return params_error(message=f"{form.errors}")
    form.type.data = news.newstype_id
    form.title.data = news.title
    form.auth.data = news.auth
    form.body.data = news.body
    form.image.data = news.coverImage
    return render_template(
        "workbench/news_edit.html",
        status=status,
        form=form,
        newsInfo = json.dumps(news.to_json())
    )


@workbench.route("/news/<int:news_id>/delete", methods=["DELETE"])
def news_delete(news_id):
    news = News.query.get(news_id)
    if news is None:
        return params_error(message="数据查询失败")
    delete_file(news.coverImage)
    db.session.delete(news)
    db.session.commit()
    return ok(data={"redirect": url_for(".news")})


@workbench.route("/newstype", methods=["GET"])
@login_required
def newstype():
    page = request.args.get("page", 1, type=int)
    pagination = NewsType.query.paginate(
        page=page,
        per_page=current_app.config["FLASKY_COMMENTS_PER_PAGE"],
        error_out=False,
    )
    news_types = pagination.items
    titles = [("row_number", "序号"), ("name", "新闻分类")]
    return render_template(
        "workbench/index.html", show_type=2, titles=titles, data=news_types
    )


@workbench.route("/newstype/<int:newstype_id>/detail", methods=["GET", "POST"])
@workbench.route("/newstype/detail", methods=["GET", "POST"])
@login_required
def newstype_detail(newstype_id=None):
    status = request.args.get("status", "0")
    if status == "2":
        newstype = NewsType()
    else:
        if newstype_id is None:
            flash("数据查询失败")
            return redirect(url_for(".newstype"))
        newstype = NewsType.query.get(newstype_id)
        if newstype is None:
            flash("数据查询失败")
            return redirect(url_for(".newstype"))
    form = NewsTypeForm()
    if form.validate_on_submit():
        name = form.name.data
        newstype.name = name
        if NewsType.query.filter_by(name=name).first():
            flash("新闻分类已存在")
        else:
            db.session.add(newstype)
            db.session.commit()
            return redirect(url_for(".newstype"))
    elif form.errors:
        return params_error(message=f"{form.errors}")
    form.name.data = newstype.name
    return render_template(
        "workbench/newstype_edit.html", show_type=2, status=int(status), form=form
    )


@workbench.route("/newstype/<int:newstype_id>/delete", methods=["DELETE"])
@login_required
def newstype_delete(newstype_id):
    newstype = NewsType.query.get(newstype_id)
    if newstype is None:
        return params_error(message="数据查询失败")
    db.session.delete(newstype)
    db.session.commit()
    return ok(data={"redirect": url_for(".newstype")})


@workbench.route("/upload", methods=["POST"])
@login_required
def upload():
    f = request.files.get("upload")
    if f:
        extension = f.filename.split(".")[-1].lower()
        if extension not in ["jpg", "jpeg", "png", "gif"]:
            return params_error(message="仅支持图片!")
        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        url = url_for(".uploaded_files", filename=filename)
        return ok(data={"url": url})
    return params_error(message="No file.py uploaded.")


@workbench.route("/files/<path:filename>")
@login_required
def uploaded_files(filename):
    path = os.path.join(current_app.config["UPLOAD_FOLDER"])
    return send_from_directory(path, filename)
