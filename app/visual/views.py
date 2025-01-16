from datetime import datetime
import os
from flask import app, current_app, flash, json, redirect, render_template, request, send_from_directory, url_for
from flask_login import login_required
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from app.models.document import Document
from app.utils.file import add_image_watermark_docx, add_image_watermark_pdf, convert_word_to_html, convert_word_to_pdf, save_file
from app.utils.numbers import decimal_default
from app.utils.restful import ok, params_error
from app.visual.forms import DocumentForm
from ..utils import decimal_default, save_file, delete_file
from . import visual
from .. import db


@visual.route("/chart")
@login_required
def chart():
    c_product = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("销售量", [5, 20, 36, 10, 75, 90], color="#754ffe")
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
            color="#754ffe",
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="近一个月注册用户"))
    )
    return render_template(
        "visual/idnex.html",
        data1=c_product.dump_options_with_quotes(),
        data2=c_customer.dump_options_with_quotes(),
    )


@visual.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    pagination = Document.query.paginate(page=page, per_page=10)
    titles = [
        ("index", "序号"),
        ("title", "标题"),
        ("update_time", "更新时间"),
    ]
    docs_orgin = pagination.items
    docs = [
        {
            "id": doc.id,
            "title": doc.title,
            "update_time": doc.update_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for doc in docs_orgin
    ]
    return render_template(
        "visual/index.html", pagination=pagination, titles=titles, docs=docs
    )


@visual.route("/<int:visual_id>/detail", methods=["GET", "POST"])
@visual.route("/detail", methods=["GET", "POST"])
@login_required
def visual_view(visual_id=None):
    status = 0  
    if visual_id is None:
        document = Document()
        status = 2
    else:
        document = Document.query.get(visual_id)
        if document is None:
            flash("数据查询失败")
            return redirect(url_for(".index"))
    form = DocumentForm()
    if document is None:
        flash("数据查询失败")
        return redirect(url_for(".index"))
    if form.validate_on_submit():
        form.title.data = form.title.data
        source = form.source.data
        watermark = form.watermark.data
        source_file = save_file(source, "UPLOAD_FOLDER_DOCS")
        watermark_file = save_file(watermark, "UPLOAD_FOLDER")
        # 处理水印
        if len(source) > 0:
            if source[0].filename.endswith("pdf"):
                out_file = add_image_watermark_pdf(source_file, watermark_file) 
            else:
                out_file = add_image_watermark_docx(source_file, watermark_file)
        else:
            return params_error(message="请上传文件")
        document.title = form.title.data
        document.create_time = datetime.now()
        document.update_time = datetime.now()
        document.source_url = url_for(
            "static", filename=f"docs/{source_file}", _external=True
        )
        document.water_url = url_for(
            "static", filename=f"docs/{watermark_file}", _external=True
        )
        document.result_url = out_file
        db.session.add(document)
        db.session.commit()
        return ok(
            message="ok", data={"result": out_file, "redirect": url_for(".index")}
        )
    elif form.errors:
        flash(f"请检查输入:", form.errors)
        return params_error(message=form.errors)

    form.title.data = document.title
    return render_template(
        "visual/v_edit.html",
        document=json.dumps(document.to_json(), default=decimal_default),
        status=status,
        type=type,
        form=form,
    )


@visual.route('/result/<filename>')
@login_required
def visual_result(filename):
    content = convert_word_to_html(filename)
    return ok(message="ok", data=content)

@visual.route('/delete/<int:visual_id>', methods=['POST'])
@login_required
def visual_delete(visual_id):
    document = Document.query.get(visual_id)
    if document is None:
        return params_error(message="数据查询失败")
    if document.result_url is not None:
        result_file_name = document.result_url.split("/")[-1]
        delete_file(result_file_name, "UPLOAD_FOLDER_DOCS")
    if document.source_url is not None:
        source_file_name = document.source_url.split("/")[-1]
        delete_file(source_file_name, "UPLOAD_FOLDER_DOCS")
    if document.water_url is not None:
        water_file_name = document.water_url.split("/")[-1]
        delete_file(water_file_name)
    db.session.delete(document)
    db.session.commit()
    return redirect(url_for(".index"))
