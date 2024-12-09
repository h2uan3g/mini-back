import http
import json
import requests
from flask import request, jsonify, current_app

from . import api

base_login_url = 'https://api.weixin.qq.com/sns/jscode2session'
base_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
base_phone_url = 'https://api.weixin.qq.com/wxa/business/getuserphonenumber'


@api.route('/wx/loginByWeixin')
def login_by_weixin():
    code = request.args.get('code')
    appid = current_app.config['WEIXIN_APPID']
    secret = current_app.config['WEIXIN_SECRET']
    r = requests.get(f'{base_login_url}?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code')
    return jsonify({
        'code': http.HTTPStatus.OK,
        'data': r.json(),
        'message': ""
    })


@api.route('/wx/getPhoneNumber')
def get_phone_number():
    code = request.args.get('code')
    token = request.args.get('token')
    payload = {
        "code": code
    }
    appid = current_app.config['WEIXIN_APPID']
    secret = current_app.config['WEIXIN_SECRET']
    token_r = requests.get(f'{base_token_url}?appid={appid}&secret={secret}&grant_type=client_credential')
    token_json = json.loads(token_r.text)
    access_token = token_json['access_token']
    r = requests.post(f'{base_phone_url}?access_token={access_token}', json=payload)
    return jsonify({
        'code': http.HTTPStatus.OK,
        'data': r.json(),
        'message': ""
    })
