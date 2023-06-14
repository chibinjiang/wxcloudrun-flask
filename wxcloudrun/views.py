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
logger = logging.getLogger(__name__)


@app.route('/')
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


@app.route('/api/ping')
def ping():
    """
    :return: 返回index页面
    """
    resp = requests.get(f"{ichiban_domain}/api/system/ping")
    return make_succ_response(resp.text)


@app.route('/api/count', methods=["POST"])
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


@app.route('/api/count', methods=["POST"])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.route('/api/oss/aliyun_upload', methods=["POST"])
def aliyun_upload_wrap():
    logger.info(f"request.files: {request.files}")
    file = request.files['file']
    filename = file.filename
    resp = requests.post(f"{ichiban_domain}/api/oss/aliyun_upload", files={'file': (filename, file)})
    resp_j = resp.json()
    print(f"/oss/aliyun_upload: {resp_j}")
    logger.info(f"/oss/aliyun_upload: {resp_j}")
    return Response(json.dumps(resp_j), mimetype='application/json')


@app.route('/api/search/product', methods=["POST"])
def search_product_wrap():
    # 获取请求体参数
    data = request.get_json()
    return post_request('/api/search/product', data)


@app.route('/api/search/ocr', methods=["POST"])
def ocr_wrap():
    # 获取请求体参数
    data = request.get_json()
    return post_request('/api/search/ocr', data)


@app.route('/api/scan/', methods=["POST"])
def scan_wrap():
    data = request.get_json()
    return post_request('/api/scan/', data)


@app.route('/api/auth/wx_login', methods=["POST"])
def wx_login_wrap():
    data = request.get_json()
    return post_request('/api/auth/wx_login', data)


@app.route('/api/user/profile', methods=["POST"])
def update_user_wrap():
    data = request.get_json()
    return post_request('/api/user/profile', data)


@app.route('/api/history/hot', methods=["GET"])
def get_most_popular_products_wrap():
    data = request.get_json()
    return post_request("/api/history/hot", data)


@app.route('/api/history/scan/list', methods=["POST"])
def get_scan_code_history_wrap():
    data = request.get_json()
    return post_request("/api/history/scan/list", data)


@app.route('/api/history/scan/record', methods=["POST"])
def update_scan_code_history_wrap():
    data = request.get_json()
    return post_request("/api/history/scan/record", data)


@app.route('/api/history/product/list', methods=["POST"])
def get_product_view_history_history_wrap():
    data = request.get_json()
    return post_request("/api/history/product/list", data)


@app.route('/api/history/product/view', methods=["POST"])
def update_product_view_history_wrap():
    data = request.get_json()
    return post_request("/api/history/product/view", data)


@app.route('/api/generator/base64', methods=["POST"])
def generate_code_image():
    data = request.get_json()
    return post_request("/api/generator/base64", data)
