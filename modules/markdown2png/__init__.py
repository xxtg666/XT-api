from flask_restful import Resource
from loguru import logger as l

resources = [
    {"name":"main","args":""},
]

class main(Resource):
    def get(self):
        return {'message': 'success'}