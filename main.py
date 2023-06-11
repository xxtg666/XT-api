import json
import os
import sys
import shutil
import random
import traceback
from flask import Flask
from flask_restful import Resource, Api
from loguru import logger as l
import importlib

l.info("正在启动 XT-api")
# 初始化缓存
try:
    shutil.rmtree("cache")
except:
    pass
os.mkdir("cache")
l.success("缓存初始化完成")
# 导入配置文件
try:
    cfg = json.load(open("config/main.json"))
    l.success("配置文件载入完成")
except:
    l.error("配置文件出现错误:\n"+traceback.format_exc())
    sys.exit(0)

# api主程序
app = Flask(__name__)
api = Api(app)


class XT_api(Resource):
    def get(self):
        return {'message': 'welcome to use XT-api'}


api.add_resource(XT_api, '/')
module_names = os.listdir("modules")
for module_name in module_names:
    if (module_name.endswith(".py") or os.path.isdir("modules/"+module_name)) and not module_name.startswith("_"):
        module_name = module_name.replace(".py", "")
        try:
            module = importlib.import_module("modules."+module_name)
            for res in module.resources:
                ep = "".join(random.choices(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=20))
                api.add_resource(
                    getattr(module, res["name"]), '/'+module_name+res["args"], endpoint=ep)
                l.success("模块 "+module_name+"." +
                          res["name"]+" 载入成功"+" (ep: "+ep+")")
        except:
            l.error("模块 "+module_name+" 载入失败:\n"+traceback.format_exc())
    else:
        l.warning(module_name+" 不是有效模块或已禁用")
l.success("XT-api 启动完成")
app.run(port=cfg["port"], host="0.0.0.0")
l.info("XT-api 已退出")
