# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    # 【新增字段】用于追踪用户是否需要修改初始密码
    needs_password_change = db.Column(db.Boolean, default=True) 	
	

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        # 密码设置后，标记为已修改（不再是初始密码）
        self.needs_password_change = False 		

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
