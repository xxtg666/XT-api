from flask_restful import Resource, reqparse
from cnocr import CnOcr
import base64
import random

resources = [
    {"name": "ocr", "args": ""},
]

o = CnOcr()
class ocr(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("img_base64", location='form', type=str)
        args = parser.parse_args()
        img_bytes = base64.b64decode(args["img_base64"])
        fn = "cache/"+"".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=20))+".png"
        open(fn, "wb").write(img_bytes)
        text =  [i['text'] for i in o.ocr(fn)]
        return {'message': 'success', 'text': text}