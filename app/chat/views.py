from flask import current_app, render_template, request
from flask_login import login_required
from openai import OpenAI

from app.utils.restful import ok, params_error
from . import chat


@chat.route('/')
@login_required
def index():
    return render_template('chat/index.html')


@chat.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    if not data:
        return params_error(message='请求参数错误')
    message = data.get('message')
    client = OpenAI(api_key=current_app.config['DEEPSEEK_APIKEY'], base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "user", "content": message},
        ],
        stream=False
    )
    html_content = response.choices[0].message.content
    return ok(data=html_content)