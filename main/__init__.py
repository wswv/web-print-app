# main/__init__.py
from flask import Blueprint

main_bp = Blueprint('main', __name__)

from . import routes # 导入路由，使蓝图知道它的视图函数
