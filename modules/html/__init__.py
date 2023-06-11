from flask_restful import Resource, reqparse
from loguru import logger as l
from playwright.sync_api import Playwright, sync_playwright
import os
import mistletoe
import random
import base64
from PIL import Image
import io

resources = [
    {"name":"markdown","args":"/markdown"},
    {"name":"img","args":"/img"},
]

class markdown(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('markdown',location='form',type=str)
        args = parser.parse_args()
        return {'message': 'success','html':mistletoe.markdown(args['markdown'])}

class img(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('html', location='form', type=str)
        parser.add_argument('github-markdown', location='form', type=str)
        parser.add_argument('timeout', location='form', type=str)
        args = parser.parse_args()
        args['html'] = args['html'].replace("\\n","")
        try:
            args['timeout'] = int(args['timeout'])
        except:
            pass
        if args['github-markdown'] is None:
            html = args['html']
        else:
            html = open("modules/html/github-markdown-template.html").read().replace("%markdown%",args['html'])
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content(html)
            fpath = os.path.join(os.getcwd(),"cache","".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=20))+".png")
            if args['github-markdown'] is None:
                page.screenshot(path=fpath,full_page=True,timeout=args['timeout'])
            else:
                element_handle = page.query_selector("//article[@id='md']")
                element_handle.screenshot(path=fpath,timeout=args['timeout'])
            browser.close()
        img = Image.open(fpath)
        rawBytes = io.BytesIO()
        img.save(rawBytes, "PNG")
        rawBytes.seek(0)
        return {"message":"success","image_base64":base64.b64encode(rawBytes.read()).decode()}