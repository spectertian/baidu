from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from json import dumps
import hashlib

from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.exceptions import NotFoundError

cluster = Cluster('couchbase://127.0.0.1')
authenticator = PasswordAuthenticator('admin', 'admin123')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('beer-sample')

# md5加密
def getMd5(s):
    md = hashlib.md5()
    md.update(s.encode('utf-8'))
    return md.hexdigest()

# 获取值
def getInfoByKey(key):
    key = 'baidu_' + key
    try:
        result = cb.get(key)
        return result.value
    except NotFoundError as e:
        return ''


# 保存值
def setInfo(key, value):
    key = 'baidu' + key
    return cb.upsert(key, value)


app = Flask(__name__)
api = Api(app)

# 添加任务
class addTask(Resource):
    def post(self):
        rp = reqparse.RequestParser()
        rp.add_argument('tqm', required=True)
        rp.add_argument('url', required=True)
        args = rp.parse_args()
        key = getMd5(args.url)
        value = {'url': args.url, 'tqm': args.tqm, 'path': '', 'process': 0, 'status': 0}
        setInfo(key, value)
        return {'task_id': key}


# 获取任务信息
class getTaskInfoById(Resource):
    def get(self, task_id):
        result = getInfoByKey(task_id)
        return jsonify(result)


# 删除任务
class removeTaskById(Resource):
    def get(self, task_id):
        result = getInfoByKey(task_id)
        return jsonify(result)


class getPathById(Resource):
    def get(self, task_id):
        result = getInfoByKey(task_id)
        return jsonify(result)


api.add_resource(addTask, '/addTask')  # 添加任务
api.add_resource(getTaskInfoById, '/getTaskInfoById/<task_id>')  # 根据任务ID获取详细任务信息
api.add_resource(removeTaskById, '/removeTaskById/<task_id>')  # 根据任务ID删除任务
api.add_resource(getPathById, '/getPathById/<task_id>')  # 根据任务ID获取任务文件路径

if __name__ == '__main__':
    app.run(port='5000', debug=True)
