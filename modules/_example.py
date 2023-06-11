from flask_restful import Resource
import json
from loguru import logger as l

# 需要不同数量的"/"分隔参数时，使用<参数名>作为参数占位符，并添加多条resources，否则会not found
resources = [
    {"name": "main", "args": ""},
    {"name": "main_arg1", "args": "/<arg1>"},
    {"name": "main_arg2", "args": "/<arg1>/<arg2>"},
]


class main(Resource):
    def get(self):
        e = json.load(open("config/example.json"))
        return {'message': 'success', 'example': e["example"]}


class main_arg1(Resource):
    def get(self, arg1):
        return {'message': 'success', 'arg1': arg1}


class main_arg2(Resource):
    def get(self, arg1, arg2):
        return {'message': 'success', 'arg1': arg1, 'arg2': arg2}
