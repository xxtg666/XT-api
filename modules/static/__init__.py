import threading
import os
import json
from loguru import logger as l

resources = []

port = str(json.load(open("config/static.json"))["port"])
def start_static_server():
    os.system('python -m http.server --directory "modules/static/files" '+port)

threading.Thread(target=start_static_server).start()

l.success("Static File Server started on port "+port+" .")