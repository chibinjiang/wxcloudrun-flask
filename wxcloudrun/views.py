import json
import logging
import requests
from datetime import datetime
from flask import render_template, request, Response
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
ichiban_domain = "http://43.138.187.204"
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def post_request(path, data, ip=''):
    logger.info(f"{path}: {data}")
    resp = requests.post(
        f"{ichiban_domain}{path}",
        json=data,
        headers={'Client-IP': ip}
    )
    resp_j = resp.json()
    logger.info(f"{path}: {resp_j}")
    return Response(json.dumps(resp_j), mimetype='application/json')


@app.route('/api/ping')
def ping():
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
    resp = requests.post(
        f"{ichiban_domain}/api/oss/aliyun_upload",
        files={'file': (filename, file)}
    )
    resp_j = resp.json()
    print(f"/oss/aliyun_upload: {resp_j}")
    logger.info(f"/oss/aliyun_upload: {resp_j}")
    return Response(json.dumps(resp_j), mimetype='application/json')


@app.route('/api/search/product', methods=["POST"])
def search_product_wrap():
    # 获取请求体参数
    data = request.get_json()
    return post_request(
        '/api/search/product', data, request.remote_addr
    )


@app.route('/api/search/ocr', methods=["POST"])
def ocr_wrap():
    # 获取请求体参数
    data = request.get_json()
    return post_request(
        '/api/search/ocr', data, request.remote_addr
    )


@app.route('/api/search/keywords', methods=["POST"])
def get_gds_keywords():
    # 获取请求体参数
    data = request.get_json()
    return post_request(
        '/api/search/keywords', data, request.remote_addr
    )


@app.route('/api/scan/', methods=["POST"])
def scan_wrap():
    data = request.get_json()
    return post_request(
        '/api/scan/', data, request.remote_addr
    )


@app.route('/api/auth/wx_login', methods=["POST"])
def wx_login_wrap():
    data = request.get_json()
    return post_request(
        '/api/auth/wx_login', data, request.remote_addr
    )


@app.route('/api/user/profile', methods=["POST"])
def update_user_wrap():
    data = request.get_json()
    return post_request(
        '/api/user/profile', data, request.remote_addr
    )


@app.route('/api/history/hot', methods=["POST"])
def get_most_popular_products_wrap():
    data = request.get_json()
    return post_request(
        "/api/history/hot", data, request.remote_addr
    )


@app.route('/api/history/scan/list', methods=["POST"])
def get_scan_code_history_wrap():
    data = request.get_json()
    return post_request(
        "/api/history/scan/list", data, request.remote_addr
    )


@app.route('/api/history/gds/record', methods=["POST"])
def save_gds_product_wrap():
    data = request.get_json()
    return post_request(
        "/api/history/gds/record", data, request.remote_addr
    )


@app.route('/api/history/scan/record', methods=["POST"])
def update_scan_code_history_wrap():
    data = request.get_json()
    return post_request(
        "/api/history/scan/record", data, request.remote_addr
    )


@app.route('/api/history/product/list', methods=["POST"])
def get_product_view_history_history_wrap():
    data = request.get_json()
    return post_request(
        "/api/history/product/list", data, request.remote_addr
    )


@app.route('/api/history/product/view', methods=["POST"])
def update_product_view_history_wrap():
    data = request.get_json()
    return post_request(
        "/api/history/product/view", data, request.remote_addr
    )


@app.route('/api/generator/base64', methods=["POST"])
def generate_code_image():
    data = request.get_json()
    return post_request(
        "/api/generator/base64", data, request.remote_addr
    )


@app.route('/api/unit/transform', methods=["POST"])
def transform_unit():
    data = request.get_json()
    return post_request(
        "/api/unit/transform", data, request.remote_addr
    )


@app.route('/api/unit/list', methods=["POST"])
def get_unit_list():
    data = request.get_json()
    return post_request(
        "/api/unit/list", data, request.remote_addr
    )


@app.route('/express/feeling/list', methods=["POST"])
def get_feelings():
    data = request.get_json()
    return post_request(
        "/express/feeling/list", data, request.remote_addr
    )


@app.route('/express/feeling/express', methods=["POST"])
def express_feeling():
    data = request.get_json()
    return post_request(
        "/express/feeling/express", data, request.remote_addr
    )


@app.route('/express/feeling/labels', methods=["POST"])
def get_labels():
    data = request.get_json()
    return post_request(
        "/express/feeling/labels", data, request.remote_addr
    )


@app.route('/express/feeling/continue', methods=["POST"])
def continue_express_feeling():
    data = request.get_json()
    return post_request(
        "/express/feeling/continue", data, request.remote_addr
    )


@app.route('/express/answer/random', methods=["POST"])
def get_book_of_answer():
    data = request.get_json()
    return post_request(
        "/express/answer/random", data, request.remote_addr
    )


@app.route('/express/record/list', methods=["POST"])
def get_user_records():
    data = request.get_json()
    return post_request(
        "/express/record/list", data, request.remote_addr
    )


@app.route('/express/record/user_do', methods=["POST"])
def record_user_action():
    data = request.get_json()
    return post_request(
        "/express/record/user_do", data, request.remote_addr
    )


@app.route('/lvya/callback', methods=["POST"])
def get_lvya_callback():
    data = request.get_json()
    print(f"绿芽参数: {data}")
    logger.info(f"绿芽参数: {data}")
    return post_request(
        "/express/lvya/callback", data, request.remote_addr
    )
