from flask import render_template
from flask_login import login_required
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie
from . import visual


@visual.route("/")
@login_required
def index():
    c_customer = (
        Line()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axislabel_opts=opts.LabelOpts(color="#fff", font_size=10),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#fff")
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axislabel_opts=opts.LabelOpts(color="#fff"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#fff")
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .add_xaxis(xaxis_data=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        .add_yaxis(
            series_name="",
            y_axis=[820, 932, 901, 934, 1290, 1330, 1320],
            symbol="emptyCircle",
            is_symbol_show=True,
            color="#2F51E9",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    c_product = (
        Bar()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(color="#fff", interval=0, font_size=10),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#fff")
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(color="#fff"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#fff")
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .add_xaxis(xaxis_data=["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("销售量", [5, 20, 36, 10, 75, 90], color="#2F51E9")
    )
    x_data = ["直接访问", "邮件营销", "联盟广告", "视频广告", "搜索引擎"]
    y_data = [335, 310, 274, 235, 400]
    data_pair = [list(z) for z in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1])
    c_news = (
        Pie(init_opts=opts.InitOpts())
        .add(
            series_name="访问来源",
            data_pair=data_pair,
            rosetype="radius",
            radius="55%",
            center=["50%", "50%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Customized Pie",
                pos_left="center",
                pos_top="20",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            label_opts=opts.LabelOpts(color="rgba(255, 255, 255, 0.3)"),
        )
    )

    return render_template(
        "visual/index.html",
        data1=c_product.dump_options_with_quotes(),
        data2=c_customer.dump_options_with_quotes(),
        data3=c_news.dump_options_with_quotes(),
    )
