import json
import os
from flask import render_template, request, flash, url_for, redirect, current_app, jsonify
from flask_login import login_required

from . import product
from .. import db
from ..models import Product, Classify
from .forms import ClassifyForm, ProductForm
from ..utils import decimal_default, save_file, delete_file
from ..utils.restful import params_error, ok


@product.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Product.query.join(Classify).filter(Classify.name != '积分商城').paginate(page=page,
                                                                                           per_page=10)
    titles = [('index', '序号'), ('name', '产品名称'), ('price', '出厂价格'), ('discount', '折扣(0-1)')]
    products = pagination.items
    return render_template('product/index.html',
                           pagination=pagination,
                           titles=titles,
                           show_type=0,
                           products=products)


@product.route('/<int:product_id>/view')
@login_required
def product_view(product_id):
    type = int(request.args.get('type'))
    product = Product.query.get(product_id)
    form = ProductForm()
    if product is None:
        flash('数据查询失败')
        return redirect(url_for('.index'))
    form.name.data = product.name
    form.introduction.data = product.introduction
    form.price.data = product.price
    form.discount.data = product.discount
    form.classify.data = product.classify_id
    form.credits.data = product.credits
    form.image1.data = product.image1
    form.image2.data = product.image2
    return render_template('product/p_edit.html',
                           product=json.dumps(product.to_json(), default=decimal_default),
                           is_view=0,
                           type=type,
                           form=form)


@product.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@product.route('/edit', methods=['GET', 'POST'])
@login_required
def product_edit(product_id=None):
    type = int(request.args.get('type'))
    if product_id is None:
        is_view = 2
        product = Product()
    else:
        is_view = 1
        product = Product.query.get(product_id)
        if product is None:
            flash('数据查询失败')
            return redirect(url_for('.index'))
    product.type = type
    form = ProductForm(type=type)
    if form.validate_on_submit():
        image1 = form.image1.data
        save_file1 = save_file(image1)
        delete_file(product.image1)
        product.image1 = save_file1
        image2 = form.image2.data
        save_file2 = save_file(image2)
        delete_file(product.image2)
        product.image2 = save_file2
        product.name = form.name.data
        product.introduction = form.introduction.data
        product.price = form.price.data
        product.credits = form.credits.data
        product.discount = form.discount.data
        product.classify_id = form.classify.data
        db.session.add(product)
        db.session.commit()
        if type == 0:
            return ok(message='ok', data={'redirect': url_for('.credits')})
        else:
            return ok(message='ok', data={'redirect': url_for('.index')})
    elif form.errors:
        return params_error(message=form.errors)
    form.name.data = product.name
    form.introduction.data = product.introduction
    form.price.data = product.price
    form.credits.data = product.credits
    form.discount.data = product.discount
    form.classify.data = product.classify_id
    form.image1.data = product.image1
    form.image2.data = product.image2
    return render_template('product/p_edit.html',
                           product=json.dumps(product.to_json(), default=decimal_default),
                           form=form,
                           type=type,
                           is_view=is_view)


@product.route('/<int:product_id>/delete', methods=['POST'])
@login_required
def product_delete(product_id=None):
    product = Product.query.get(product_id)
    image1 = product.image1
    image2 = product.image2
    if product is None:
        flash('数据查询失败')
        return redirect(url_for('.index'))
    db.session.delete(product)
    db.session.commit()
    # 删除文件
    delete_file(image1)
    delete_file(image2)
    return ok(message="ok", data={'redirect': url_for('.index')})


@product.route('/credits')
@login_required
def credits():
    page = request.args.get('page', 1, type=int)
    pagination = Product.query.join(Classify).filter(Classify.name == '积分商城').paginate(page=page, per_page=12)
    titles = [('index', '序号'), ('name', '产品分类')]
    product = pagination.items
    return render_template('product/index.html',
                           pagination=pagination,
                           titles=titles,
                           show_type=1,
                           product=product)


@product.route('/classify')
@login_required
def classify():
    page = request.args.get('page', 1, type=int)
    pagination = Classify.query.paginate(page=page, per_page=10)
    titles = [('index', '序号'), ('name', '产品分类')]
    classify = pagination.items
    return render_template('product/index.html',
                           pagination=pagination,
                           titles=titles,
                           show_type=2,
                           classify=classify)


@product.route('/classify/<int:classify_id>/view')
@login_required
def classify_view(classify_id):
    classify = Classify.query.get(classify_id)
    form = ClassifyForm()
    if product is None:
        flash('数据查询失败')
    form.name.data = classify.name
    return render_template('product/c_edit.html',
                           classify=classify,
                           form=form,
                           is_view=True)


@product.route('/classify/<int:classify_id>/edit', methods=['GET', 'POST', 'DELETE'])
@product.route('/classify/edit', methods=['GET', 'POST'])
@login_required
def classify_edit(classify_id=None):
    if classify_id is None:
        classify = Classify()
    else:
        classify = Classify.query.get(classify_id)
    form = ClassifyForm()
    if product is None:
        flash('数据查询失败')
        return redirect(url_for('.classify'))
    if form.validate_on_submit():
        classify.name = form.name.data
        db.session.add(classify)
        db.session.commit()
        return redirect(url_for('.classify'))
    form.name.data = classify.name
    return render_template('product/c_edit.html',
                           data=classify,
                           form=form,
                           is_view=False)


@product.route('/classify/<int:classify_id>/delete', methods=['POST'])
@login_required
def classify_delete(classify_id):
    classify = Classify.query.get(classify_id)
    if product is None:
        flash('数据查询失败')
        return redirect(url_for('.classify'))
    db.session.delete(classify)
    db.session.commit()
    return redirect(url_for('.classify'))
