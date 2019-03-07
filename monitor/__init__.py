#-*- coding:utf-8 -*-
# author:liyan
# datetime:2019/3/4 17:53

from flask import jsonify
from flask import request
from flask import Blueprint
from flask import render_template
from monitor.logic import Logic

monitor=Blueprint('monitor',__name__)

@monitor.route('/index')
def index():
    return render_template("monitor/index.html")

@monitor.route('api/v1/search')
def api_v1_search():
    data=request.values.to_dict()
    if 'ip' not in data:
        return jsonify({
            'status':400,
            'message':'request need "ip" parameter!',
            'data': data
        })
    try:
        runner=Logic()
        result=runner.search(data)





