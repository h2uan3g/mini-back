from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

from ..models import Classify


class ProductForm(FlaskForm):
    name = StringField('产品名称：',
                       validators=[DataRequired()],
                       render_kw={'placeholder': u'输入产品名称'})
    introduction = StringField('产品简介：',
                               validators=[DataRequired()],
                               render_kw={'placeholder': u'输入产品简介'})
    price = DecimalField('价格：', validators=[DataRequired()],
                         render_kw={'placeholder': u'输入产品价格'})
    discount = DecimalField('折扣：', validators=[DataRequired()],
                            render_kw={'placeholder': u'输入折扣比例(0-1)'})
    classify = SelectField('产品分类：', coerce=int, validators=[DataRequired()],
                           render_kw={'placeholder': u'选择产品分类'})
    image1 = MultipleFileField('轮播照片(3-5张)：',
                               validators=[FileAllowed(['jpeg', 'jpg', 'png', 'gif'], '只能上传图片'), DataRequired()],
                               render_kw={"style": "border: 1px solid; \
                                          border-color:silver; padding:4px;border-radius:4px;"}
                               )
    image2 = MultipleFileField('简介照片(3-5张)：',
                               validators=[FileAllowed(['jpeg', 'jpg', 'png', 'gif'], '只能上传图片'), DataRequired()],
                               render_kw={"style": "border: 1px solid; \
                                          border-color:silver; padding:4px;border-radius:4px;"}
                               )
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.classify.choices = [(cla.id, cla.name)
                                 for cla in Classify.query.order_by(Classify.name).all()]


class ClassifyForm(FlaskForm):
    name = StringField('产品类别：',
                       validators=[DataRequired()],
                       render_kw={'placeholder': u'输入产品类别'})
    submit = SubmitField('提交')
