import json
import requests
from datetime import datetime
from flask import render_template, request, Response
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
# My Domain
ichiban_domain = "http://116.62.70.115"


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
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


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.route('/api/oss/aliyun_upload', methods=['POST'])
def aliyun_upload_wrap():
    """
    :return: 计数的值
    """
    file = request.files['file']
    resp = requests.post(f"{ichiban_domain}/api/oss/aliyun_upload", files={'file': file})
    resp_j = resp.json()
    print(f"/api/oss/aliyun_upload: {resp_j}")
    return Response(json.dumps(resp_j), mimetype='application/json')


@app.route('/api/search/', methods=['POST'])
def search_wrap():
    """
    :return: 计数的值
    """
    # 获取请求体参数
    params = request.get_json()
    code = params['code']
    resp = requests.post(f"{ichiban_domain}/api/search/", json={'code': code})
    resp_j = resp.json()
    print(f"/api/search/: {resp_j}")
    return Response(json.dumps(resp_j), mimetype='application/json')


@app.route('/api/scan/', methods=['POST'])
def scan_wrap():
    """
    :return: 计数的值
    """
    # 获取请求体参数
    params = request.get_json()
    url = params['url']
    resp = requests.post(f"{ichiban_domain}/api/scan/", json={'url': url})
    resp_j = resp.json()
    print(f"/api/scan/: {resp_j}")
    return Response(json.dumps(resp_j), mimetype='application/json')
