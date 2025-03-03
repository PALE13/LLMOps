#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_migrate import Migrate
from injector import Module, Binder,Injector
from redis import Redis
from pkg.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_weaviate import FlaskWeaviate

from internal.extension.database_extension import db
from internal.extension.migrate_extension import migrate
from internal.extension.redis_extension import redis_client
from internal.extension.login_extension import login_manager
from internal.extension.weaviate_extension import weaviate

class ExtensionModule(Module):
    """扩展模块的依赖注入"""
    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)
        binder.bind(Redis, to=redis_client)
        binder.bind(LoginManager, to=login_manager)
        binder.bind(FlaskWeaviate, to=weaviate)


injector = Injector([ExtensionModule])
