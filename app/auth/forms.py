from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('用户名：',
                        validators=[DataRequired(), Length(1, 64)],
                        render_kw={'placeholder': u'输入用户名或邮箱'})
    password = PasswordField('账户密码：', validators=[DataRequired()],
                             render_kw={'placeholder': u'输入密码'})
    code = StringField('验证码：',
                       validators=[DataRequired()],
                       render_kw={'placeholder': u'输入验证码'})
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登 录')

    def validate_code(self, data):
        input_code = data.data
        code = session.get('valid')
        if input_code.lower() != code.lower():  # 判断输入的验证码
            raise ValidationError('验证码错误')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64)])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '用户名格式错误额')])
    password = PasswordField('密码', validators=[
        DataRequired(), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注 册',
                         render_kw={"style": "width: 100%;"})

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('用户名:', validators=[Length(0, 64)])
    location = StringField('地址:', validators=[Length(0, 64)])
    email = StringField('邮箱:', validators=[Length(0, 64)])
    avatar = StringField('头像:')
    about_me = TextAreaField('用户详情:')
    submit = SubmitField('保存')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
