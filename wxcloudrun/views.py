import json
import logging
import requests
from datetime import datetime
from flask import render_template, request, Response
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
# My Domain
ichiban_domain = "http://116.62.70.115"
# ichiban_domain = "http://0.0.0.0:8000"
logger = logging.getLogger(__name__)


@app.get('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


def post_request(path, data):
    logger.info(f"{path}: {data}")
    resp = requests.post(f"{ichiban_domain}{path}", json=data)
    resp_j = resp.json()
    logger.info(f"{path}: {resp_j}")
    return Response(json.dumps(resp_j), mimetype='application/json')


@app.get('/api/ping')
def ping():
    """
    :return: 返回index页面
    """
    resp = requests.get(f"{ichiban_domain}/api/system/ping")
    return make_succ_response(resp.text)


@app.post('/api/count')
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.get('/api/count')
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.post('/api/oss/aliyun_upload')
def aliyun_upload_wrap():
    """
    :return: 计数的值
    """
    logger.info(f"request.files: {request.files}")
    file = request.files['file']
    filename = file.filename
    resp = requests.post(f"{ichiban_domain}/api/oss/aliyun_upload", files={'file': (filename, file)})
    resp_j = resp.json()
    print(f"/oss/aliyun_upload: {resp_j}")
    logger.info(f"/oss/aliyun_upload: {resp_j}")
    return Response(json.dumps(resp_j), mimetype='application/json')


@app.post('/api/search/')
def search_wrap():
    """
    :return: 计数的值
    """
    # 获取请求体参数
    data = request.get_json()
    return post_request('/api/search/', data)


@app.post('/api/scan/')
def scan_wrap():
    """
    :return: 计数的值
    """
    # 获取请求体参数
    data = request.get_json()
    return post_request('/api/scan/', data)


@app.post('/api/auth/wx_login')
def wx_login_wrap():
    # 获取请求体参数
    data = request.get_json()
    return post_request('/api/auth/wx_login', data)


@app.post('/api/user/profile')
def update_user_wrap():
    # 获取请求体参数
    data = request.get_json()
    return post_request('/api/user/profile', data)


@app.post('/api/scan/record')
def update_user_wrap():
    # 获取请求体参数
    data = request.get_json()
    return post_request("/api/scan/record", data)


@app.post('/api/scan/history')
def update_user_wrap():
    # 获取请求体参数
    data = request.get_json()
    return post_request('/api/scan/history', data)