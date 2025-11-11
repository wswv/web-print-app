from flask import render_template, redirect, url_for, flash, request, Blueprint, abort
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from sqlalchemy import or_

from .forms import LoginForm, ChangePasswordForm, UserManagementForm, RegisterForm
from models import db, User
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# --- 辅助装饰器 ---
def admin_required(f):
    """确保只有管理员才能访问的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("权限不足：只有管理员才能访问此页面。", 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# --- 路由定义 ---

# 登录路由 (保持不变)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # 假设 LoginForm 已经存在
    form = LoginForm() 
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).filter_by(username=form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误。', 'danger')
            return redirect(url_for('.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # 检查是否需要强制修改密码
        if user.needs_password_change:
            flash("出于安全考虑，请先修改您的初始密码。", 'info')
            return redirect(url_for('.change_password'))
        
        # 登录成功后跳转到首页或重定向页
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))

    return render_template('login.html', title='登录', form=form)

# 登出路由 (保持不变)
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# 【新增】用户修改自己密码的路由
@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm() # 假设 ChangePasswordForm 已经存在
    
    # 提交表单
    if form.validate_on_submit():
        # 1. 验证旧密码
        if not current_user.check_password(form.old_password.data):
            flash('原密码不正确。', 'danger')
            return redirect(url_for('.change_password'))
        
        # 2. 设置新密码（models.py中的 set_password 会自动设置 needs_password_change=False）
        current_user.set_password(form.new_password.data)
        
        try:
            db.session.commit()
            flash('密码修改成功。', 'success')
            return redirect(url_for('main.index'))
        except:
            db.session.rollback()
            flash('数据库错误，密码修改失败。', 'danger')
            return redirect(url_for('.change_password'))

    # 如果是 GET 请求，但用户需要修改密码，显示信息
    if current_user.needs_password_change and request.method == 'GET':
        flash("您正在使用初始密码，请务必修改！", 'warning')
        
    return render_template('change_password.html', title='修改密码', form=form)


# 【新增】管理员用户管理页面
@auth_bp.route('/admin/manage_users')
@login_required
@admin_required # 只有管理员能访问
def manage_users():
    users = db.session.scalars(db.select(User).order_by(User.id)).all()
    return render_template('manage_users.html', title='用户管理', users=users)

# 【新增】管理员编辑用户（权限/密码）
@auth_bp.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)

    form = UserManagementForm(obj=user) # 假设 UserManagementForm 已经存在
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.is_admin = form.is_admin.data
        
        # 仅当输入了新密码时才修改
        if form.new_password.data:
            # 注意：这里需要手动导入 generate_password_hash，因为它不在 models.py 的 User 类中
            user.password_hash = generate_password_hash(form.new_password.data)
            user.needs_password_change = False # 管理员修改后，视为密码已修改
        
        try:
            db.session.commit()
            flash(f'用户 {user.username} 已更新。', 'success')
            return redirect(url_for('.manage_users'))
        except IntegrityError:
            db.session.rollback()
            flash('用户名已存在，更新失败。', 'danger')
        except:
            db.session.rollback()
            flash('数据库错误，更新失败。', 'danger')

    return render_template('edit_user.html', title=f'编辑用户: {user.username}', form=form, user=user)

# 占位符，假设已包含
# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     ...
#     return render_template('register.html', title='注册', form=form)