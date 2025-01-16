import json
import os
from datetime import datetime

from flask import render_template, send_from_directory, url_for, request, current_app, flash, redirect, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.models.resouce import NewsType
from app.utils.file import delete_file

from . import workbench
from .forms import TopImageForm, NewsForm
from .. import db
from ..models import TopImage, News
from ..utils import save_single_file, params_error, ok


@workbench.route('/', methods=['GET'])
@login_required
def index():
    topImages = TopImage.query.all()
    form = TopImageForm()
    titles = [('index', '序号'), ('title', '标题'), ('image', '图片')]
    items_list = [{
                   "index": image.row_number,
                   "id": image.id,
                   "image": url_for('static', filename=f'images/{image.image}', _external=True) if image else "",
                   "title": image.title} for image in topImages]
    return render_template('workbench/index.html',form=form,  titles=titles,topImages=items_list, show_type=0)


@workbench.route('/<int:top_image_id>/detail', methods=['GET', 'POST'])
@workbench.route('/detail', methods=['GET', 'POST'])
@login_required
def top_image_detail(top_image_id=None):
    status = request.args.get('status', '0')
    if status == '2':
        topImage = TopImage()
    else:
        if top_image_id is None:
            flash('数据查询失败')
            return redirect(url_for('.index'))
        topImage = TopImage.query.get(top_image_id)
        if topImage is None:
            flash('数据查询失败')
            return redirect(url_for('.index'))
        
    form = TopImageForm()
    if form.validate_on_submit():
        image = form.image.data
        title = form.title.data
        save_file = save_single_file(image)
        if status == 1:
            pre_image = topImage.image
            delete_file(pre_image)
        topImage.image = save_file
        topImage.title = title
        db.session.add(topImage)
        db.session.commit()
        return ok(data = {'redirect': url_for('.index')})
    elif form.errors:
        return params_error(message=f'{form.errors}')
    form.title.data = topImage.title
    form.image.data = topImage.image
    return render_template('workbench/top_image_edit.html',
                           topImage=json.dumps(topImage.to_json()),
                           status=status,
                           form=form)


@workbench.route('/news', methods=['GET'])
@login_required
def news():
    news = News.query.all()
    form = NewsForm()
    titles = [('id', '序号'), ('type', '类型'), ('title', '标题'), ('auth', '作者'), ('updateTime', '修改时间')]
    type_map = {0: "肝癌", 1: "肺病", 2: "卵巢痣",
                3: "乳腺痛", 4: "食管癌", 5: "肾癌",
                6: "旸癢", 7: "胰腺瘺", 8: "子宫癌",
                9: "前列腺痛", 10: "甲状腺癌", 11: "胃癌"}
    news_list = [
        {"id": heal.id,
         "image": url_for('static', filename=f'images/{heal.coverImage}', _external=True) if heal.coverImage else "",
         "type": type_map[heal.type],
         "auth": heal.auth,
         "isAd": 0,
         "updateTime": heal.updateTime,
         "title": heal.title} for heal in news]
    return render_template('workbench/index.html',
                           form=form,
                           titles=titles,
                           new=news_list,
                           show_type=1)


@workbench.route('/<int:News_id>/News_view')
@login_required
def news_view(news_id):
    News = News.query.get(news_id)
    form = NewsForm()
    if News is None:
        flash('数据查询失败')
        return redirect(url_for('.index'))
    form.type.data = News.type
    form.title.data = News.title
    form.auth.data = News.auth
    form.body.data = News.body
    form.image.data = News.coverImage
    return render_template('workbench/w_edit_News.html',
                           NewsInfo=json.dumps(News.to_json()),
                           status=0,
                           form=form)


@workbench.route('/<int:news_id>/news_edit', methods=['GET', 'POST'])
@workbench.route('/news_edit', methods=['GET', 'POST'])
@login_required
def news_edit(news_id=None):
    if news_id is None:
        News = News()
    else:
        News = News.query.get(news_id)
        if News is None:
            flash('数据查询失败')
            return redirect(url_for('.index'))
    form = NewsForm()
    if form.validate_on_submit():
        image = form.image.data
        # 一个类型只有一项
        type = form.type.data
        if image:
            NewsPre = News.query.filter_by(type=type).first()
            if NewsPre:
                pre_image = NewsPre.coverImage
                if pre_image is not None and len(pre_image) > 0:
                    os.remove(current_app.config['UPLOAD_FOLDER'] + '/' + pre_image)
            else:
                NewsPre = News()
            save_file = save_single_file(image)
            NewsPre.type = type
            NewsPre.coverImage = save_file
            NewsPre.auth = form.auth.data
            NewsPre.title = form.title.data
            NewsPre.updateTime = datetime.now()
            NewsPre.body = form.body.data
            db.session.add(NewsPre)
            db.session.commit()
            return jsonify({'redirect': url_for('.News')})
    elif form.errors:
        return params_error(message=f'{form.errors}')
    form.type.data = News.type
    form.title.data = News.title
    form.auth.data = News.auth
    form.body.data = News.body
    form.image.data = News.coverImage
    return render_template('workbench/news_edit.html',
                           NewsInfo=json.dumps(News.to_json()),
                           is_view=False,
                           status=2,  
                           form=form)


@workbench.route('/newstype', methods=['GET'])
@login_required
def newstype():
    news_types = NewsType.query.all()
    return render_template('workbench/index.html',show_type=2)


@workbench.route('/upload', methods=['POST'])
@login_required
def upload():
    f = request.files.get('upload')
    if f:
        extension = f.filename.split('.')[-1].lower()
        if extension not in ['jpg', 'jpeg', 'png', 'gif']:
            return params_error(message='仅支持图片!')
        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        url = url_for('.uploaded_files', filename=filename)
        return ok(data={'url': url})
    return params_error(message='No file.py uploaded.')


@workbench.route('/files/<path:filename>')
@login_required
def uploaded_files(filename):
    path = os.path.join(current_app.config['UPLOAD_FOLDER'])
    return send_from_directory(path, filename)
