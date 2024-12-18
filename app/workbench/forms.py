from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.choices import RadioField, SelectField
from wtforms.fields.simple import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired


class TopImageForm(FlaskForm):
    type = RadioField('栏目：',
                      choices=[
                          (0, '癌症知识'),
                          (1, '企业文化'),
                          (2, '医疗场景'),
                      ],
                      validators=[DataRequired()],
                      default=0, )

    image = FileField('照片：',
                      validators=[FileAllowed(['jpeg', 'jpg', 'png', 'gif'], '只能上传图片'), DataRequired()],
                      render_kw={"style": "border: 1px solid; \
                                      border-color:silver; padding:4px;border-radius:4px;"}
                      )

    submit = SubmitField('提交')


class HealthForm(FlaskForm):
    type = SelectField('分类：',
                       choices=[
                           (0, '肝癌'),
                           (1, '肺病'),
                           (2, '卵巢痣'),
                           (3, '乳腺痛'),
                           (4, '食管癌'),
                           (5, '肾癌'),
                           (6, '旸癢'),
                           (7, '胰腺瘺'),
                           (8, '子宫癌'),
                           (9, '前列腺痛'),
                           (10, '甲状腺癌'),
                           (11, '胃癌'),
                       ],
                       validators=[DataRequired()], )
    title = StringField('标题：',
                        validators=[DataRequired()],
                        render_kw={'placeholder': u'输入标题名称'})
    auth = StringField('作者：',
                       validators=[DataRequired()],
                       render_kw={'placeholder': u'输入作者名称'})
    image = FileField('封面：',
                      validators=[FileAllowed(['jpeg', 'jpg', 'png', 'gif'], '只能上传图片'), DataRequired()],
                      render_kw={"style": "border: 1px solid; \
                                          border-color:silver; padding:4px;border-radius:4px;"}
                      )
    body = TextAreaField('正文：')
    submit = SubmitField('提交')
