from flask import render_template
from flask_login import login_required
from pyecharts import options as opts
from pyecharts.charts import Bar, Line

from . import visual


@visual.route('/')
@login_required
def index():
    c_product = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("销售量", [5, 20, 36, 10, 75, 90], color='#754ffe')
        .set_global_opts(title_opts=opts.TitleOpts(title="近一个月销售Top6"))
    )
    c_customer = (
        Line()
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
        .add_xaxis(xaxis_data=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        .add_yaxis(
            series_name="",
            y_axis=[820, 932, 901, 934, 1290, 1330, 1320],
            symbol="emptyCircle",
            is_symbol_show=True,
            color='#754ffe',
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="近一个月注册用户"))
    )
    return render_template('visual.html',
                           data1=c_product.dump_options_with_quotes(),
                           data2=c_customer.dump_options_with_quotes())
