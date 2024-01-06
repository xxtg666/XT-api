from flask_restful import Resource, reqparse
import base64
import json
import time
import requests

resources = [
    {"name": "main", "args": ""},
]

def get_access_token(force_update=False):
    datafile = "config/baiduAPI.json"
    data = json.load(open(datafile, "r"))
    if not (force_update or data["expires_in"] < int(time.time())):
        return data["access_token"]
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={data['api_key']}&client_secret={data['secret_key']}"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data="")
    odata = json.loads(response.text)
    access_token = odata['access_token']
    expires_in = odata['expires_in']
    data["access_token"] = access_token
    data["expires_in"] = int(time.time()-30)+expires_in
    json.dump(data, open(datafile, "w"))
    return access_token

class main(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("img_base64", location='form', type=str)
        args = parser.parse_args()
        params = {"image": args["img_base64"].encode()}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(
            "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined?access_token=" + get_access_token(),
            data=params, headers=headers)
        return {'message': 'success', 'result': response.json()}