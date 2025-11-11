from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User
from functools import wraps

main_bp = Blueprint('main', __name__, template_folder='templates')

# --- 辅助装饰器 (用于检查是否需要强制修改密码) ---
def password_check(f):
    """如果用户需要修改密码，则强制跳转到修改页面。"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.needs_password_change:
            flash("出于安全考虑，请先修改您的初始密码。", 'info')
            return redirect(url_for('auth.change_password'))
        return f(*args, **kwargs)
    return decorated_function

# --- 路由定义 ---

@main_bp.route('/')
@main_bp.route('/index')
@login_required
@password_check # 【新增】在访问主页前进行密码检查
def index():
    # 示例数据（您提供的截图是 Web 打印队列）
    print_jobs = [
        {'id': 56, 'printer': 'N/A', 'title': 'N/A', 'user': 'N/A', 'status': '未激活', 'time': 'N/A'},
        # ... 更多数据 ...
        {'id': 1, 'printer': 'N/A', 'title': 'N/A', 'user': 'N/A', 'status': '未激活', 'time': 'N/A'},
    ]
    return render_template('index.html', title='Web 打印', jobs=print_jobs)