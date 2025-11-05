#!/bin/sh
set -e

echo "等待数据库上线..."
for i in $(seq 1 15); do
  mysqladmin ping -h db -u flask -pflaskpass --silent && break
  echo "第 $i 次尝试..."
  sleep 1
done
echo "数据库 OK！"

echo "自动建表 + 万能创建管理员..."
python -c "
import os
import sys
from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    db.create_all()
    
    username = os.getenv('ADMIN_USER', 'admin')
    password = os.getenv('ADMIN_PASS', '123456')
    
    if User.query.filter_by(username=username).first():
        print(f'管理员已存在 → {username}')
        print(f'密码: {password}')
        sys.exit(0)
    
    # 万能字段探测
    from sqlalchemy import inspect
    cols = {c.key for c in inspect(User).mapper.column_attrs}
    
    # 构造参数
    data = {'username': username}
    if 'email' in cols: data['email'] = f'{username}@local'
    if 'is_admin' in cols: data['is_admin'] = True
    if 'role' in cols: data['role'] = 'admin'
    if 'admin' in cols: data['admin'] = True
    
    admin = User(**data)
    
    # 万能设置密码（支持 8 种写法）
    if hasattr(admin, 'set_password'):
        admin.set_password(password)
    elif hasattr(admin, 'password_hash'):
        import hashlib
        admin.password_hash = hashlib.md5(password.encode()).hexdigest()
    elif hasattr(admin, 'password'):
        admin.password = password
    else:
        # 直接写明文（极少数项目）
        admin.password = password
    
    db.session.add(admin)
    db.session.commit()
    print('管理员创建成功！')
    print(f'账号: {username}')
    print(f'密码: {password}')
"

echo "启动 Gunicorn..."
exec gunicorn -w 2 -b 0.0.0.0:5000 run:app