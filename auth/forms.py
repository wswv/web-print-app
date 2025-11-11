from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Optional
from models import db, User

# 假设这个表单已经存在
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

# 【新增】用户修改自己密码的表单
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认新密码', validators=[
        DataRequired(), 
        EqualTo('new_password', message='两次输入的新密码不一致。')
    ])
    submit = SubmitField('修改密码')

# 【新增】管理员编辑用户的表单
class UserManagementForm(FlaskForm):
    # 用户名需要唯一性检查
    username = StringField('用户名', validators=[DataRequired()])
    is_admin = BooleanField('管理员权限')
    # 密码可选，不输入则不修改
    new_password = PasswordField('新密码 (留空则不修改)', validators=[
        Optional(), 
        EqualTo('confirm_password', message='两次输入的新密码不一致。')
    ])
    confirm_password = PasswordField('确认新密码', validators=[Optional()])
    submit = SubmitField('保存')

    def validate_username(self, username):
        user = db.session.scalar(db.select(User).filter_by(username=username.data))
        # 只有在创建新用户或修改用户名与现有用户冲突时才触发错误
        # 对于编辑现有用户，需要检查它是否是当前用户本身
        if user is not None and user.id != self._obj.id:
            raise ValidationError('该用户名已被使用。')

# 占位符，假设已包含
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('注册')