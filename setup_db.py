#!/usr/local/bin/python
# setup_db.py

"""
此脚本用于在容器首次启动时执行数据库创建和初始用户设置。
它由 docker-entrypoint.sh 脚本调用。
"""

import sys
import os

# 确保项目根目录在 Python 路径中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run import create_app, initialize_database
from config import Config

if __name__ == "__main__":
    # 创建应用实例
    app = create_app(Config)
    
    # 调用初始化函数
    initialize_database(app)

    print("Database initialization complete. Ready to start Gunicorn.")