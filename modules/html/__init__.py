from flask_restful import Resource, reqparse
from playwright.sync_api import sync_playwright
import mistletoe
import base64


resources = [
    {"name": "markdown", "args": "/markdown"},
    {"name": "img", "args": "/img"},
]


class markdown(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('markdown', location='form', type=str)
        args = parser.parse_args()
        return {'message': 'success', 'html': mistletoe.markdown(args['markdown'])}


class img(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('html', location='form', type=str)
        parser.add_argument('github-markdown', location='form', type=str)
        parser.add_argument('timeout', location='form', type=int)
        args = parser.parse_args()
        args['html'] = args['html'].replace("\\n", "")
        if args['github-markdown'] is None:
            html = args['html']
        else:
            html = open(
                "modules/html/github-markdown-template.html").read().replace("%markdown%", args['html'])
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content(html)
            page.wait_for_timeout(3000)
            if args['github-markdown'] is None:
                rawBytes = page.screenshot(
                    type="png", full_page=True, timeout=args['timeout'])
            else:
                element_handle = page.query_selector("//article[@id='md']")
                rawBytes = element_handle.screenshot(
                    type="png", timeout=args['timeout'])
            browser.close()
        return {"message": "success", "image_base64": base64.b64encode(rawBytes).decode()}
