# coding=utf8
from app.models.models import *
from wtforms import Form, TextField, PasswordField, validators


class AdminUserForm(Form):
    user_name = TextField(u'用户名', [validators.Required(message=u"用户名不能为空。")])
    user_pass = PasswordField(u'密码', [validators.Required(message=u"密码不能为空。")])
