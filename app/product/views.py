from flask import render_template, request, flash, url_for, redirect

from . import product
from .. import db
from ..models import Product, Classify
from .forms import ClassifyForm, ProductForm


@product.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Product.query.paginate(page=page, per_page=10)
    titles = [('id', ''), ('name', '产品名称'), ('price', '出厂价格'), ('discount', '折扣(0-1)')]
    products = pagination.items
    return render_template('product/index.html',
                           pagination=pagination,
                           titles=titles,
                           show_classify=False,
                           products=products)


@product.route('/<int:product_id>/view')
def product_view(product_id):
    product = Product.query.get(product_id)
    form = ProductForm()
    if product is None:
        flash('数据查询失败')
        return redirect(url_for('.index'))
    form.name.data = product.name
    form.introduction.data = product.introduction
    form.price.data = product.price
    form.discount.data = product.discount
    form.image1.data = product.image1
    form.image2.data = product.image2
    return render_template('product/p_edit.html',
                           product=product,
                           is_view=True,
                           form=form)


@product.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@product.route('/edit', methods=['GET', 'POST'])
def product_edit(product_id=None):
    if product_id is None:
        product = Product()
    else:
        product = Product.query.get(product_id)
        if product is None:
            flash('数据查询失败')
            return redirect(url_for('.index'))
    form = ProductForm()
    form.name.data = product.name
    form.introduction.data = product.introduction
    form.price.data = product.price
    form.discount.data = product.discount
    form.image1.data = product.image1
    form.image2.data = product.image2
    if form.validate_on_submit():
        product.name = form.name.data
        product.introduction = form.price.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.image1 = form.image1.data
        product.image2 = form.image2.data
        return redirect(url_for('.index'))
    return render_template('product/p_edit.html',
                           product=product,
                           form=form,
                           is_view=False)


@product.route('/<int:product_id>/delete', methods=['POST'])
def product_delete(product_id=None):
    product = Product.query.get(product_id)
    if product is None:
        flash('数据查询失败')
    return render_template('product/p_edit.html', product=product)


@product.route('/classify')
def classify():
    page = request.args.get('page', 1, type=int)
    pagination = Classify.query.paginate(page=page, per_page=10)
    titles = [('index', '序号'), ('name', '产品分类')]
    classify = pagination.items
    return render_template('product/index.html',
                           pagination=pagination,
                           titles=titles,
                           show_classify=True,
                           classify=classify)


@product.route('/classify/<int:classify_id>/view')
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
def classify_delete(classify_id):
    classify = Classify.query.get(classify_id)
    if product is None:
        flash('数据查询失败')
        return redirect(url_for('.classify'))
    db.session.delete(classify)
    db.session.commit()
    return redirect(url_for('.classify'))
