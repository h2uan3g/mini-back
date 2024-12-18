from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from sqlalchemy import not_
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired

from ..models import Classify
from ..utils import validate_file


class ProductForm(FlaskForm):
    name = StringField('产品名称：',
                       validators=[DataRequired()],
                       render_kw={'placeholder': u'输入产品名称'})
    introduction = StringField('产品简介：',
                               validators=[DataRequired()],
                               render_kw={'placeholder': u'输入产品简介'})
    price = DecimalField('价格(元)：', validators=[InputRequired()],
                         render_kw={'placeholder': u'输入产品价格'})
    credits = DecimalField('积分(豆)：', validators=[InputRequired()],
                           render_kw={'placeholder': u'输入积分数'})
    discount = DecimalField('折扣(0-1)：', validators=[InputRequired()],
                            render_kw={'placeholder': u'输入折扣比例(0-1)'})
    classify = SelectField('产品分类：', coerce=int, validators=[InputRequired()],
                           render_kw={'placeholder': u'选择产品分类'})
    image1 = MultipleFileField('轮播照片(3-5张)：',
                               validators=[validate_file],
                               render_kw={"style": "border: 1px solid; \
                                          border-color:silver; padding:4px;border-radius:4px;"}
                               )
    image2 = MultipleFileField('简介照片(3-5张)：',
                               validators=[validate_file],
                               render_kw={"style": "border: 1px solid; \
                                          border-color:silver; padding:4px;border-radius:4px;"}
                               )
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if kwargs.get('type') == 0:
            self.classify.choices = [(cla.id, cla.name)
                                     for cla in
                                     Classify.query.filter(Classify.name == '积分商城').order_by(Classify.name).all()]
        else:
            self.classify.choices = [(cla.id, cla.name)
                                     for cla in
                                     Classify.query.filter(Classify.name != '积分商城').order_by(Classify.name).all()]


class ClassifyForm(FlaskForm):
    name = StringField('产品类别：',
                       validators=[DataRequired()],
                       render_kw={'placeholder': u'输入产品类别'})
    submit = SubmitField('提交')
