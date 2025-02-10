from datetime import datetime, timedelta
from flask import app, current_app, render_template
from flask_login import login_required
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
from sqlalchemy import extract, func

from app.models.resouce import News, NewsType
from app.models.user import User
from app.utils.restful import ok
from . import visual
from app import db


@visual.route("/")
@login_required
def index():
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
        data3=c_news.dump_options_with_quotes(),
    )


@visual.route("/customer")
@login_required
def customer():
    now = datetime.now()
    six_months_ago = now - timedelta(days=180)
    result = (
        db.session.query(
            extract("year", User.created_at).label("year"),
            extract("month", User.created_at).label("month"),
            func.count(User.id).label("count"),
        )
        .filter(User.created_at >= six_months_ago)
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )
    data = [
        {"year": item.year, "month": item.month, "count": item.count} for item in result
    ]
    return ok(data=data)


@visual.route("/news")
@login_required
def news():
    result = (
        db.session.query(News, NewsType)
        .join(News, News.newstype_id == NewsType.id)
        .order_by(News.created_at.desc())
        .limit(10)
        .all()
    )

    data = [
        {
            "title": item[0].title,
            "auth": item[0].auth,
            "body": item[0].body,
            "type": item[1].name,
        }
        for item in result
    ]
    return ok(data=data)
