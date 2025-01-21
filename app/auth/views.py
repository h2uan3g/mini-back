from flask import (
    render_template,
    flash,
    request,
    url_for,
    redirect,
    session,
    make_response,
    current_app,
)
from flask_login import login_required, login_user, logout_user, current_user
from io import BytesIO
from . import auth
from .forms import LoginForm, RegistrationForm, EditProfileForm, EditProfileAdminForm
from .. import db
from ..decorators import admin_required, permission_required
from ..models import User, Role, Permission
from ..utils import generate_image


@auth.route("/image")
def get_image():
    image, code = generate_image(4)
    buffer = BytesIO()
    image.save(buffer, "jpeg")
    buf_bytes = buffer.getvalue()
    session["valid"] = code
    response = make_response(buf_bytes)
    response.headers["Content-Type"] = "image/jpeg"
    return response


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if (
            not current_user.confirmed
            and request.endpoint
            and request.blueprint != "auth"
            and request.endpoint != "static"
        ):
            return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account. Thanks!")
    else:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("main.index"))


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    flash("A new confirmation email has been sent to you by email.")
    return redirect(url_for("main.index"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    form.remember_me.data = True
    if form.validate_on_submit():
        if "@" in form.email.data:
            user = User.query.filter_by(email=form.email.data).first()
        else:
            user = User.query.filter_by(username=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("用户名或密码错误")
    elif form.errors:
        flash(f"{form.errors}")
    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("退出成功!")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
            about_me=form.about_me.data,
            location=form.location.data,
            confirmed=True,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash("修改成功.")
        return redirect(url_for("main.index"))
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.avatar.data = current_user.gravatar()
    status = 0
    if current_user.is_administrator():
        status = 1
    return render_template("auth/profile.html", form=form, status=status)


@auth.route("/follow/<username>")
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user.")
        return redirect(url_for(".index"))
    if current_user.is_following(user):
        flash("You are already following this user.")
        return redirect(url_for(".user", username=username))
    current_user.follow(user)
    db.session.commit()
    flash("You are now following %s." % username)
    return redirect(url_for(".user", username=username))


@auth.route("/followers/<username>")
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user.")
        return redirect(url_for(".index"))
    page = request.args.get("page", 1, type=int)
    pagination = user.followers.paginate(
        page=page,
        per_page=current_app.config["FLASKY_FOLLOWERS_PER_PAGE"],
        error_out=False,
    )
    follows = [
        {"user": item.follower, "timestamp": item.timestamp}
        for item in pagination.items
    ]
    return render_template(
        "followers.html",
        user=user,
        title="Followers of",
        endpoint=".followers",
        pagination=pagination,
        follows=follows,
    )


@auth.route("/unfollow/<username>")
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user.")
        return redirect(url_for(".index"))
    if not current_user.is_following(user):
        flash("You are not following this user.")
        return redirect(url_for(".user", username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash("You are not following %s anymore." % username)
    return redirect(url_for(".user", username=username))


@auth.route("/followed_by/<username>")
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user.")
        return redirect(url_for(".index"))
    page = request.args.get("page", 1, type=int)
    pagination = user.followed.paginate(
        page=page,
        per_page=current_app.config["FLASKY_FOLLOWERS_PER_PAGE"],
        error_out=False,
    )
    follows = [
        {"user": item.followed, "timestamp": item.timestamp}
        for item in pagination.items
    ]
    return render_template(
        "followers.html",
        user=user,
        title="Followed by",
        endpoint=".followed_by",
        pagination=pagination,
        follows=follows,
    )


@auth.route("/customer")
@login_required
def customer():
    page = request.args.get("page", 1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config["FLASKY_COMMENTS_PER_PAGE"],
        error_out=False,
    )
    users = pagination.items
    titles = [
        ("row_number", "序号"),
        ("username", "昵称"),
        ("avatar_hash", "头像"),
        ("last_seen", "最近登录时间"),
    ]
    return render_template(
        "customer/customer.html", titles=titles, users=users, pagination=pagination
    )


@auth.route("/customer/<int:user_id>/view")
@login_required
def customer_view(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = EditProfileForm()
    if user is None:
        return render_template("404.html")
    form.username.data = user.username
    form.email.data = user.email
    form.location.data = user.location
    form.about_me.data = user.about_me
    form.avatar.data = user.gravatar()
    status = 0
    if user.id == current_user.id:
        status = 1
    return render_template(
        "customer/customer_edit.html", status=status, form=form, user=user
    )


@auth.route("/customer/<int:user_id>/view", methods=["GET", "POST"])
@login_required
def customer_edit(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = EditProfileForm()
    if user is None:
        return render_template("404.html")
    if form.validate_on_submit():
        if "cancle" in request.form:
            # 取消
            return redirect(url_for(".customer"))
        elif "submit" in request.form:
            user.username = form.username.data
            user.email = form.email.data
            user.location = form.location.data
            user.about_me = form.about_me.data
            db.session.add(user)
            db.session.commit()
            return redirect(url_for(".customer"))
    form.username.data = user.username
    form.email.data = user.email
    form.location.data = user.location
    form.about_me.data = user.about_me
    form.avatar.data = user.gravatar()
    status = 0
    if user.id == current_user.id:
        status = 1
    return render_template(
        "customer/customer_edit.html", status=status, form=form, user=user
    )
