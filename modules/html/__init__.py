from flask_restful import Resource, reqparse
from loguru import logger as l
from flask import Response
from playwright.sync_api import Playwright, sync_playwright
import os
import markdown2
import random

resources = [
    {"name":"markdown","args":"/markdown"},
    {"name":"img","args":"/img"},
]

class markdown(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('markdown',location='form',type=str)
        args = parser.parse_args()
        return {'message': 'success','html':markdown2.markdown(args['markdown'])}

class img(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('html', location='form', type=str)
        args = parser.parse_args()
        html = markdown2.markdown(args['html'])
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content(html)
            fpath = os.path.join(os.getcwd(),"cache","".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=20))+".png")
            page.screenshot(path=fpath)
            browser.close()
        return Response(open(fpath), mimetype="image/png")