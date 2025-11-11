# auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import routes # 导入路由，使蓝图知道它的视图函数
