from flask import render_template, flash, request, url_for, redirect, session, make_response
from flask_login import login_required, login_user, logout_user, current_user
from io import BytesIO
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User
from ..utils import generate_image


@auth.route('/image')
def get_image():
    image, code = generate_image(4)
    buffer = BytesIO()
    image.save(buffer, 'jpeg')
    buf_bytes = buffer.getvalue()
    session['valid'] = code
    response = make_response(buf_bytes)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form.remember_me.data = True
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('用户名或密码错误')
    elif form.errors:
        flash(f'{form.errors}')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('退出成功!')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
