#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/5 19:03
@Author  : thezehui@gmail.com
@File    : module.py
"""
from flask_migrate import Migrate
from injector import Module, Binder
from internal.extension.database_extension import db
from internal.extension.migrate_extension import migrate
from pkg.sqlalchemy import SQLAlchemy


class ExtensionModule(Module):
    """扩展模块的依赖注入"""
    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)
