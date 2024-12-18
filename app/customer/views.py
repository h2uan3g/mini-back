from flask import render_template, current_app, request

from . import customer
from ..auth.forms import RegistrationForm
from ..models import User


@customer.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(
        page=page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    titles = [('index', '序号'), ('username', '昵称'), ('avatar_hash', '头像')]
    return render_template('customer/customer.html',
                           titles=titles,
                           users=users,
                           pagination=pagination)


@customer.route('/<int:user_id>/view')
def view(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = RegistrationForm()
    if user is None:
        return render_template('404.html')
    form.username = user.username
    form.email = user.email
    return render_template('customer/customer_edit.html',
                           is_view=0,
                           form=form)
