#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/1 14:42
@Author  : thezehui@gmail.com
@File    : app_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    """基础聊天接口请求验证"""
    # 必填、长度最大为2000
    query = StringField("query", validators=[
        DataRequired(message="用户的提问是必填"),
        Length(max=2000, message="用户的提问最大长度是2000"),
    ])
