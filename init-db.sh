#!/bin/bash
flask db init
flask db migrate
flask db upgrade
python -c "
from app import db, create_app
from app.models import User
from werkzeug.security import generate_password_hash
app = create_app()
with app.app_context():
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', password=generate_password_hash('123456')))
        db.session.commit()
        print('admin/123456 创建成功')
"