from datetime import datetime, timedelta
from flask import app, current_app, render_template
from flask_login import login_required
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
from sqlalchemy import extract, func

from app.models.product import Classify, Product
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


    return render_template(
        "visual/index.html",
        data1=c_product.dump_options_with_quotes(),
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


@visual.route("/classify")
@login_required
def classify():
    query = (
        db.session.query(
            Classify.name.label("classify_name"),
            func.count(Product.id).label("product_count"),
        )
        .join(Product)
        .group_by(Classify.name)
    )
    results = query.all()
    data = [
        {"name": item.classify_name, "value": item.product_count}
        for item in results
    ]
    return ok(data=data)
