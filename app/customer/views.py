from flask import render_template

from . import customer


@customer.route('/')
def index():
    return render_template('customer.html')