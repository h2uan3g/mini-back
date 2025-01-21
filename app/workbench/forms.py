from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_wtf.form import _Auto
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired

from app.models.resouce import NewsType


class TopImageForm(FlaskForm):
    title = StringField(
        "标题：",
        validators=[DataRequired()],
        default=0,
    )

    image = FileField(
        "照片：",
        validators=[
            FileAllowed(["jpeg", "jpg", "png", "gif"], "只能上传图片"),
            DataRequired(),
        ],
        render_kw={
            "style": "border: 1px solid; \
                                      border-color:silver; padding:4px;border-radius:4px;"
        },
    )

    submit = SubmitField("提交")


class NewsForm(FlaskForm):
    type = SelectField(
        "分类：",
        validators=[DataRequired()],
    )
    title = StringField(
        "标题：", validators=[DataRequired()], render_kw={"placeholder": "输入标题名称"}
    )
    auth = StringField(
        "作者：", validators=[DataRequired()], render_kw={"placeholder": "输入作者名称"}
    )
    image = FileField(
        "封面：",
        validators=[
            FileAllowed(["jpeg", "jpg", "png", "gif"], "只能上传图片"),
            DataRequired(),
        ],
        render_kw={
            "style": "border: 1px solid; \
                                          border-color:silver; padding:4px;border-radius:4px;"
        },
    )
    body = TextAreaField("正文：")
    cancle = SubmitField("取 消")
    submit = SubmitField("提 交")

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.type.choices = [(type.id, type.name) for type in NewsType.query.all()]


class NewsTypeForm(FlaskForm):
    name = StringField(
        "名称：", validators=[DataRequired()], render_kw={"placeholder": "输入名称"}
    )
    cancle = SubmitField("取 消")
    submit = SubmitField("保 存")
