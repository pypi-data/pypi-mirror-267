from flask import Flask, request, jsonify
from mysql.connector import Error
from flask_cors import CORS

default_config = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False,
}

# 跨域
def cors(app, resources=None, origins="*", methods=None, allow_headers=None):
    """
    配置Flask应用以允许跨域请求。

    :param app: Flask应用实例。
    :param resources: 一个字典，定义了哪些路由应该允许跨域请求。如果为None，则对所有路由允许跨域请求。
    :param origins: 允许的源。可以是字符串、列表或"*"（表示允许所有源）。
    :param methods: 允许的HTTP方法列表。
    :param allow_headers: 允许的头部信息列表。
    """
    cors_config = {
        "origins": origins,
        "methods": methods,
        "allow_headers": allow_headers
    }
    # 如果未指定resources，应用全局CORS策略
    if resources is None:
        CORS(app, **cors_config)
    else:
        CORS(app, resources=resources, **cors_config)

# 去除空格
def trim(data, key, default = ""):
    value = data.get(key, default)
    if isinstance(value, str):
        return value.strip()
    return value

# 非空校验
def notNull(params):
    """非空校验"""
    if not params:
        raise Error("参数不能为空")
    
# 必须是整数
def isInt(params):
    """必须是整数"""
    if not params or not isinstance(params, int):
        raise Error("参数必须是整数")
    
# 服务
def Service(__name__):
    return Flask(__name__)

# 解析参数
def get_request_data(params="body"):
    if params == "body":
        return request.get_json()
    else:
        return request.args

# 发送数据
def send_data(code=0, msg="数据获取成功。", data=None):
    response_content = {"code": code, "msg": msg}
    if data is not None:
        response_content["data"] = data
    
    status = 200 if code == 0 else code
    return jsonify(response_content), status

# 运行服务
def run(app, config = default_config):
    final_config = {**default_config, **config}
    app.run(**final_config)
