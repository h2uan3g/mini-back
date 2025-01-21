from wtforms import Field
from wtforms.widgets import html_params


# 自定义按钮字段
class ButtonGroupWidget(object):
    def __call__(self, field, **kwargs):
        buttons = []
        for value, item_kw in field.choices:
            button = f'<button class="btn btn-sm btn-bottom {item_kw[1]}" type={value} name={value}>{item_kw[0]}</button>'
            buttons.append(button)
        return f'<div class="btn-group float-end mt-3">{ " ".join(buttons)}</div>'


class ButtonGroupField(Field):
    widget = ButtonGroupWidget()

    def __init__(self, label=None, validators=None, choices=None, **kwargs):
        super(ButtonGroupField, self).__init__(label, validators, **kwargs)
        self.choices = choices or []
