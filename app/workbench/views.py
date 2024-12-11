import json
import os
from datetime import datetime

from flask import render_template, send_from_directory, url_for, request, current_app, flash, redirect, jsonify
from flask_ckeditor import upload_success, upload_fail
from werkzeug.utils import secure_filename

from . import workbench
from .forms import TopImageForm, HealthForm
from .. import db
from ..models import TopImage, Health
from ..utils import save_single_file


@workbench.route('/', methods=['GET'])
def index():
    topImages = TopImage.query.all()
    form = TopImageForm()
    titles = [('id', ''), ('type', '类型'), ('image', '图片')]
    return render_template('workbench/index.html',
                           form=form,
                           titles=titles,
                           topImages=topImages,
                           show_top_image=True)


@workbench.route('/<int:top_image_id>/view')
def top_image_view(top_image_id):
    topImage = TopImage.query.get(top_image_id)
    form = TopImageForm()
    if topImage is None:
        flash('数据查询失败')
        return redirect(url_for('.index'))
    form.type.data = topImage.type
    form.image.data = topImage.image
    return render_template('workbench/w_edit_top_image.html',
                           topImage=json.dumps(topImage.to_json()),
                           is_view=True,
                           form=form)


@workbench.route('/<int:top_image_id>/edit', methods=['GET', 'POST'])
def top_image_edit(top_image_id):
    topImage = TopImage.query.get(top_image_id)
    form = TopImageForm()
    if topImage is None:
        flash('数据查询失败')
        return redirect(url_for('.index'))
    if form.validate_on_submit():
        image = form.image.data
        type = form.type.data
        if image:
            save_file = save_single_file(image)
            topImageType = TopImage.query.filter_by(type=type).first()
            if topImageType:
                pre_image = topImageType.image
                if len(pre_image) > 0:
                    os.remove(current_app.config['UPLOAD_FOLDER'] + '/' + pre_image)
                topImageType.image = save_file
                db.session.add(topImageType)
            else:
                topImage = TopImage()
                topImage.image = save_file
                topImage.type = type
                db.session.add(topImageType)
            db.session.commit()
            flash("上传成功!!!")
            return jsonify({'redirect': url_for('.index')})
    elif form.image.errors and form.image.data:
        # 图片未修改
        print(form.errors)
        return jsonify({'redirect': url_for('.index')})
    else:
        print(form.errors)
    form.type.data = topImage.type
    form.image.data = topImage.image
    return render_template('workbench/w_edit_top_image.html',
                           topImage=json.dumps(topImage.to_json()),
                           is_view=False,
                           form=form)


@workbench.route('/health', methods=['GET'])
def health():
    health = Health.query.all()
    form = HealthForm()
    titles = [('id', ''), ('type', '类型'), ('title', '标题'), ('auth', '作者'), ('updateTime', '修改时间')]
    return render_template('workbench/index.html',
                           form=form,
                           titles=titles,
                           health=health,
                           show_top_image=False)


@workbench.route('/<int:health_id>/health_view')
def health_view(health_id):
    health = Health.query.get(health_id)
    form = HealthForm()
    if health is None:
        flash('数据查询失败')
        return redirect(url_for('.index'))
    form.type.data = health.type
    form.title.data = health.title
    form.auth.data = health.auth
    form.body.data = health.body
    form.image.data = health.coverImage
    return render_template('workbench/w_edit_health.html',
                           healthInfo=json.dumps(health.to_json()),
                           status=0,
                           form=form)


@workbench.route('/<int:health_id>/health_edit', methods=['GET', 'POST'])
@workbench.route('/health_edit', methods=['GET', 'POST'])
def health_edit(health_id=None):
    if health_id is None:
        health = Health()
    else:
        health = Health.query.get(health_id)
        if health is None:
            flash('数据查询失败')
            return redirect(url_for('.index'))
    form = HealthForm()
    if form.validate_on_submit():
        image = form.image.data
        # 一个类型只有一项
        type = form.type.data
        if image:
            healthPre = Health.query.filter_by(type=type).first()
            if healthPre:
                pre_image = healthPre.coverImage
                if pre_image is not None and len(pre_image) > 0:
                    os.remove(current_app.config['UPLOAD_FOLDER'] + '/' + pre_image)
            else:
                healthPre = Health()
            save_file = save_single_file(image)
            healthPre.coverImage = save_file
            healthPre.auth = form.auth.data
            healthPre.title = form.title.data
            healthPre.updateTime = datetime.now()
            healthPre.body = form.body.data
            db.session.add(healthPre)
            db.session.commit()
            flash("上传成功!!!")
            # return redirect(url_for('.index', show_top_image=False))
            return jsonify({'redirect': url_for('.health')})
    elif form.image.errors and form.image.data:
        # 图片未修改
        type = form.type.data
        healthPre = Health.query.filter_by(type=type).first()
        healthPre.auth = form.auth.data
        healthPre.title = form.title.data
        healthPre.updateTime = datetime.now()
        healthPre.body = form.body.data
        db.session.add(healthPre)
        db.session.commit()
        return jsonify({'redirect': url_for('.health')})
    else:
        print(form.errors)
    form.type.data = health.type
    form.title.data = health.title
    form.auth.data = health.auth
    form.body.data = health.body
    form.image.data = health.coverImage
    return render_template('workbench/w_edit_health.html',
                           healthInfo=json.dumps(health.to_json()),
                           is_view=False,
                           status=2,  # 0 view 1 edit 2 new
                           form=form)


@workbench.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')  # 获取上传的图片文件对象
    if f:
        extension = f.filename.split('.')[-1].lower()
        if extension not in ['jpg', 'jpeg', 'png', 'gif']:
            return upload_fail(message='仅支持图片!')  # 如果不是图片，返回错误
        # 保存文件
        filename = secure_filename(f.filename)
        f.save(os.path.join('/the/uploaded/directory', filename))
        # 返回上传成功的响应
        url = url_for('uploaded_files', filename=filename)
        return upload_success(url=url)
    return upload_fail(message='No file.py uploaded.')


@workbench.route('/files/<path:filename>')
def uploaded_files(filename):
    path = '/the/uploaded/directory'  # 设置图片保存的目录
    return send_from_directory(path, filename)
