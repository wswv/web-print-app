# config.py

import os

# 定义基础目录 (这是容器的工作目录)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # --- 基本配置 ---
    SECRET_KEY = 'your_secret_key_123'
    
    # --- CUPS 配置 ---
    # 请将 '10.1.1.219' 替换为您局域网 CUPS 服务器的实际 IP
    CUPS_SERVER_IP = '10.1.1.219' 
    CUPS_SERVER_PORT = 631
    CUPS_SERVER = CUPS_SERVER_IP
    CUPS_PORT = CUPS_SERVER_PORT

    # --- 文件/上传配置 ---
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'}
    
    # --- 数据库配置 ---
    # 使用绝对路径指向 /usr/src/app/users.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'users.db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
