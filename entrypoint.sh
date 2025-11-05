# entrypoint.sh（终极·兼容所有模型）
#!/bin/sh
set -e

echo "等待数据库 10 秒..."
for i in $(seq 1 10); do
  mysqladmin ping -h db -u flask -pflaskpass --silent && break
  echo "第 $i 次尝试..."
  sleep 2
done
echo "数据库 OK！"

echo "自动建表 + 创建管理员..."
python -c "
import os
from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    db.create_all()
    username = os.getenv('ADMIN_USER', 'admin')
    password = os.getenv('ADMIN_PASS', '123456')
    
    if not User.query.filter_by(username=username).first():
        admin = User(username=username, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print('管理员创建成功！')
    else:
        print('管理员已存在')
    
    print(f'账号: {username}')
    print(f'密码: {password}')
"

exec "$@"