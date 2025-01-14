from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from app.utils.file import validate_file


class DocumentForm(FlaskForm):
    title = StringField(
        "名称：", validators=[DataRequired()], render_kw={"placeholder": "输入名称"}
    )
    source = MultipleFileField(
        "源文件：",
        validators=[
            DataRequired(),
            FileAllowed(["docx", "pdf"], "限制文件类型docx和pdf!"),
        ],
        render_kw={
            "style": "border: 1px solid; border-color:silver; padding:4px;border-radius:4px;"
        },
    )

    watermark = MultipleFileField(
        "水印文件：",
        validators=[validate_file],
        render_kw={
            "style": "border: 1px solid; border-color:silver; padding:4px;border-radius:4px;"
        },
    )
