import json
from flask import render_template, request, flash, url_for, redirect
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
    titles = [('row_number', '序号'), ('name', '产品名称'), ('price', '出厂价格'), ('discount', '折扣(0-1)')]
    products = pagination.items
    return render_template('product/index.html',
                           pagination=pagination,
                           titles=titles,
                           show_type=0,
                           products=products)


@product.route('/search')
@login_required
def product_search():
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    query = Product.query.join(Classify).filter(Classify.name != '积分商城')
    if search:
        query = query.filter(Product.name.like(f'%{search}%') | Product.introduction.like(f'%{search}%'))
    pagination = query.paginate(page=page,per_page=10)
    titles = [('row_number', '序号'), ('name', '产品名称'), ('price', '出厂价格'), ('discount', '折扣(0-1)')]
    products = pagination.items
    view_url = ('product.product_detail', [('classify_id', ':id')])
    edit_url=('product.product_detail', [('product_id', ':id'), ('status', '1')])
    delete_url=('product.product_delete', [('product_id', ':id')])
    return render_template('common/table_contain.html',
                           pagination=pagination,
                           titles=titles,
                           show_type=0,
                           view_url=view_url,
                           edit_url=edit_url,
                           delete_url=delete_url,
                           data=products)



@product.route('/<int:product_id>/detail', methods=['GET', 'POST'])
@product.route('/detail', methods=['GET', 'POST'])
@login_required
def product_detail(product_id=None):
    status = 0
    if product_id is None:
        product = Product()
        status = 2
    else:
        product = Product.query.get(product_id)
        if product is None:
            flash('数据查询失败')
            return redirect(url_for('.index'))
        if request.args.get("status", "0") == "1":
            status = 1
    type = request.args.get("type", "0")
    form = ProductForm(type=type)
    if form.validate_on_submit():
        image1 = form.image1.data
        save_file1 = save_file(image1)
        image2 = form.image2.data
        save_file2 = save_file(image2)
        if status == 1:
            delete_file(product.image1)
            delete_file(product.image2)
        product.image1 = save_file1
        product.image2 = save_file2
        product.name = form.name.data
        product.introduction = form.introduction.data
        product.price = form.price.data
        product.credits = form.credits.data
        product.discount = form.discount.data
        product.classify_id = form.classify.data
        db.session.add(product)
        db.session.commit()
        if type == "0":
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
    return render_template('product/product_edit.html',
                           product=json.dumps(product.to_json(), default=decimal_default),
                           form=form,
                           type=type,
                           status=status)


@product.route('/<int:product_id>/delete', methods=['DELETE'])
@login_required
def product_delete(product_id=None):
    product = Product.query.get(product_id)
    image1 = product.image1
    image2 = product.image2
    delete_file(image1)
    delete_file(image2)
    if product is None:
        flash('数据查询失败')
        return redirect(url_for('.index'))
    db.session.delete(product)
    db.session.commit()
    type = request.args.get("type", "0")
    if type == "0":
        return ok(message="ok", data={'redirect': url_for('.credits')})
    else:
        return ok(message="ok", data={'redirect': url_for('.index')})


@product.route('/credits')
@login_required
def credits():
    page = request.args.get('page', 1, type=int)
    pagination = Product.query.join(Classify).filter(Classify.name == '积分商城').paginate(page=page, per_page=12)
    titles = [('row_number', '序号'), ('name', '产品分类')]
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
    titles = [('row_number', '序号'), ('name', '产品分类'), ('updated_at', '修改时间')]
    classify = pagination.items
    return render_template('product/index.html',
                           pagination=pagination,
                           titles=titles,
                           show_type=2,
                           classify=classify)

@product.route('/classify/search', methods=['GET'])
@login_required
def classify_search():
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    query = Classify.query
    if search:
        query = query.filter(Classify.name.like(f'%{search}%'))
    pagination = query.paginate(page=page, per_page=10)
    titles = [('row_number', '序号'), ('name', '产品分类'), ('updated_at', '修改时间')]
    classify = pagination.items
    view_url = ('product.classify_detail', [('classify_id', ':id')])
    edit_url=('product.classify_detail', [('classify_id', ':id'), ('status', '1')])
    delete_url=('product.classify_delete', [('classify_id', ':id')])
    return render_template('common/table_contain.html',
                           pagination=pagination,
                           titles=titles,
                           show_type=2,
                           view_url=view_url,
                           edit_url=edit_url,
                           delete_url=delete_url,
                           data=classify)


@product.route('/classify/<int:classify_id>/detail', methods=['GET', 'POST', 'DELETE'])
@product.route('/classify/detail', methods=['GET', 'POST'])
@login_required
def classify_detail(classify_id=None):
    status = 0
    if classify_id is None:
        classify = Classify()
        status = 2
    else:
        classify = Classify.query.get(classify_id)
        if classify is None:
            return redirect(url_for('.classify'))
        if request.args.get("status", "0") == "1":
            status = 1
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
    return render_template('product/classify_edit.html',
                           data=classify,
                           form=form,
                           status=status)


@product.route('/classify/<int:classify_id>/delete', methods=['DELETE'])
@login_required
def classify_delete(classify_id):
    classify = Classify.query.get(classify_id)
    if classify is None:
        flash('数据查询失败')
        return redirect(url_for('.classify'))
    db.session.delete(classify)
    db.session.commit()
    return ok(message="ok", data={'redirect': url_for('.classify')})
