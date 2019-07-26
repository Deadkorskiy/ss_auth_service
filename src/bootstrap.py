from flask import Flask
from flask import request
from werkzeug.exceptions import Forbidden
from settings import settings
from modules import shadowsocks

from router import health
from router import shadowsocks as shadowsocks_router



app = Flask(__name__)
app.url_map.strict_slashes = False


app.register_blueprint(shadowsocks_router.router, url_prefix="/api/shadowsocks")
app.register_blueprint(health.router, url_prefix="/health")


# create SSConf() to avoid race condition
shadowsocks.service.SSConf.get_instance()
